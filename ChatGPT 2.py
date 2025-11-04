# eldenvale_rpg.py
# Eldenvale — a 2D open-world RPG demo with dynamic lighting, NPCs, quests, combat, and inventory.
# Procedural art, no external assets required. Uses pygame.
#
# Run: pip install pygame
#      python eldenvale_rpg.py

import pygame, random, math, json, sys, time, os
from collections import deque

### ---------------------- CONFIG ------------------------
WIDTH, HEIGHT = 1200, 720
FPS = 60
TILE = 48                # base tile visual size (world is continuous)
MAP_W, MAP_H = 48, 36    # tiles
WORLD_W, WORLD_H = MAP_W * TILE, MAP_H * TILE
DAY_LENGTH = 120.0       # seconds per full day cycle
SAVE_FILE = "eldenvale_save.json"

# Player stats
BASE_HP = 120
BASE_MANA = 80
BASE_SPEED = 160.0       # px/sec
SPRINT_MULT = 1.55
ATTACK_COOLDOWN = 0.45
SPELL_COOLDOWN = 1.0

# Colors
COL_SKY_DAY = (132, 191, 255)
COL_SKY_DUSK = (140, 110, 170)
COL_SKY_NIGHT = (12, 18, 38)
COL_GRASS = (80, 155, 76)
COL_TERRAIN = (120, 100, 60)
COL_WATER = (50, 110, 170)
COL_UI_PANEL = (18, 20, 28, 220)
COL_TEXT = (238, 238, 238)
COL_ACCENT = (230, 200, 120)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eldenvale — RPG Demo")
clock = pygame.time.Clock()
small = pygame.font.SysFont("Consolas", 16)
med = pygame.font.SysFont("Consolas", 20, True)
big = pygame.font.SysFont("Consolas", 32, True)

### ---------------------- UTIL --------------------------
def clamp(x, a, b): return max(a, min(b, x))
def dist(a,b): return math.hypot(a[0]-b[0], a[1]-b[1])
def lerp(a,b,t): return a + (b-a)*t
def color_lerp(c1,c2,t): return tuple(int(lerp(c1[i],c2[i],t)) for i in range(3))

### ---------------------- WORLD GEN ---------------------
random.seed(1337)
world_tiles = [[None for _ in range(MAP_W)] for __ in range(MAP_H)]

def gen_world():
    # Simple noise-ish procedural world: grass, water, rock, forest, village
    for y in range(MAP_H):
        for x in range(MAP_W):
            nx = x/MAP_W - 0.5
            ny = y/MAP_H - 0.5
            d = math.hypot(nx, ny)
            # lakes
            r = random.random()
            if d > 0.43 and r < 0.5:
                t = 'water'
            elif r < 0.08:
                t = 'rock'
            elif r < 0.26:
                t = 'forest'
            else:
                t = 'grass'
            world_tiles[y][x] = t

    # carve a village in the center
    cx, cy = MAP_W//2, MAP_H//2
    for dy in range(-2,3):
        for dx in range(-3,4):
            world_tiles[cy+dy][cx+dx] = 'village'
    # make a river
    rx = random.randint(6, MAP_W-7)
    for y in range(MAP_H):
        w = int(1 + 2*math.sin(y*0.4 + random.random()*2))
        for xx in range(max(0, rx-w), min(MAP_W, rx+w)):
            world_tiles[y][xx] = 'water'
    # paths
    for i in range(6):
        x1,y1 = random.randint(0,MAP_W-1), random.randint(0,MAP_H-1)
        x2,y2 = cx, cy
        carve_path(x1,y1,x2,y2)
    return

def carve_path(x1,y1,x2,y2):
    x,y = x1,y1
    for _ in range(500):
        world_tiles[y][x] = 'path'
        if x==x2 and y==y2: break
        if random.random() < 0.6:
            x += 1 if x<x2 else (-1 if x>x2 else 0)
        else:
            y += 1 if y<y2 else (-1 if y>y2 else 0)
        x = clamp(x,0,MAP_W-1); y = clamp(y,0,MAP_H-1)

gen_world()

### ---------------------- ENTITIES ---------------------
class Entity:
    def __init__(self,x,y,r=12):
        self.x=x; self.y=y; self.r=r
        self.vx=0; self.vy=0
        self.dead=False

    def pos(self): return (self.x,self.y)

    def distance_to(self, other):
        return dist((self.x,self.y),(other.x,other.y))

class Player(Entity):
    def __init__(self,x,y):
        super().__init__(x,y, r=14)
        self.hp=BASE_HP; self.max_hp=BASE_HP
        self.mana=BASE_MANA; self.max_mana=BASE_MANA
        self.xp=0; self.level=1
        self.gold=0
        self.speed=BASE_SPEED
        self.last_attack=-999
        self.last_spell=-999
        self.inventory = {}
        self.quest_log = []
        self.name = "Wanderer"

    def can_attack(self, now):
        return (now - self.last_attack) >= ATTACK_COOLDOWN

    def can_cast(self, now):
        return (now - self.last_spell) >= SPELL_COOLDOWN and self.mana >= 10

player = Player(WORLD_W//2 + 20, WORLD_H//2 + 20)

class NPC(Entity):
    def __init__(self,x,y,name,portrait=None, dialog_tree=None):
        super().__init__(x,y,r=14)
        self.name=name
        self.dialog_tree = dialog_tree or []
        self.portrait = portrait
        self.talked = False

class Enemy(Entity):
    def __init__(self,x,y, kind='wolf'):
        super().__init__(x,y,r=13)
        self.kind = kind
        self.hp = 40 if kind=='wolf' else 120
        self.max_hp = self.hp
        self.state = 'wander'   # wander, chase, attack
        self.ai_timer = random.random()*2

enemies = []
npcs = []

### populate world with NPCs and enemies
def spawn_entities():
    npcs.clear(); enemies.clear()
    # spawn some NPCs in village center
    vcx, vcy = MAP_W//2 * TILE + TILE//2, MAP_H//2 * TILE + TILE//2
    elders = [
        NPC(vcx+40, vcy+10, "Elder Rowan"),
        NPC(vcx-60, vcy+18, "Healer Miri"),
        NPC(vcx+10, vcy-50, "Guard Haret")
    ]
    npcs.extend(elders)

    # add a starter quest to Elder Rowan
    elders[0].dialog_tree = [
        ("greeting", "Welcome, traveler. The valley stirs — dark wolves prowl the Ravine. Will you hunt them for the village?"),
        ("offer", "If you bring 3 Wolf Pelts, I'll teach you a secret restoration charm."),
        ("accept", "Thank you. Return with pelts and I'll reward you."),
        ("decline", "I see. Stay safe then.")
    ]

    # spawn hostile wolves and one orc
    for i in range(8):
        x = random.randint(10, MAP_W-10)*TILE + random.randint(0,TILE-8)
        y = random.randint(6, MAP_H-6)*TILE + random.randint(0,TILE-8)
        if world_tile_at(x,y) != 'water':
            enemies.append(Enemy(x,y,'wolf'))
    # one stronger enemy near edge
    ex = random.randint(2, MAP_W-3)*TILE
    ey = random.randint(2, MAP_H-3)*TILE
    enemies.append(Enemy(ex,ey,'orc'))
spawn_entities()

def world_tile_at(px,py):
    tx = clamp(int(px // TILE), 0, MAP_W-1)
    ty = clamp(int(py // TILE), 0, MAP_H-1)
    return world_tiles[ty][tx]

### ---------------------- DIALOG/QUEST SYSTEM ----------------------
class DialogSession:
    def __init__(self, npc):
        self.npc = npc
        self.stage = 0
        # simple linear tree for demo
        self.options = []
        self.open = True

    def current_text(self):
        dt = self.npc.dialog_tree
        if not dt: return "..."
        # cycle through dialog segments for demo
        idx = min(self.stage, len(dt)-1)
        return dt[idx][1]

    def choose(self, idx):
        # demo branching: choose 0 accept, 1 decline if available
        if self.npc.name == "Elder Rowan":
            if self.stage == 0:
                # after greeting -> offer
                self.stage = 1
                return
            if self.stage == 1:
                # present Accept / Decline
                if idx == 0:  # accept
                    self.stage = 2
                    self.npc.talked = True
                    player.quest_log.append({"id":"wolf_pelts","progress":0,"complete":False})
                else:
                    self.stage = 3
                return
        # fallback: close
        self.open = False

### ---------------------- INVENTORY & UI ----------------------
def add_item(name, qty=1):
    player.inventory[name] = player.inventory.get(name,0) + qty

def remove_item(name, qty=1):
    if player.inventory.get(name,0)>=qty:
        player.inventory[name] -= qty
        if player.inventory[name] <= 0: del player.inventory[name]; return True
        return True
    return False

### ---------------------- PARTICLES & LIGHTS ----------------------
particles = []
lights = []  # (x,y,radius,color,intensity)

def spawn_particle(x,y,dx,dy,col,life=30):
    particles.append([x,y,dx,dy,col,life])

def update_particles():
    for p in particles[:]:
        p[0]+=p[2]; p[1]+=p[3]; p[3]+=0.08; p[5]-=1
        if p[5]<=0: particles.remove(p)

### ---------------------- INPUT & CAMERA ----------------------
camx, camy = player.x - WIDTH//2, player.y - HEIGHT//2
dialog = None
message_queue = deque(maxlen=6)
def push_message(s):
    message_queue.appendleft((s, time.time()))

### ---------------------- COMBAT & AI ----------------------
def player_attack(now, target):
    if player.can_attack(now):
        player.last_attack = now
        # simple melee hit if within range
        if player.distance_to(target) < 46:
            dmg = random.randint(14, 24)
            target.hp -= dmg
            spawn_particle(target.x, target.y, (random.uniform(-1,1))*2, -1.5, (255,120,40), 20)
            push_message(f"Hit {target.kind} for {dmg} dmg")
            if target.hp <= 0:
                target.dead = True
                if target.kind == 'wolf':
                    add_item("Wolf Pelt",1); player.gold += random.randint(5,12)
                    push_message("You collected a Wolf Pelt.")
                else:
                    add_item("Orc Tooth",1); player.gold += random.randint(20,40)
                player.xp += 20

def player_cast(now, tx, ty):
    if player.can_cast(now):
        # basic fireball style projectile
        player.last_spell = now
        player.mana -= 12
        # spawn a high-speed projectile
        dx,dy = tx - player.x, ty - player.y
        mag = math.hypot(dx,dy) or 1
        vx,vy = dx/mag*520, dy/mag*520
        projectiles.append([player.x, player.y, vx, vy, 18, (255,120,40), 50, time.time()])
        push_message("Cast Firebolt!")

projectiles = []  # [x,y,vx,vy,r,color,life,spawn_time]

def update_projectiles(dt):
    for p in projectiles[:]:
        p[0]+=p[2]*dt; p[1]+=p[3]*dt; p[6]-=dt*FPS
        if p[6] <= 0:
            try: projectiles.remove(p)
            except: pass
            continue
        # collide with enemies
        for e in enemies:
            if not e.dead and dist((p[0],p[1]), (e.x,e.y)) < p[4]+e.r:
                e.hp -= 26
                spawn_particle(e.x, e.y, (random.uniform(-1,1))*3, -2, (255,200,80), 26)
                if e.hp <= 0:
                    e.dead = True
                    if e.kind=='wolf': add_item("Wolf Pelt",1)
                try: projectiles.remove(p); break
                except: pass

def enemies_update(dt):
    for e in enemies:
        if e.dead: continue
        dx = player.x - e.x; dy = player.y - e.y
        d = math.hypot(dx,dy)
        e.ai_timer -= dt
        if d < 180:
            # chase
            dirx,diry = dx/d if d!=0 else 0, dy/d if d!=0 else 0
            speed = 80 if e.kind=='wolf' else 56
            e.x += dirx * speed * dt
            e.y += diry * speed * dt
            # attack if close
            if d < 32 and random.random() < 0.02:
                player.hp -= (6 if e.kind=='wolf' else 14) * dt * 7  # damage rate
        else:
            # wander
            if e.ai_timer <= 0:
                e.vx = random.uniform(-40,40)
                e.vy = random.uniform(-40,40)
                e.ai_timer = 1.0 + random.random()*3.0
            e.x += e.vx * dt
            e.y += e.vy * dt
        # clamp to world and avoid water by small push
        t = world_tile_at(e.x,e.y)
        if t == 'water':
            e.y -= 12*dt*40

### ---------------------- DRAWING ----------------------
def draw_world(surface, cx, cy, t):
    # sky gradient based on day time
    day_t = (t % DAY_LENGTH) / DAY_LENGTH  # 0..1
    # map day_t to sky color
    if day_t < 0.25:
        # dawn -> day
        s = day_t / 0.25
        sky = color_lerp(COL_SKY_DUSK, COL_SKY_DAY, s)
    elif day_t < 0.65:
        s = (day_t - 0.25) / 0.4
        sky = color_lerp(COL_SKY_DAY, COL_SKY_DAY, s)
    elif day_t < 0.85:
        s = (day_t - 0.65) / 0.2
        sky = color_lerp(COL_SKY_DAY, COL_SKY_DUSK, s)
    else:
        s = (day_t - 0.85) / 0.15
        sky = color_lerp(COL_SKY_DUSK, COL_SKY_NIGHT, s)
    surface.fill(sky)

    # parallax distant mountains
    for layer, offset_scale, shade in [(1,0.2,(40,40,50)), (2,0.35,(28,28,36))]:
        for i in range(-1,4):
            px = -cx*offset_scale + i*500 + 80
            py = 140 + 20*layer
            pygame.draw.polygon(surface, shade, [(px+0,py+220),(px+140,py+40),(px+260,py+120),(px+360,py+40),(px+520,py+200)])

    # draw tiles
    for ty in range(MAP_H):
        for tx in range(MAP_W):
            x = tx*TILE - cx
            y = ty*TILE - cy
            ttype = world_tiles[ty][tx]
            if ttype == 'grass' or ttype == 'village' or ttype == 'path':
                pygame.draw.rect(surface, COL_GRASS, (x,y,TILE+1,TILE+1))
            if ttype == 'water':
                pygame.draw.rect(surface, COL_WATER, (x,y,TILE+1,TILE+1))
            if ttype == 'rock':
                pygame.draw.rect(surface, (120,110,100), (x,y,TILE+1,TILE+1))
            if ttype == 'forest':
                pygame.draw.rect(surface, (70, 120, 60), (x,y,TILE+1,TILE+1))
            if ttype == 'path':
                pygame.draw.rect(surface, (150,120,80), (x,y,TILE+1,TILE+1))
            # small decorative
            if ttype == 'village':
                # houses: draw roof & door
                pygame.draw.rect(surface, (200,170,120), (x+6,y+6, TILE-12, TILE-12))
                pygame.draw.polygon(surface, (120,70,40), [(x+6,y+6),(x+TILE/2,y-6),(x+TILE-6,y+6)])
    # trees (draw above ground for nice layering)
    for ty in range(MAP_H):
        for tx in range(MAP_W):
            ttype = world_tiles[ty][tx]
            if ttype == 'forest':
                x = tx*TILE - cx + TILE//2
                y = ty*TILE - cy + TILE//2
                # trunk
                pygame.draw.rect(surface, (80,50,30), (x-6,y+6,12,18))
                # leaves
                pygame.draw.circle(surface, (28,90,36), (x,y), 20)

def draw_entities(surface, cx, cy, now):
    # NPCs
    for n in npcs:
        px,py = n.x - cx, n.y - cy
        pygame.draw.circle(surface, (200,180,80), (int(px),int(py)), n.r)
        # name
        txt = small.render(n.name, True, COL_TEXT)
        surface.blit(txt, (px - txt.get_width()/2, py - n.r - 18))
    # enemies
    for e in enemies:
        if e.dead: continue
        col = (170,80,60) if e.kind=='orc' else (140,110,80)
        px,py = e.x - cx, e.y - cy
        # body
        pygame.draw.circle(surface, col, (int(px),int(py)), e.r)
        # hp bar
        frac = e.hp / e.max_hp
        pygame.draw.rect(surface, (20,20,20), (px-18, py-e.r-14, 36,6))
        pygame.draw.rect(surface, (200,50,50), (px-18, py-e.r-14, int(36*frac),6))

    # projectiles
    for p in projectiles:
        pygame.draw.circle(surface, p[5], (int(p[0]-cx), int(p[1]-cy)), p[4])

    # player
    px,py = player.x - cx, player.y - cy
    pygame.draw.circle(surface, (240,240,255), (int(px),int(py)), player.r)
    # player face / direction
    ang = math.atan2(player.vy, player.vx) if (player.vx or player.vy) else 0
    ex = px + math.cos(ang)*player.r*0.6
    ey = py + math.sin(ang)*player.r*0.6
    pygame.draw.circle(surface, (60,60,90), (int(ex),int(ey)), 6)

### lighting pass (simple radial darkness at night + torches)
def draw_lighting(surface, cx, cy, now):
    day_t = (now % DAY_LENGTH) / DAY_LENGTH
    # compute darkness
    darkness = 0.0
    if day_t < 0.15:
        darkness = 0.5*(1 - (day_t/0.15))
    elif day_t < 0.3:
        darkness = 0.0
    elif day_t < 0.7:
        darkness = 0.0
    elif day_t < 0.85:
        darkness = 0.5*( (day_t-0.7)/0.15 )
    else:
        darkness = 0.8
    if darkness <= 0.02:
        return
    dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark.fill((8,10,18, int(200*darkness)))
    # create light holes for player & torches
    # player light
    lx = int(player.x - cx); ly = int(player.y - cy)
    pygame.draw.circle(dark, (0,0,0,0), (lx,ly), int(160), 0)
    # NPC torches - simple per village NPC
    for n in npcs:
        nx,ny = int(n.x-cx), int(n.y-cy)
        pygame.draw.circle(dark, (0,0,0,0), (nx,ny), 80)
    surface.blit(dark, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

### ---------------------- UI DRAW ----------------------
def draw_ui(surface, now):
    # bottom panel
    panel = pygame.Surface((WIDTH, 84), pygame.SRCALPHA)
    panel.fill(COL_UI_PANEL)
    surface.blit(panel, (0, HEIGHT-84))
    # player stats
    hp_text = med.render(f"HP: {int(player.hp)}/{player.max_hp}", True, COL_TEXT)
    mana_text = med.render(f"Mana: {int(player.mana)}/{player.max_mana}", True, COL_TEXT)
    xp_text = small.render(f"XP: {player.xp}  Lvl: {player.level}", True, COL_TEXT)
    gold_text = small.render(f"Gold: {player.gold}", True, COL_ACCENT)
    surface.blit(hp_text, (16, HEIGHT-72))
    surface.blit(mana_text, (16, HEIGHT-44))
    surface.blit(xp_text, (220, HEIGHT-70))
    surface.blit(gold_text, (220, HEIGHT-44))
    # quick help
    help_text = small.render("WASD/Arrows: move  •  Left Click: attack  •  Right Click: Cast  •  E: Talk  •  I: Inventory", True, (200,200,200))
    surface.blit(help_text, (420, HEIGHT-60))
    # quest preview
    surface.blit(med.render("Quest Log", True, COL_ACCENT), (WIDTH-220, HEIGHT-78))
    qy = HEIGHT-56
    for q in player.quest_log[-3:]:
        status = "Done" if q.get("complete") else f"{q.get('progress',0)}/3"
        surface.blit(small.render(f"- {q['id'].replace('_',' ').title()} ({status})", True, COL_TEXT), (WIDTH-220, qy))
        qy += 18

    # messages
    mx = 16
    my = HEIGHT-100
    for i,(m,t) in enumerate(list(message_queue)[:4]):
        a = max(0, 1 - (time.time()-t)/5.0)
        txt = small.render(m, True, (255,255,255))
        surface.blit(txt, (mx, my - i*18))

### ---------------------- SAVE/LOAD ----------------------
def save_game():
    data = {
        'player': {'x':player.x,'y':player.y,'hp':player.hp,'mana':player.mana,'xp':player.xp,'gold':player.gold,'inventory':player.inventory,'level':player.level},
        'time': now_time
    }
    try:
        with open(SAVE_FILE,'w') as f:
            json.dump(data,f)
        push_message("Game saved.")
    except Exception as e:
        push_message("Save failed.")

def load_game():
    if not os.path.exists(SAVE_FILE): return
    try:
        with open(SAVE_FILE,'r') as f:
            data = json.load(f)
        p = data.get('player',{})
        player.x = p.get('x',player.x); player.y=p.get('y',player.y)
        player.hp = p.get('hp',player.hp); player.mana = p.get('mana',player.mana)
        player.xp = p.get('xp',player.xp); player.gold = p.get('gold',player.gold)
        player.inventory = p.get('inventory',player.inventory)
        player.level = p.get('level',player.level)
        push_message("Game loaded.")
    except Exception as e:
        push_message("Load failed.")

### ---------------------- MAIN LOOP ----------------------
now_time = 0.0
running = True
mouse_down = False
show_inventory = False
dialog_session = None

# initial small tutorial items
add_item("Bread", 2)
add_item("Torch", 1)

push_message("Welcome to Eldenvale — press E to talk to NPCs in town.")

while running:
    dt = clock.tick(FPS) / 1000.0
    now_time += dt
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
            if ev.key == pygame.K_i:
                show_inventory = not show_inventory
            if ev.key == pygame.K_e:
                # talk if near NPC
                for n in npcs:
                    if dist((n.x,n.y),(player.x,player.y)) < 80:
                        dialog_session = DialogSession(n)
                        push_message(f"Talking to {n.name}")
                        break
            if ev.key == pygame.K_F5:
                save_game()
            if ev.key == pygame.K_F9:
                load_game()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                mouse_down = True
            if ev.button == 3:
                mouse_down = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    # INPUT: movement
    keys = pygame.key.get_pressed()
    mx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
    my = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
    running_input = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    spd = player.speed * (SPRINT_MULT if running_input else 1.0)
    # normalize move
    if mx==0 and my==0:
        vx,vy=0,0
    else:
        mag = math.hypot(mx,my) or 1
        vx,vy = mx/mag*spd, my/mag*spd
    player.vx, player.vy = vx, vy
    player.x += player.vx * dt
    player.y += player.vy * dt
    player.x = clamp(player.x, 8, WORLD_W-8); player.y = clamp(player.y, 8, WORLD_H-8)

    # mouse actions
    mxs, mys = pygame.mouse.get_pos()
    world_mx, world_my = camx + mxs, camy + mys
    now = now_time
    if mouse_down:
        # left click = attack (projectile spawned instantly towards mouse)
        if pygame.mouse.get_pressed()[0]:
            # melee impulse: attack nearest enemy in front of player
            for e in enemies:
                if not e.dead and dist((e.x,e.y),(player.x,player.y)) < 60:
                    player_attack(now, e)
                    break
        # right click = cast
        if pygame.mouse.get_pressed()[2]:
            player_cast(now, world_mx, world_my)
            mouse_down = False

    # regen mana slowly
    player.mana = clamp(player.mana + 6*dt, 0, player.max_mana)
    # small HP regen if resting and no enemies near
    if all(dist((e.x,e.y),(player.x,player.y)) > 160 for e in enemies):
        player.hp = clamp(player.hp + 4*dt, 0, player.max_hp)

    # update enemies & projectiles & particles
    update_projectiles(dt)
    enemies_update(dt)
    update_particles()

    # update camera smoothly
    camx = player.x - WIDTH/2
    camy = player.y - HEIGHT/2
    camx = clamp(camx, 0, WORLD_W - WIDTH)
    camy = clamp(camy, 0, WORLD_H - HEIGHT)

    # interactions: quest completion check
    for q in player.quest_log:
        if q['id']=='wolf_pelts' and not q.get('complete'):
            if player.inventory.get("Wolf Pelt",0) >= 3:
                q['complete'] = True
                remove_item("Wolf Pelt",3)
                add_item("Restoration Charm", 1)
                player.xp += 120
                push_message("Quest complete: Wolf Pelts — You received a Restoration Charm!")
                # teach a spell / buff
                player.max_hp += 15
                player.hp = player.max_hp

    # handle dialog UI
    if dialog_session:
        # simple dialog progression by pressing number keys or space
        pass

    # Cull dead enemies occasionally and respawn in far regions
    if random.random() < 0.01:
        for e in enemies[:]:
            if e.dead and random.random() < 0.02:
                enemies.remove(e)
                # spawn new
                rx = random.randint(2,MAP_W-2)*TILE
                ry = random.randint(2,MAP_H-2)*TILE
                enemies.append(Enemy(rx,ry, random.choice(['wolf','wolf','orc'])))

    # DRAW
    draw_world(screen, camx, camy, now_time)
    draw_entities(screen, camx, camy, now_time)
    draw_lighting(screen, camx, camy, now_time)

    # projectiles & particles drawn inside draw_entities / particles loop
    for p in particles:
        pygame.draw.circle(screen, p[4], (int(p[0]-camx), int(p[1]-camy)), 3)

    # UI
    draw_ui(screen, now_time)

    # inventory overlay
    if show_inventory:
        inv_surf = pygame.Surface((460, 420), pygame.SRCALPHA)
        inv_surf.fill((10,10,12,230))
        pygame.draw.rect(inv_surf, (80,80,100), (12,12,436,396), 2)
        inv_surf.blit(big.render("Inventory", True, COL_ACCENT), (24,16))
        y = 70
        for k,v in player.inventory.items():
            inv_surf.blit(med.render(f"{k}: {v}", True, COL_TEXT), (24,y)); y+=28
        inv_surf.blit(med.render("Press I to close. F5 save, F9 load.", True, (200,200,200)), (24, 380))
        screen.blit(inv_surf, (WIDTH//2 - 230, HEIGHT//2 - 210))

    # dialog window
    if dialog_session and dialog_session.open:
        dlg = pygame.Surface((640,140), pygame.SRCALPHA)
        dlg.fill((20,20,26,230))
        pygame.draw.rect(dlg, (90,90,100), (6,6,628,128),2)
        text = dialog_session.current_text()
        lines = []
        words = text.split(" ")
        cur = ""
        for w in words:
            if med.size(cur + w + " ")[0] < 600:
                cur += w + " "
            else:
                lines.append(cur); cur = w + " "
        lines.append(cur)
        y = 12
        dlg.blit(med.render(dialog_session.npc.name, True, COL_ACCENT), (12,y)); y+=36
        for ln in lines:
            dlg.blit(small.render(ln, True, COL_TEXT), (12,y)); y+=22
        dlg.blit(small.render("Press 1:Continue  2:Accept  3:Decline  (Space closes)", True, (200,200,200)), (360,100))
        screen.blit(dlg, (WIDTH//2 - 320, HEIGHT-180))

        # handle key presses for dialogue
        k = pygame.key.get_pressed()
        if k[pygame.K_SPACE]:
            dialog_session.open = False
            dialog_session = None
        if k[pygame.K_1]:
            dialog_session.choose(0)
            # small delay
            time.sleep(0.18)
        if k[pygame.K_2]:
            dialog_session.choose(0)
            time.sleep(0.18)
        if k[pygame.K_3]:
            dialog_session.choose(1)
            time.sleep(0.18)

    # minimap
    mm = pygame.Surface((180,140), pygame.SRCALPHA)
    mm.fill((10,12,18,200))
    # draw simplified tiles
    tw = 180 / MAP_W; th = 140 / MAP_H
    for y in range(MAP_H):
        for x in range(MAP_W):
            c = (40,160,40) if world_tiles[y][x] in ('grass','village','forest') else (20,20,110) if world_tiles[y][x]=='water' else (120,100,70)
            mm.fill(c, (int(x*tw), int(y*th), int(tw)+1, int(th)+1))
    # player dot
    px = int(player.x / WORLD_W * 180); py = int(player.y / WORLD_H * 140)
    pygame.draw.circle(mm, (255,240,200), (px,py), 3)
    screen.blit(mm, (WIDTH-200, 12))
    pygame.draw.rect(screen, (200,200,200), (WIDTH-200, 12, 180, 140), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()

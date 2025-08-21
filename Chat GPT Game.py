import pygame
import random
import math
import sys

# -----------------------------
# Wyrmvale: a tiny 2D action RPG
# -----------------------------
# Controls:
#   Move: WASD
#   Sprint: Hold LEFT SHIFT (uses stamina)
#   Attack: SPACE (short sword slash with cooldown)
#   Interact/Talk: E (near NPC)
#   Toggle Inventory: I
#   Toggle Help: H
#   Quit: ESC / window close
#
# Goal:
#   Talk to the Elder (in village) to receive a quest:
#   Gather 3 Moonherbs from the wild and return for a reward.
#
# Notes:
#   - Pure pygame, no external images. Just shapes/colors.
#   - Basic AI (wolves) that wander/chase.
#   - Loot drops, inventory, health/stamina, simple UI panels.
#   - Resizable camera viewport with smooth scrolling.

# -----------------------------
# Config
# -----------------------------
WIDTH, HEIGHT = 960, 540          # initial window size (resizable)
TILE = 32                         # tile size
MAP_W, MAP_H = 60, 60             # world dimensions in tiles
FPS = 60

# Player stats
PLAYER_SPEED = 2.2
PLAYER_SPRINT = 3.6
PLAYER_MAX_HP = 100
PLAYER_MAX_STAM = 100
STAMINA_DRAIN = 22 / FPS
STAMINA_REGEN = 14 / FPS

# Combat
ATTACK_COOLDOWN = 0.45            # seconds
ATTACK_RANGE = 42                 # pixels
ATTACK_ARC_DEG = 70               # +/- degrees
ATTACK_DAMAGE = 35

# Enemies
WOLF_HP = 55
WOLF_SPEED = 1.7
WOLF_CHASE_RANGE = 220
WOLF_LEASH = 320
WOLF_DAMAGE = 15
WOLF_RESPAWN_SEC = 15

# Herbs
HERB_COUNT = 7

# Colors
COL_BG = (18, 20, 26)
COL_GRASS = (46, 120, 52)
COL_WATER = (30, 80, 130)
COL_ROCK = (95, 95, 110)
COL_TREE = (22, 70, 30)
COL_PATH = (150, 120, 80)
COL_UI = (10, 10, 12)
COL_PANEL = (20, 22, 30)
COL_ACCENT = (255, 215, 100)
COL_HP = (200, 60, 60)
COL_STAM = (70, 180, 200)
COL_TEXT = (230, 230, 235)
COL_NPC = (220, 210, 160)
COL_PLAYER = (255, 255, 255)
COL_WOLF = (140, 120, 100)
COL_HERB = (60, 200, 100)
COL_SLASH = (250, 250, 180)

pygame.init()
pygame.display.set_caption("Wyrmvale – a tiny RPG")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
base_font = pygame.font.SysFont("consolas", 18)
big_font = pygame.font.SysFont("consolas", 28, True)

# -----------------------------
# World generation (simple)
# -----------------------------
# Tiles: 0 = grass, 1 = water, 2 = rock/cliff, 3 = tree, 4 = path, 5 = village floor
GRASS, WATER, ROCK, TREE, PATH, VILLAGE = 0, 1, 2, 3, 4, 5

def make_world(w, h):
    rng = random.Random(42)
    tiles = [[GRASS for _ in range(w)] for _ in range(h)]

    # Scatter lakes
    for _ in range(7):
        cx, cy = rng.randrange(w), rng.randrange(h)
        r = rng.randrange(3, 8)
        for y in range(h):
            for x in range(w):
                if (x-cx)**2 + (y-cy)**2 <= r*r and rng.random() < 0.9:
                    tiles[y][x] = WATER

    # Scatter cliffs/rocks
    for _ in range(200):
        x, y = rng.randrange(w), rng.randrange(h)
        for _ in range(rng.randrange(10, 40)):
            if 0 <= x < w and 0 <= y < h:
                if tiles[y][x] == GRASS and rng.random() < 0.8:
                    tiles[y][x] = ROCK
            x += rng.choice([-1, 0, 1])
            y += rng.choice([-1, 0, 1])

    # Forests (trees)
    for _ in range(120):
        x, y = rng.randrange(w), rng.randrange(h)
        for _ in range(rng.randrange(15, 60)):
            if 0 <= x < w and 0 <= y < h:
                if tiles[y][x] == GRASS and rng.random() < 0.7:
                    tiles[y][x] = TREE
            x += rng.choice([-1, 0, 1])
            y += rng.choice([-1, 0, 1])

    # Carve a village area in the center
    vx0, vy0 = w//2 - 4, h//2 - 4
    for y in range(vy0, vy0+8):
        for x in range(vx0, vx0+8):
            tiles[y][x] = VILLAGE

    # Paths leading out
    for x in range(vx0-10, vx0+18):
        if 0 <= x < w:
            tiles[vy0+4][x] = PATH
    for y in range(vy0-12, vy0+16):
        if 0 <= y < h:
            tiles[y][vx0+4] = PATH

    return tiles, (vx0+4, vy0+4)

tiles, village_center = make_world(MAP_W, MAP_H)

# Collision: which tiles block movement?
def blocks(t):
    return t in (WATER, ROCK, TREE)

# -----------------------------
# Entities
# -----------------------------
class Entity:
    def __init__(self, x, y):
        self.x = x*1.0
        self.y = y*1.0
        self.r = 12
        self.vx = 0
        self.vy = 0

    @property
    def pos(self):
        return (self.x, self.y)

    def tile_pos(self):
        return int(self.x // TILE), int(self.y // TILE)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.max_stam = PLAYER_MAX_STAM
        self.stam = self.max_stam
        self.facing = (1, 0)
        self.last_attack = -999
        self.inv = {"Moonherb": 0, "Wolf Pelt": 0}
        self.quest = None
        self.quest_complete = False

    def update(self, dt, keys):
        # Movement
        mx = (keys[pygame.K_d] - keys[pygame.K_a])
        my = (keys[pygame.K_s] - keys[pygame.K_w])
        mag = math.hypot(mx, my)
        if mag > 0:
            mx, my = mx/mag, my/mag
            self.facing = (mx, my)

        speed = PLAYER_SPEED
        sprinting = False
        if keys[pygame.K_LSHIFT] and self.stam > 0.5 and mag > 0:
            speed = PLAYER_SPRINT
            sprinting = True

        dx = mx * speed * dt
        dy = my * speed * dt

        self.move_and_collide(dx, dy)

        # Stamina
        if sprinting:
            self.stam = max(0, self.stam - STAMINA_DRAIN * dt * FPS)
        else:
            self.stam = min(self.max_stam, self.stam + STAMINA_REGEN * dt * FPS)

    def move_and_collide(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        # Horizontal
        if not solid_at(nx, self.y, self.r):
            self.x = nx
        else:
            # slide along walls
            if not solid_at(self.x, self.y + dy, self.r):
                self.y += dy
        # Vertical
        if not solid_at(self.x, self.y + dy, self.r):
            self.y += dy

    def can_attack(self, t):
        return (t - self.last_attack) >= ATTACK_COOLDOWN

class Wolf(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_hp = WOLF_HP
        self.hp = self.max_hp
        self.home = (x, y)
        self.aggro = False
        self.dead = False
        self.respawn_timer = 0

    def update(self, dt, player):
        if self.dead:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.dead = False
                self.hp = self.max_hp
            return

        px, py = player.pos
        dx, dy = px - self.x, py - self.y
        dist = math.hypot(dx, dy)

        if dist < WOLF_CHASE_RANGE:
            self.aggro = True
        if dist > WOLF_LEASH:
            self.aggro = False

        if self.aggro:
            if dist > 0:
                dx /= dist; dy /= dist
            sp = WOLF_SPEED
            self.try_move(dx * sp * dt, dy * sp * dt)
        else:
            # wander a bit
            if random.random() < 0.01:
                self.vx = random.uniform(-0.7, 0.7)
                self.vy = random.uniform(-0.7, 0.7)
            self.try_move(self.vx * dt, self.vy * dt)

    def try_move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if not solid_at(nx, self.y, self.r): self.x = nx
        if not solid_at(self.x, ny, self.r): self.y = ny

# -----------------------------
# Helpers
# -----------------------------
def solid_at(x, y, radius):
    # sample 4 points around entity
    points = [
        (x - radius, y),
        (x + radius, y),
        (x, y - radius),
        (x, y + radius),
    ]
    for px, py in points:
        tx, ty = int(px // TILE), int(py // TILE)
        if tx < 0 or ty < 0 or tx >= MAP_W or ty >= MAP_H:
            return True
        if blocks(tiles[ty][tx]):
            return True
    return False

def tile_color(t):
    return {
        GRASS: COL_GRASS,
        WATER: COL_WATER,
        ROCK: COL_ROCK,
        TREE: COL_TREE,
        PATH: COL_PATH,
        VILLAGE: (120, 90, 60),
    }[t]

def draw_world(surface, camx, camy, vw, vh):
    # Draw only visible tiles
    x0 = int(camx // TILE)
    y0 = int(camy // TILE)
    cols = vw // TILE + 3
    rows = vh // TILE + 3
    for ty in range(y0, y0 + rows):
        if 0 <= ty < MAP_H:
            for tx in range(x0, x0 + cols):
                if 0 <= tx < MAP_W:
                    rect = pygame.Rect(tx*TILE - camx, ty*TILE - camy, TILE, TILE)
                    t = tiles[ty][tx]
                    pygame.draw.rect(surface, tile_color(t), rect)
                    if t == TREE:
                        pygame.draw.rect(surface, (16, 50, 22), rect.inflate(-14, -14))
                    if t == ROCK:
                        pygame.draw.rect(surface, (130, 130, 145), rect.inflate(-18, -18))
                    if t == WATER:
                        pygame.draw.rect(surface, (50, 120, 180), rect.inflate(-12, -12))

def circle(surface, color, pos, radius, width=0):
    pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), radius, width)

def angle_between(a, b):
    return math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))

# -----------------------------
# NPCs, Items, Quest
# -----------------------------
class NPC:
    def __init__(self, x, y, name, lines):
        self.x = x*TILE + TILE//2
        self.y = y*TILE + TILE//2
        self.name = name
        self.lines = lines
        self.r = 13

    def draw(self, surf, camx, camy):
        circle(surf, COL_NPC, (self.x - camx, self.y - camy), self.r)
        label = base_font.render(self.name, True, COL_TEXT)
        surf.blit(label, (self.x - camx - label.get_width()//2, self.y - camy - 28))

    def near(self, player):
        return math.hypot(player.x - self.x, player.y - self.y) < 48

class Herb:
    def __init__(self, x, y):
        self.x = x*TILE + TILE//2
        self.y = y*TILE + TILE//2
        self.r = 8
        self.taken = False

    def draw(self, surf, camx, camy):
        if not self.taken:
            pygame.draw.circle(surf, COL_HERB, (int(self.x - camx), int(self.y - camy)), self.r)
            pygame.draw.circle(surf, (40, 120, 70), (int(self.x - camx), int(self.y - camy)), self.r, 2)

    def try_pick(self, player):
        if not self.taken and math.hypot(player.x - self.x, player.y - self.y) < 28:
            self.taken = True
            player.inv["Moonherb"] += 1
            return True
        return False

# place NPC Elder in village center
elder = NPC(village_center[0], village_center[1], "Elder", [
    "Welcome to Wyrmvale.",
    "Our healers need Moonherbs.",
    "Bring me 3 Moonherbs from the wild.",
    "Return safely, child."
])

# Scatter herbs on grass near but outside the village
herbs = []
rngh = random.Random(99)
while len(herbs) < HERB_COUNT:
    tx, ty = rngh.randrange(MAP_W), rngh.randrange(MAP_H)
    if tiles[ty][tx] == GRASS and math.hypot(tx - village_center[0], ty - village_center[1]) > 7:
        herbs.append(Herb(tx, ty))

# Wolves: roam around forests
wolves = []
rngw = random.Random(7)
for _ in range(10):
    tx, ty = rngw.randrange(MAP_W), rngw.randrange(MAP_H)
    if tiles[ty][tx] in (GRASS, PATH) and math.hypot(tx - village_center[0], ty - village_center[1]) > 8:
        wolves.append(Wolf(tx*TILE + TILE//2, ty*TILE + TILE//2))

# Player spawn at village
player = Player(village_center[0]*TILE + TILE//2, village_center[1]*TILE + TILE//2)

# -----------------------------
# UI
# -----------------------------
def draw_bar(surf, x, y, w, h, frac, col_fg, col_bg=(40,40,48)):
    pygame.draw.rect(surf, col_bg, (x, y, w, h), border_radius=4)
    inner = max(0, int(w * max(0.0, min(1.0, frac))))
    pygame.draw.rect(surf, col_fg, (x, y, inner, h), border_radius=4)

def draw_inventory_panel(surf):
    panel = pygame.Surface((260, 140), pygame.SRCALPHA)
    panel.fill((*COL_PANEL, 220))
    surf.blit(panel, (12, 80))
    title = big_font.render("Inventory", True, COL_ACCENT)
    surf.blit(title, (24, 86))
    y = 120
    for k, v in player.inv.items():
        line = base_font.render(f"{k}: {v}", True, COL_TEXT)
        surf.blit(line, (24, y)); y += 22

def draw_help_panel(surf):
    lines = [
        "WASD: Move   SHIFT: Sprint   SPACE: Attack",
        "E: Interact/Talk   I: Inventory   H: Help",
        "Goal: Talk to Elder, gather 3 Moonherbs, return.",
        "Avoid wolves or fight them—watch your stamina!",
    ]
    panel = pygame.Surface((540, 120), pygame.SRCALPHA)
    panel.fill((*COL_PANEL, 220))
    surf.blit(panel, (12, 240))
    y = 252
    for s in lines:
        surf.blit(base_font.render(s, True, COL_TEXT), (24, y)); y += 22

def draw_dialog(surf, speaker, lines):
    panel = pygame.Surface((screen.get_width()-40, 140), pygame.SRCALPHA)
    panel.fill((*COL_PANEL, 230))
    surf.blit(panel, (20, screen.get_height()-160))
    surf.blit(big_font.render(speaker, True, COL_ACCENT), (36, screen.get_height()-152))
    y = screen.get_height()-122
    for l in lines[:4]:
        surf.blit(base_font.render(l, True, COL_TEXT), (36, y)); y += 22
    surf.blit(base_font.render("Press E to continue/close", True, (180,180,190)), (36, y+6))

# -----------------------------
# Combat helpers
# -----------------------------
def attack_cone(player, target):
    # Is target within arc and range?
    px, py = player.pos
    tx, ty = target.x, target.y
    dist = math.hypot(tx - px, ty - py)
    if dist > ATTACK_RANGE + target.r:
        return False
    facing = player.facing
    a0 = math.degrees(math.atan2(facing[1], facing[0]))
    a1 = math.degrees(math.atan2(ty - py, tx - px))
    da = (a1 - a0 + 540) % 360 - 180
    return abs(da) <= ATTACK_ARC_DEG

def draw_slash(surf, camx, camy, when, now, origin, facing):
    t = now - when
    if 0 <= t <= ATTACK_COOLDOWN:
        # simple arc wedge
        ox, oy = origin
        ox -= camx; oy -= camy
        steps = 16
        radius = ATTACK_RANGE
        base_ang = math.degrees(math.atan2(facing[1], facing[0]))
        spread = ATTACK_ARC_DEG
        pts = [(ox, oy)]
        for i in range(steps+1):
            ang = math.radians(base_ang - spread + (2*spread)*i/steps)
            pts.append((ox + math.cos(ang)*radius, oy + math.sin(ang)*radius))
        pygame.draw.polygon(surf, (*COL_SLASH, 120), pts)

# -----------------------------
# Game Loop
# -----------------------------
show_inv = False
show_help = True
dialog_active = False
dialog_lines = []
quest_given = False

def within_world(px, py):
    return 0 <= px < MAP_W*TILE and 0 <= py < MAP_H*TILE

def handle_attack(now):
    hit_any = False
    for w in wolves:
        if not w.dead and attack_cone(player, w):
            w.hp -= ATTACK_DAMAGE
            hit_any = True
            if w.hp <= 0:
                w.dead = True
                w.respawn_timer = WOLF_RESPAWN_SEC
                # loot drop
                if random.random() < 0.8:
                    player.inv["Wolf Pelt"] += 1
    # minor stamina cost even if swing misses
    player.stam = max(0, player.stam - 12)
    return hit_any

def update_camera():
    vw, vh = screen.get_width(), screen.get_height()
    camx = max(0, min(int(player.x - vw//2), MAP_W*TILE - vw))
    camy = max(0, min(int(player.y - vh//2), MAP_H*TILE - vh))
    return camx, camy

def draw_minimap(surf):
    mw, mh = 180, 180
    mini = pygame.Surface((mw, mh))
    mini.fill((20, 22, 28))
    sx = mw / MAP_W
    sy = mh / MAP_H
    for y in range(MAP_H):
        for x in range(MAP_W):
            c = tile_color(tiles[y][x])
            mini.fill(c, (int(x*sx), int(y*sy), int(math.ceil(sx)), int(math.ceil(sy))))
    # player & elder
    pygame.draw.circle(mini, COL_PLAYER, (int(player.x/TILE*sx), int(player.y/TILE*sy)), 3)
    pygame.draw.circle(mini, (240,200,120), (int(elder.x/TILE*sx), int(elder.y/TILE*sy)), 3)
    surf.blit(mini, (screen.get_width()-mw-12, 12))
    pygame.draw.rect(surf, (255,255,255), (screen.get_width()-mw-12, 12, mw, mh), 2)

def main():
    global show_inv, show_help, dialog_active, dialog_lines, quest_given

    running = True
    last_time = pygame.time.get_ticks() / 1000.0

    while running:
        now = pygame.time.get_ticks() / 1000.0
        dt = now - last_time
        last_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_i:
                    show_inv = not show_inv
                if event.key == pygame.K_h:
                    show_help = not show_help
                if event.key == pygame.K_SPACE:
                    if player.can_attack(now):
                        player.last_attack = now
                        handle_attack(now)
                if event.key == pygame.K_e:
                    # Interact: talk to elder or advance dialog
                    if dialog_active:
                        dialog_active = False
                        # complete quest check
                        if player.quest and player.inv["Moonherb"] >= 3 and not player.quest_complete and elder.near(player):
                            player.quest_complete = True
                            player.inv["Moonherb"] -= 3
                            player.max_hp += 20
                            player.hp = min(player.max_hp, player.hp + 40)
                            dialog_active = True
                            dialog_lines = [
                                "These herbs will help the healers.",
                                "You have our gratitude.",
                                "Take this blessing. May your vitality grow."
                            ]
                    else:
                        if elder.near(player):
                            if not quest_given:
                                player.quest = "Gather 3 Moonherbs"
                                quest_given = True
                                dialog_active = True
                                dialog_lines = [
                                    "Greetings. We need Moonherbs to heal the sick.",
                                    "Find 3 in the wild and bring them to me.",
                                    "You will be rewarded."
                                ]
                            else:
                                # Repeat or completion hint
                                if player.quest_complete:
                                    dialog_active = True
                                    dialog_lines = [
                                        "You’ve done well. Rest now.",
                                        "The valley owes you a debt."
                                    ]
                                else:
                                    dialog_active = True
                                    have = player.inv["Moonherb"]
                                    dialog_lines = [
                                        f"You have {have}/3 Moonherbs.",
                                        "Search the wild glades near the village.",
                                        "Return when you have enough."
                                    ]

        keys = pygame.key.get_pressed()

        # Update
        player.update(dt*60, keys)  # scaled for feel
        player.x = max(16, min(player.x, MAP_W*TILE-16))
        player.y = max(16, min(player.y, MAP_H*TILE-16))

        # Pick herbs
        for h in herbs:
            if not h.taken:
                h.try_pick(player)

        # Wolves update + damage if close
        for w in wolves:
            w.update(dt*60, player)
            if not w.dead and math.hypot(player.x - w.x, player.y - w.y) < (w.r + player.r + 4):
                # small knock + damage
                player.hp -= WOLF_DAMAGE * dt  # damage over time on contact
                # nudge player away
                dx, dy = player.x - w.x, player.y - w.y
                d = math.hypot(dx, dy) or 1
                player.x += (dx/d) * 0.8
                player.y += (dy/d) * 0.8
                player.x = max(16, min(player.x, MAP_W*TILE-16))
                player.y = max(16, min(player.y, MAP_H*TILE-16))

        # Death? Soft respawn at village
        if player.hp <= 0:
            player.hp = player.max_hp
            player.stam = player.max_stam
            player.x = village_center[0]*TILE + TILE//2
            player.y = village_center[1]*TILE + TILE//2

        # Draw
        screen.fill(COL_BG)
        camx, camy = update_camera()
        vw, vh = screen.get_width(), screen.get_height()

        draw_world(screen, camx, camy, vw, vh)

        # Herbs
        for h in herbs:
            h.draw(screen, camx, camy)

        # Elder
        elder.draw(screen, camx, camy)

        # Wolves
        for w in wolves:
            if not w.dead:
                circle(screen, COL_WOLF, (w.x - camx, w.y - camy), w.r)
                # hp bar
                frac = max(0, w.hp / w.max_hp)
                pygame.draw.rect(screen, (20,20,20), (w.x - camx - 16, w.y - camy - 22, 32, 5))
                pygame.draw.rect(screen, COL_HP, (w.x - camx - 16, w.y - camy - 22, 32*frac, 5))

        # Player
        circle(screen, COL_PLAYER, (player.x - camx, player.y - camy), player.r, 2)
        # Facing dot
        fx = player.x + player.facing[0]*10
        fy = player.y + player.facing[1]*10
        circle(screen, COL_PLAYER, (fx - camx, fy - camy), 3)

        # Recent slash
        draw_slash(screen, camx, camy, player.last_attack, now, (player.x, player.y), player.facing)

        # UI
        # HP and Stamina bars
        draw_bar(screen, 12, 12, 240, 16, player.hp/player.max_hp, COL_HP)
        screen.blit(base_font.render(f"HP {int(player.hp)}/{player.max_hp}", True, (0,0,0)), (18, 12))
        draw_bar(screen, 12, 34, 240, 12, player.stam/player.max_stAM if hasattr(player, 'max_stAM') else player.stam/player.max_stam, COL_STAM)
        screen.blit(base_font.render(f"ST {int(player.stam)}/{player.max_stam}", True, (0,0,0)), (18, 32))

        # Quest
        q = "Quest: " + (player.quest if player.quest else "Speak to the Elder")
        if player.quest_complete:
            q = "Quest: Completed – return to Elder (or explore!)"
        screen.blit(base_font.render(q, True, COL_TEXT), (12, 56))

        # Minimap
        draw_minimap(screen)

        # Panels
        if show_inv: draw_inventory_panel(screen)
        if show_help: draw_help_panel(screen)
        if dialog_active:
            draw_dialog(screen, elder.name, dialog_lines)

        # Interaction hint
        if elder.near(player) and not dialog_active:
            tip = base_font.render("Press E to talk", True, COL_ACCENT)
            screen.blit(tip, (int(elder.x - camx - tip.get_width()//2), int(elder.y - camy - 46)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()

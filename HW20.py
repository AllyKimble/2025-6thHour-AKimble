#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW20

#1. Create a class containing a def function that inits self and 3 other attributes for store items (stock, cost, and weight).

class StoreItem:
    def __init__(self, stock, cost, weight):
        self.stock = stock
        self.cost = cost
        self.weight = weight

    def double_cost(self):
        self.cost = self.cost * 2


#2. Make 3 objects to serve as your store items and give them values to those 3 attributes defined in the class.

Taco = StoreItem(stock = 10, cost = 10.00, weight = 10)
Turtle = StoreItem(stock = 50, cost = 50.00, weight = 50)
TNT = StoreItem(stock = 100, cost = 100.00, weight = 100)

#3. Print the stock of all three objects and the cost of the second store item.

print("Stock of Taco: ", Taco.stock)
print("Stock of Turtle: ", Turtle.stock)
print("Stock of TNT: ", TNT.stock)

print("Cost of Turtle: ", Turtle.cost)

#4. Make a def function within the class that doubles the cost an item, double the cost of the second store item, and print the new cost below the original cost print statement.

Turtle.double_cost()
print("Doubled cost of Turtle: ", Turtle.cost)

#5. Directly change the stock of the third store item to approx. 1/4th the original stock and then print the new stock amount.

TNT.stock = TNT.stock / 4
TNT.stock = round(TNT.stock)
print("New TNT stock:" , TNT.stock)

#6. Delete the first store item and then attempt to print the weight of the first store item. Create a try/except catch to fix the error.

del Taco

try:
    print("Weight of Taco: ", Taco.weight)
except NameError:
    print("Error. Taco no longer exists.")
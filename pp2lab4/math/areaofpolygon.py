import math

n_sides = int(input("Input number of sides: "))
length = float(input("Input the length of a side: "))

area = (n_sides * (length ** 2)) / (4 * math.tan(math.pi / n_sides))

print(f"The area of the polygon is: {int(area) if area.is_integer() else area}")
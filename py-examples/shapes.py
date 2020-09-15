import numpy as np
import math


class Shape():
    def __init__(self):
        self.__name = "Shape"

    def perimeter(self):
        return "I am an undefined shape"

    def surface(self):
        return "I am an undefined shape"

    def whatAmI(self):
        print("I am a", self.__name)




class Rectangle(Shape):
    def __init__(self, sides):
        self.__name = "Rectangle"
        self.__sides = sides

    def whatAmI(self):
        print("I am a", self.__name)

    def perimeter(self):
        return sum(self.__sides) * 2

    def surface(self):
        return self.__side[0] * self.__side[1]


class Square(Rectangle):
    def __init__(self, side):
        self.__name = "Square"
        self.__side = side

    def whatAmI(self):
        print("I am a", self.__name)

    def perimeter(self):
        return 4 * self.__side

    def surface(self):
        return self.__side ** 2


class Circle(Shape):
    def __init__(self, radius):
        self.__name = "Circle"
        self.__radius = radius

    def whatAmI(self):
        print("I am a", self.__name)

    def perimeter(self):
        return 2 * self.__radius * math.pi

    def surface(self):
        return math.pi * self.__radius ** 2


class Polygon(Shape):
    def __init__(self, edges):
        self.__name = "Polygon"
        self.__edges = edges

    def whatAmI(self):
        print("I am a", self.__name)

    def perimeter(self):
        return sum(self.__edges)

    def surface(self):
        return "I don't know :("


class Triangle(Shape):
    def __init__(self, sides):
        self.__name = "Triangle"
        self.__radius = sides

    def whatAmI(self):
        print("I am a", self.__name)

    def perimeter(self):
        return sum(self.__sides)

    def surface(self):
        return "I don't know :("


# TODO: implement a main function
t = Triangle(8)
t.whatAmI()
print(f"My perimeter: {t.perimeter()}")
print(f"My surface area: {t.surface()}")

p = Polygon([3, 5, 3, 6])
p.whatAmI()
print(f"My perimeter: {p.perimeter()}")
print(f"My surface area: {p.surface()}")
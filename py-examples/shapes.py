import numpy as np
import math


class Shape():
    def __init__(self, _name="Shape"):
        self.set_name(_name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        """Setter for the instance variable name"""
        self._name = name

    def perimeter(self):
        """Define common interface for all Shapes"""
        pass

    def surface(self):
        """Define common interface for all Shapes"""
        pass



class Rectangle(Shape):
    def __init__(self, _name="Rectangle", _sides=[]):
        """Initializer"""
        self.name = _name
        self.set_sides(_sides)

    def set_sides(self, _sides):
        """Setter for instance variable sides"""
        if len(_sides) != 2:
            raise ValueError("Please specify only 2 sides (L+W)")
        self._sides = _sides

    def perimeter(self):
        return sum(self._sides) * 2

    def surface(self):
        return self._side[0] * self._side[1]


class Square(Rectangle):
    def __init__(self, _name="Square", _side=1.0):
        self.name = _name
        self.set_side(_side)

    def set_side(self, _side):
        """Setter for instance variable side"""
        self._side = _side

    def perimeter(self):
        return 4 * self._side

    def surface(self):
        return self._side ** 2


class Circle(Shape):
    def __init__(self, _name="Circle", _radius=1.0):
        """Initializer with default radius"""
        self.name = _name
        self.radius = _radius

    @property
    def radius(self):
        """Getter for instance variable radius"""
        return self._radius

    @radius.setter
    def radius(self, radius):
        """Setter for instance variable radius"""
        if radius < 0:
            raise ValueError('Radius cannot be negative')
        self._radius = radius

    # A method which can be accessed via str() or print()
    def __str__(self):
        return f"This is a Circle with a radius of {self._radius}"

    def perimeter(self):
        """Return the perimeter of this Circle instance"""
        return 2 * self._radius * math.pi

    def surface(self):
        """Return the area of this Circle instance"""
        return math.pi * self._radius ** 2


class Polygon(Shape):
    def __init__(self, _name="Polygon", _edges=[]):
        self.name = _name
        self.set_edges(_edges)

    def set_edges(self, _edges):
        """Setter for the instance variable edges"""
        if len(_edges) < 3:
            raise ValueError("Polygon must have at least 3 sides!")
        self._edges = _edges

    def get_edges(self):
        """Getter for the instance variable edges"""
        return self._edges

    # A method which can be accessed via str() or print()
    def __str__(self):
        return f"This is a Polygon with edges: {self._edges}"

    def perimeter(self):
        return sum(self._edges)

    def surface(self):
        return "I don't know :("


class Triangle(Shape):
    def __init__(self, _name="Triangle", _sides=[]):
        self.name = _name
        self.set_sides(_sides)

    def set_sides(self, _sides):
        """Setter for the instance variable sides"""
        if len(_sides) != 3:
            raise ValueError("Triangle must have exactly 3 sides!")
        self._sides = _sides

    def get_sides(self):
        """Getter for the instance variable sides"""
        return self._sides

    # A method which can be accessed via str() or print()
    def __str__(self):
        return f"This is a Triangle with sides: {self._sides}"

    def perimeter(self):
        return sum(self._sides)

    def surface(self):
        return "I don't know :("


# TODO: implement a main function
t = Triangle(_sides=[8, 6, 4])
print(t)
print(f"My perimeter: {t.perimeter()}")
print(f"My surface area: {t.surface()}")

p = Polygon(_edges=[3, 5, 3, 6])
print(p)
print(f"My perimeter: {p.perimeter()}")
print(f"My surface area: {p.surface()}")

c = Circle(_radius=2.5)
print(c)

# Example: confirming class type/inheritance
# check the types of the developed classes
print(f"Triangle is Shape: {isinstance(t, Shape)}")
print(f"Triangle is Triangle: {isinstance(t, Triangle)}")

# N.B. these checks look at the Classes, not the instances!
print(f"Triangle is subclass of Shape: {issubclass(Triangle, Shape)}")
print(f"Shape is subclass of Triangle: {issubclass(Shape, Triangle)}")
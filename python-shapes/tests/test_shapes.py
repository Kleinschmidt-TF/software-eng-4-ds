import sys
import model.shapes as shapes

test_epsilon = 0.01

# sys.path.append("C:/Repos/python-shapes/model/")


def test_square():
    assert shapes.Square(2).area() == 4
    assert shapes.Square(2).perimeter() == 8
    assert shapes.Square(3).perimeter() != 9


def test_rectangle():
    assert shapes.Rectangle(2, 4).area() == 8
    assert shapes.Rectangle(2, 4).perimeter() == 12


def test_circle():
    assert abs(shapes.Circle(2).area() - 12.56) < test_epsilon
    assert abs(shapes.Circle(2).perimeter() - 12.56) < test_epsilon


def test_cube():
    assert shapes.Cube(3).volume() == 27
    assert shapes.Cube(3).area() == 54


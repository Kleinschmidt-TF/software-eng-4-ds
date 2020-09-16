import sys
import model.shapes as shapes

sys.path.append("/Users/saxen/Documents/GitHub/python-shapes/model/")

def test_square():
    assert shapes.Square(2).area() is 4
    assert shapes.Square(2).perimeter() is 8

#python -m pytest shapes.py

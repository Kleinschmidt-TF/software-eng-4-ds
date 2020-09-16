import model.shapes as shapes

def test_shapes():
    assert shapes.Square(2).area() is 4
    assert shapes.Square(2).perimeter() is 8

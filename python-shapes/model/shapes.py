from abc import ABCMeta, abstractmethod
from render import cube as cube_render

class Shape(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def render(self):
        pass

class Shape2D(metaclass=ABCMeta):

    @abstractmethod
    def perimeter(self):
        pass

    def inc_size(self):
        pass

    def dec_size(self):
        pass

class Shape3D(Shape):
    @abstractmethod
    def volume(self):
        pass

class Square(Shape2D):
    def __init__(self, side: int):
        self.name = "Square"
        self._side = side

    def perimeter(self)->int:
        return self._side*4

    def area(self):
        return self._side*self._side

    @property
    def side(self):
        return self._side

    @side.setter
    def name(self, side:int):
        self._side = side

class Rectangle(Shape2D):
    def __init__(self, length: int,width: int):
        self.name = "Rectangle"
        self._length = length
        self._width = width

    def perimeter(self)->int:
        return (self._length+self._width)*2

    def area(self)->int:
        return self._length*self._width

    @property
    def side(self):
        return self._side

    @side.setter
    def name(self, side:int):
        self._side = side

class Polygon(Shape2D):
    def __init__(self, nsegment):
        self.name = "polygon"
        self.__nsegment = nsegment

    @property
    def nsegment(self):
        return self.__nsegment

    @nsegment.setter
    def nsegment(self, nsegment):
        self.__nsegment = nsegment

class Cube(Shape3D):

    def __init__(self, side: int):
        self.name = "Cube"
        self._side = side

    def volume(self)->int:
        return self._side * self._side * self._side

    def area(self)->int:
        return self._side*self._side*4

    @property
    def side(self):
        return self._side

    @side.setter
    def name(self, side:int):
        self._side = side

    def render(self):
        cube_render.render_cube()

def test():
    #sh = Shape("circle")
    #p = Polygon(3)
    #p.name = "poly"

    #print(sh.name)
    #print(p.name)
    cube = Cube(10)
    print(cube.area())
    print(cube.volume())
    cube.render()

def main():
    test()

if __name__ == "__main__":
    main()






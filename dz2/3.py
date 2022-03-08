from math import pi


class Cylinder:
    def __init__(self, diametr, high):
        self.dia = diametr
        self.h = high
        self.__area = self.make_area(diametr, high)
 
    @staticmethod
    def make_area(d, h):
        circle = pi * d ** 2 / 4
        side = pi * d * h
        return round(circle * 2 + side, 2)
 
    def __setattr__(self, attr, value):
        if attr == '_Cylinder__area':
            self.__dict__[attr] = value
        
        if attr == 'area':
            print(f"value cannot be assigned field: '{attr}'")

        if attr in ['dia', 'h']:
            self.__dict__[attr] = value
            if self.__area is not None:
                self.__area = self.make_area(self.dia, self.h)

    def __getattr__(self, attr):
        if attr == 'area':
            return self.__area


def main():
    a = Cylinder(1, 2)
    print(a.area)

    a.dia = 2
    print(a.area)
    print(a.make_area(2, 2))

    a.h = 3
    print(a.area)
    print(a.make_area(2, 3)) 

    a.dia = 4
    a.h = 4 
    print(a.area)
    print(a.make_area(4, 4))

    a.area = 120
    print(a.area)


if __name__ == '__main__':
    main()
    
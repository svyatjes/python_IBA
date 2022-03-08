class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, sec_dot):
        x = self.x + sec_dot.x
        y = self.y + sec_dot.y
        return Dot(x, y)

def main():
    a = Dot(2, 3)
    b = Dot(4, 1)
    c = a + b 
    print(c)


if __name__ == '__main__':
    main()
    
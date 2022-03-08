class CheckStr(str):
    def __init__(self, string):
        self.string = string

    def is_repeatance(self, s):
        is_str = isinstance(s, str)
        is_empty = True if is_str and len(s) == 0 else False

        if not is_str or is_empty:
            return False
        
        n = len(self.string) // len(s)
        return self.string == s * n

    def is_palindrom(self):
        if len(self.string) == 0:
            return True

        s = self.lower().replace(' ', '')
        return s == s[::-1]


def main():
    s1 = CheckStr('abccdabccdabccd')
    print(s1.is_repeatance('abccd'))
    print(s1.is_repeatance('abcc'))
    print(s1.is_repeatance(''))
    print(s1.is_repeatance(1234))


    s = CheckStr('радар')
    print(s.is_palindrom())

    s2 = CheckStr('а роза упала на лапу азора')
    print(s2.is_palindrom())

    s3 = CheckStr('')
    print(s3.is_palindrom())

    s4 = CheckStr('milk')
    print(s4.is_palindrom())


if __name__ == '__main__':
    main()

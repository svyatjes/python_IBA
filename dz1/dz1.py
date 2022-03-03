def main():
    message = input()
    msg_len = len(message)
    SPACE = 12

    print(SPACE * ' ', msg_len * '_')
    print((SPACE - 2) * ' ', f'< {message} >')
    print(SPACE * ' ', msg_len * '-')
    print((SPACE - 2) * ' ', '/')
    print(r' /\_/\    /')
    print('( o.o )')
    print(' > ^ <')


if __name__ == '__main__':
    main()

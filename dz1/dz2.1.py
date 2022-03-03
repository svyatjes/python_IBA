def main():
    products = []
    while True:
        product = input()
        if product == '':
            break
        else:
            products.append(product)

    print("list of products:\n{}".format('\n'.join(products)))


if __name__ == '__main__':
    main()

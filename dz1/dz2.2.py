products = {}

def write_products(name):
    name_products = products.keys()
    if name in name_products:
        products[name] = products[name] + 1
    else:
        products[name] = 1


def del_product():
    values = list(products.values())
    max_count = max(values)
    index_max_count = values.index(max_count)

    keys = list(products.keys())
    key_of_max_count = keys[index_max_count]

    print(f'DELETE product: {key_of_max_count}\n')
    del products[key_of_max_count]


def main():
    
    while True:
        product = input()
        if product == '':
            break
        else:
            write_products(product.lower())

    del_product()

    for key in products:
        print(f'product: {key}  |  count: {products[key]}')


if __name__ == '__main__':
    main()

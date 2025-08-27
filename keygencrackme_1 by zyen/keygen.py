def keygen(name: str) -> int:
    L = len(name)
    return L*L * 10

def main():
    name = input('Nombre: ')
    print(keygen(name))

if __name__ == '__main__':
    main()
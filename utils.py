import json

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def main():
    a = load_json('14_06_2022.json')
    for i in a.keys(): # i fecha de adquisicion
        for j in a[i].keys(): # j tipo de opcion/futuro
            if j != 'FUTURO':
                for k in a[i][j].keys(): #dates de opciones
                    print(i, j, k, a[i][j][k])
                    for l in a[i][j][k].keys(): #Typos de strike, volatilidad, price
                        print(i, j, k, l, a[i][j][k][l])
    return 0


if __name__ == '__main__':
    main()
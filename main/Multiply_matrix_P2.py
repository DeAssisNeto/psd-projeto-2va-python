from multiprocessing import Process, Queue
from datetime import datetime

matOne = [
    [1, 4],
    [2, 5],
    [3, 6]
]
matTwo = [
    [1, 3],
    [2, 4],
]

matThree = [
    [5, 8, -4],
    [6, 9, -5],
    [4, 7, -2]
]

matFour = [
    [2],
    [-3],
    [1]
]

def get_colun(num, mat1):
    return [i for i in mat1[num]]

def get_line(num, mat2):
    return [i[num] for i in mat2]

def multiply_l_c(line, colun, cont, q, j, i):
    mult = 0
    inicio = datetime.now().strftime("%H:%M:%S.%f")
    print(f"Processo {cont}: Inicio: {inicio}" )

    for k in range(len(line)):
        mult += line[k] * colun[k]

    fim = datetime.now().strftime("%H:%M:%S.%f")
    print(f"Processo {cont}: Fim: {fim}" )

    q.put((j, i, mult))


def multiply(mat1, mat2):
    if len(mat1[0]) != len(mat2):
        raise Exception(
            f"O numero de colunas do parametro mat1"
            f" ({len(mat1[0])}) tem que ser igual do numero "
            f"de linhas so parametro mat2 ({len(mat2)})")


    mat_ret = []
    cont = 0
    for i in range(len(mat1)):
        mat_ret.append([0] * len(mat2[0]))
    print(mat_ret)
    
    # [1][2] [1][2]
    # [3][4] [3][4]
    # Dividir matriz em 4 por exemplo, então uma matriz 4 x 4
    # Processo 1 [1][1]+[1][3]
    # Processo 2 [2][2]+[2][4] 
    # Processo 3 [3][1]+[3][3]
    # Processo 4 [4][2]+[4][4]

    lines, coluns = get_lines_and_coluns(mat1, mat2) # divisão das matrizes de entrada
                                                     # lines representa as linhas do parametro mat1
                                                     # coluns representa as colunas do parametro mat2

    n = len(coluns)  # número de colunas
    m = len(lines)  # número de linhas

    # Inicializando a fila para receber os resultados
    q = Queue()
    mat_ret = [[0 for _ in range(n)] for _ in range(m)]
    # Ainda não aplicado!

    for i in range(len(mat_ret[0])):
        for j in range(len(mat_ret)):
            cont = f'({j},{i})'
            process = Process(target=multiply_l_c, args=(coluns[i], lines[j], cont, q, j, i))
            # Resultado esta saindo o processo, ajustar para que cada processo mande o valor para outra matriz ou outra coisa
            process.start()
            print(mat_ret[j][i])

    for _ in range(n * m):
        j, i, result = q.get()
        mat_ret[j][i] = result

    return mat_ret


def txt_to_mat(file_name):
    list_ret = []
    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            list_ret.append(line.split())

    for i in range(len(list_ret)):
        for j in range(len(list_ret[i])):
            list_ret[i][j] = float(list_ret[i][j])
    return list_ret[1:], list_ret[0]

def get_lines_and_coluns(mat1, mat2):
    lines_mat1 = []
    coluns_mat2 = []

    for i in range(len(mat1)):
        lines_mat1.append(mat1[i])

    for i in range(len(mat2[0])):
        coluns_mat2.append(get_line(i, mat2))

    return lines_mat1, coluns_mat2

if __name__ == "__main__":
    #matFive = txt_to_mat('ex1')[0]
    #matSix = txt_to_mat('ex2')[0]
    #matSeven = txt_to_mat('ex3')[0]

    print( f'mat3 x mat4z\n - {multiply(txt_to_mat("ex2")[0], txt_to_mat("ex2")[0])} -')
    #print(multiply(matOne, matTwo))
    #print(multiply(matSix, matSix))
    lines, coluns = get_lines_and_coluns(matOne, matTwo)
    print(lines)
    print(coluns)

    print(f"Variações de P1, P2, P3, P4 e P5: {0}")
    print(f"Computadores Remotos: {0}")
    print(f"Numero de Linhas Matriz: {0}")
    print(f"Numero de Colunas Matriz: {0}")
    print(f"Tempo de Processamento: {0}")    
    print("")
    print(f"Matriz Gerada: {0}")


from multiprocessing import cpu_count
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


def get_line(num, mat):
    return [line for line in mat[num]]


def get_colun(num, mat):
    return [row[num] for row in mat]


def multiply_l_c(line, colun, cont):
    mult = 0
    for i in range(len(line)):
        mult += line[i] * colun[i]
    return mult


def multiply(mat1, mat2):
    if len(mat1[0]) != len(mat2):
        raise Exception(
            f"O numero de colunas do parametro mat1"
            f" ({len(mat1[0])}) tem que ser igual do numero "
            f"de linhas so parametro mat2 ({len(mat2)})")
    mat_ret = []
    num_cores = cpu_count()
    cont = 0
    for i in range(len(mat1)):
        mat_ret.append([0] * len(mat2[0]))

    lines, coluns = get_lines_and_coluns(mat1, mat2)  # divisão das matrizes de entrada

    inicio_total = datetime.now()
    for i in range(len(mat_ret[0])):
        for j in range(len(mat_ret)):
            cont += 1
            mat_ret[i][j] = (multiply_l_c(lines[i], coluns[j], cont))

    fim_total = datetime.now()
    time_total = fim_total - inicio_total


    return mat_ret, num_cores, time_total


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

    for line in mat1:
        lines_mat1.append(line)

    for i in range(len(mat2[0])):
        coluns_mat2.append(get_colun(i, mat2))

    return lines_mat1, coluns_mat2


if __name__ == "__main__":
    mat = txt_to_mat("test1")
    mat_result = multiply(mat[0], mat[0])

    print(f"Variações de P1, P2, P3, P4 e P5: P1")
    print(f"Número de cores: {mat_result[1]}")
    print(f"Computadores Remotos: {0}")
    print(f"Numero de Linhas Matriz: {int(mat[1][0])}")
    print(f"Numero de Colunas Matriz: {int(mat[1][1])}")
    print(f"Tempo de Processamento: {mat_result[2]}")

    print("")

    print(f"Matriz Resposta:")
    for line in mat_result[0]:
        print(line)

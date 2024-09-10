from multiprocessing import Process
from datetime import datetime
import socket

matOne = [
    [1, 4],
    [2, 5],
    [3, 6]
]
matTwo = [
    [1, 3],
    [2, 4, ],
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

def multiply_l_c(line, colun, cont):
    mult = 0
    inicio = datetime.now().strftime("%H:%M:%S.%f")
    print(f"Processo {cont}: Inicio: {inicio}" )
    for i in range(len(line)):
        mult += line[i] * colun[i]
    fim = datetime.now().strftime("%H:%M:%S.%f")
    print(f"Processo {cont}: Fim: {fim}" )
    return mult

def multiply(mat1, mat2):
    mat_ret = []
    cont = 0
    for i in range(len(mat1)):
        mat_ret.append([0] * len(mat2[0]))

    for i in range(len(mat_ret[0])):
        for j in range(len(mat_ret)):
            cont+=1
            mat_ret[j][i] = Process(target=multiply_l_c, args=(get_line(i, mat2), get_colun(j, mat1), cont))
            mat_ret[j][i].start()
            print(mat_ret[j][i])
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

if __name__ == "__main__":
    #matFive = txt_to_mat('ex1')[0]
    #matSix = txt_to_mat('ex2')[0]
    #matSeven = txt_to_mat('ex3')[0]
    multiply(matThree, matFour)

    #print(multiply(matThree, matFour))
    #print(multiply(matThree, matFour))
    #print(multiply(matOne, matTwo))
    #print(multiply(matSix, matSix))

from multiprocessing import Process, Queue, cpu_count
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


def multiply_l_c(task_list, mat1, mat2, q):
    #Função executada pelos processos para multiplicar subconjuntos de linhas e colunas
    for task in task_list:
        j, i = task
        line = mat1[j]
        colun = get_colun(i, mat2)
        mult = sum(line[k] * colun[k] for k in range(len(line)))
        q.put((j, i, mult))


def multiply(mat1, mat2):
    """Multiplica duas matrizes utilizando um número de processos adaptado aos núcleos do processador"""
    if len(mat1[0]) != len(mat2):
        raise Exception(
            f"O número de colunas de mat1 ({len(mat1[0])}) deve ser igual ao número de linhas de mat2 ({len(mat2)}).")

    # Inicializa a matriz resultado
    mat_ret = []
    for i in range(len(mat1)):
        mat_ret.append([0] * len(mat2[0]))

    # Número de núcleos lógicos do processador
    num_cores = cpu_count()
    print(f"Utilizando {num_cores} processos.")

    # Lista de todas as operações (pares de índices [j, i] para multiplicação)
    tasks = [(j, i) for j in range(len(mat1)) for i in range(len(mat2[0]))]

    # Divide as tarefas entre os processos
    task_split = [tasks[i::num_cores] for i in range(num_cores)]

    # Inicializa a fila para armazenar os resultados
    q = Queue()

    # Início da contagem de tempo
    inicio_total = datetime.now()
    print(f"Multiplicação iniciada às {inicio_total.strftime('%H:%M:%S.%f')}")

    # Cria e inicia os processos
    processes = []
    for i in range(num_cores):
        process = Process(target=multiply_l_c, args=(task_split[i], mat1, mat2, q))
        processes.append(process)
        process.start()

    # Aguarda a finalização de todos os processos
    for process in processes:
        process.join()

    # Coleta os resultados da fila
    while not q.empty():
        j, i, result = q.get()
        mat_ret[j][i] = result

    # Fim da contagem de tempo
    fim_total = datetime.now()
    time_total = fim_total - inicio_total
    print(f"Multiplicação finalizada às {fim_total.strftime('%H:%M:%S.%f')}")
    print(f"Tempo total de processamento: {fim_total}")

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

    print(f"Variações de P1, P2, P3, P4 e P5: P2")
    print(f"Número de cores: {mat_result[1]}")
    print(f"Computadores Remotos: {0}")
    print(f"Numero de Linhas Matriz: {int(mat[1][0])}")
    print(f"Numero de Colunas Matriz: {int(mat[1][1])}")
    print(f"Tempo de Processamento: {mat_result[2]}")

    print("")

    print(f"Matriz Resposta:")
    for line in mat_result[0]:
        print(line)

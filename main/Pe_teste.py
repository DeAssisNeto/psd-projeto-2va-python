from multiprocessing import Process, Queue, cpu_count
from datetime import datetime


def get_colun(num, mat1):
    """Função para obter uma coluna de uma matriz"""
    return [row[num] for row in mat1]


def multiply_l_c(task_list, mat1, mat2, q):
    """Função executada pelos processos para multiplicar subconjuntos de linhas e colunas"""
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
    mat_ret = [[0] * len(mat2[0]) for _ in range(len(mat1))]

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
    # Garantindo que todos os processos tenham colocado seus resultados na fila
    results_collected = 0
    total_results = len(mat1) * len(mat2[0])  # Total de operações (linhas * colunas)

    while results_collected < total_results:
        j, i, result = q.get()
        mat_ret[j][i] = result
        results_collected += 1

    # Fim da contagem de tempo
    fim_total = datetime.now()
    time_total = fim_total - inicio_total
    print(f"Multiplicação finalizada às {fim_total.strftime('%H:%M:%S.%f')}")
    print(f"Tempo total de processamento: {time_total}")

    return mat_ret, num_cores, time_total


def txt_to_mat(file_name):
    """Carrega uma matriz de um arquivo txt"""
    list_ret = []
    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            list_ret.append(list(map(float, line.split())))

    return list_ret[1:], list_ret[0]  # Matriz e dimensões


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

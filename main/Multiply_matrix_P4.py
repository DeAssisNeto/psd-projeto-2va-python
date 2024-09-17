from multiprocessing import Process, Queue
from datetime import datetime

def get_line(num, mat):
    return [line for line in mat[num]]

def get_colun(num, mat):
    return [row[num] for row in mat]

def multiply_l_c(task_list, mat1, mat2, q, cc):
    """Função executada pelos processos para multiplicar subconjuntos de linhas e colunas."""
    for task in task_list:
        j, i = task
        line = mat1[j]
        colun = get_colun(i, mat2)
        mult = sum(line[k] * colun[k] for k in range(len(line)))
        q.put((j, i, mult))  # Coloca o resultado na fila (linha, coluna, multiplicação)

def multiply(mat1, mat2):
    """Multiplica duas matrizes utilizando um número de processos adaptado aos núcleos do processador."""
    if len(mat1[0]) != len(mat2):
        raise Exception(f"O número de colunas de mat1 ({len(mat1[0])}) deve ser igual ao número de linhas de mat2 ({len(mat2)}).")

    # Inicializa a matriz resultado
    mat_ret = [[0] * len(mat2[0]) for _ in range(len(mat1))]

    # Número de núcleos lógicos do processador (máximo de 16 processos)
    num_cores = 4

    # Lista de todas as operações (pares de índices [j, i] para multiplicação)
    tasks = [(j, i) for j in range(len(mat1)) for i in range(len(mat2[0]))]

    # Divide as tarefas entre os processos
    task_split = [tasks[i::num_cores] for i in range(num_cores)]

    # Inicializa a fila para armazenar os resultados
    q = Queue()

    # Início da contagem de tempo
    inicio_total = datetime.now()

    # Cria e inicia os processos
    processes = []
    cc = 1
    for i in range(num_cores):
        process = Process(target=multiply_l_c, args=(task_split[i], mat1, mat2, q, cc))
        processes.append(process)
        cc += 1
        process.start()

    # Coleta os resultados da fila
    collected_tasks = 0
    while collected_tasks < len(tasks):
        if not q.empty():
            j, i, result = q.get()
            mat_ret[j][i] = result  # Preenche a matriz resultante com os valores da fila
            collected_tasks += 1
        else:
            break

    # Fim da contagem de tempo
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
    return list_ret[1:], list_ret[0]  # Retorna a matriz lida do arquivo

if __name__ == "__main__":
    # Lê a matriz de um arquivo
    mat = txt_to_mat("./main/128")

    # Executa a multiplicação de matrizes
    mat_result, num_cores, time_total = multiply(mat[0], mat[0])

    # Exibe informações sobre a execução
    print(f"Variação P4")
    print(f"Número de núcleos: {num_cores}")
    print(f"Computadores Remotos: {0}")
    print(f"Numero de Linhas Matriz: {int(mat[1][0])}")
    print(f"Numero de Colunas Matriz: {int(mat[1][1])}")
    print(f"Tempo de processamento: {time_total}")

    print("\nMatriz Resultado:")
    for line in mat_result:
        print(line)  # Exibe a matriz resultante no formato adequado

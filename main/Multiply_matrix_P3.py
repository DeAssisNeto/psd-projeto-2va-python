from multiprocessing import Process, Queue
import numpy as np

def read_matrix(file_name):
    """Lê uma matriz de um arquivo de texto."""
    with open(file_name, 'r') as f:
        lines = f.readlines()
    dimensions = list(map(int, lines[0].strip().split()))
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(float, line.strip().split())))
    return np.array(matrix)

def multiply_part(result_queue, row, col, row_values, col_values):
    """Multiplica uma linha da primeira matriz por uma coluna da segunda."""
    result = np.dot(row_values, col_values)
    result_queue.put((row, col, result))

def distribute_tasks(mat1, mat2, result_queue):
    """Divide as tarefas de multiplicação entre processos."""
    processes = []
    rows_m1, cols_m2 = mat1.shape[0], mat2.shape[1]
    
    for i in range(rows_m1):  # Para cada linha da matriz 1
        for j in range(cols_m2):  # Para cada coluna da matriz 2
            row_values = mat1[i, :]
            col_values = mat2[:, j]
            process = Process(target=multiply_part, args=(result_queue, i, j, row_values, col_values))
            processes.append(process)
            process.start()

    # Esperar os processos terminarem
    for process in processes:
        process.join()

def collect_results(result_queue, result_matrix):
    """Coleta os resultados do Queue e preenche a matriz final."""
    while not result_queue.empty():
        row, col, result = result_queue.get()
        result_matrix[row][col] = result

def matrix_multiplication(mat1_file, mat2_file):
    """Gerencia a multiplicação de duas matrizes e retorna o resultado."""
    mat1 = read_matrix(mat1_file)
    mat2 = read_matrix(mat2_file)

    # Verificar a compatibilidade das dimensões
    if mat1.shape[1] != mat2.shape[0]:
        raise ValueError("O número de colunas da primeira matriz deve ser igual ao número de linhas da segunda matriz.")

    # Inicializar a matriz de resultado
    result_matrix = np.zeros((mat1.shape[0], mat2.shape[1]))

    # Fila para armazenar os resultados
    result_queue = Queue()

    # Dividir as tarefas e distribuir para processos
    distribute_tasks(mat1, mat2, result_queue)

    # Coletar os resultados e preencher a matriz
    collect_results(result_queue, result_matrix)

    return result_matrix

if __name__ == "__main__":
    # Defina os nomes dos arquivos de matriz diretamente aqui:
    mat1_file = "./main/ex1.txt"
    mat2_file = "./main/ex1.txt"

    # Executa a multiplicação de matrizes
    resultado = matrix_multiplication(mat1_file, mat2_file)

    # Exibe a matriz resultante
    print("Matriz Resultante:")
    print(resultado)

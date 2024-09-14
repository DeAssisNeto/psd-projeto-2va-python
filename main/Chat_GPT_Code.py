import numpy as np
import time
import threading
import multiprocessing
import os

def multiply_part(A, B, C, start_row, end_row):
    C[start_row:end_row] = np.dot(A[start_row:end_row], B)

def main():
    A = np.random.rand(100, 100)
    B = np.random.rand(100, 100)
    C = np.zeros((100, 100))
    
    num_threads = os.cpu_count()
    threads = []
    rows_per_thread = A.shape[0] // num_threads
    print(f'rows_per - {rows_per_thread} type- {type(rows_per_thread)}')
    print(f'rows - {A.shape[0]} type- {type(A.shape[0])}')
    
    start_time = time.time()
    for i in range(num_threads):
        start_row = i * rows_per_thread
        end_row = (i + 1) * rows_per_thread if i != num_threads - 1 else A.shape[0]
        thread = threading.Thread(target=multiply_part, args=(A, B, C, start_row, end_row))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    with open('output_P2.txt', 'w') as f:
        f.write("P2\n")
        f.write(f"{os.cpu_count()}\n")
        f.write("0\n")
        f.write(f"{A.shape[0]}\n")
        f.write(f"{A.shape[1]}\n")
        f.write(f"{processing_time}\n\n")
        np.savetxt(f, C, fmt='%.2f')

if __name__ == "__main__":
    main()

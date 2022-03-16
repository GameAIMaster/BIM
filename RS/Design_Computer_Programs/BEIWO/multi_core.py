# 多核计算
import math
import datetime
import multiprocessing as mp
import pandas as pd


def train_on_parameter(file_name, result_list, result_lock):
    result = 0
    # 成块读入
    reader = pd.read_csv(file_name,
                         header=None, sep=",", chunksize=50)
    print(next(reader))
    with result_lock:
        result_list = result
    return


def combine_particle(file_list, start_index, num):
    reader_map = {}
    for i in range(start_index, start_index + num):
        if i < len(file_list):
            file_name = file_list[i]
            # 成块读入
            reader = pd.read_csv(file_name,
                                 header=None, sep=",", chunksize=50)
            reader_map['task'+str(i)] = reader
        else:
            break
    return reader_map


if __name__ == '__main__':

    start_t = datetime.datetime.now()

    num_cores = int(mp.cpu_count())
    print("本地计算机有: " + str(num_cores) + " 核心")
    pool = mp.Pool(num_cores)
    file_list=[
        'data0.csv',
        'data1.csv',
        'data2.csv',
        'data3.csv',
        'data4.csv',
        'data5.csv',
        'data6.csv',
        'data7.csv',
    ]
    combine_map = combine_particle(file_list, 0, 8)
    param_dict = {'task0': list(range(10, 3000000)),
                  'task1': list(range(3000000, 6000000)),
                  'task2': list(range(6000000, 9000000)),
                  'task3': list(range(9000000, 12000000)),
                  'task4': list(range(12000000, 15000000)),
                  'task5': list(range(15000000, 18000000)),
                  'task6': list(range(18000000, 21000000)),
                  'task7': list(range(21000000, 24000000))}
    manager = mp.Manager()
    managed_locker = manager.Lock()
    managed_list = manager.list()
    results = [pool.apply_async(train_on_parameter, args=(file_name, managed_list, managed_locker)) for file_name in file_list]
    # results = [p.get() for p in results]

    print(managed_list)

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("多线程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
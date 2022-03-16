import pickle
import pandas as pd
import csv
import random
# 方法1，利用随机采样采取样本，或者利用齐普夫定律根据词频划定所选二元组的范围
# 目前素材有78150 形成的二元组则有78150*78150 = 6107422500个组合
# 假设所有的方案有1TB数据要进行统计，可以将数据随机采样0.01%,然后利用hash表统计次数
# 数据量没有那么多，那就采用全部数据，利用分治算法计算
# 假设对所有的商品素材编号，不包含材质，放样的商品

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    two_grams = [tuple(map(int,line.split(','))) for line in open(filename,mode='r').read().split('\n') ]
    return two_grams



# data = readwordlist('binarygroup1.txt')

# 随机生成测试数据
def generate_data(num):
    result = []
    for i in range(num):
        result.append(tuple([random.randint(1,100),random.randint(1,100)]))
    return result
# 假设所有商品计算了相连关系,用(x,y)表示，用<x,y,#(x,y)>表示
# 找出高频的二元组
def statistical_data(in_data):
    hash_table = {}
    for item in in_data:
        hash_table[item] = 1 + hash_table.get(item, 0)
    return hash_table

data = generate_data(1000)
statistical = statistical_data(data)
# print(statistical)

# 对结果排序写入数组中
result = sorted(statistical.items(), key=lambda item:item[0])

# 存储数据到硬盘 pickle
with open('data.pickle', 'wb') as f:
    pickle.dump(result, f)

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)
    print(data)
# 存储数据到硬盘 csv
# todo 是否是用数字格式存储数据的
with open('data7.csv','w') as out:
    csv_out=csv.writer(out)
    for row in result:
        csv_out.writerow((row[0][0], row[0][1], row[1]))

# 从硬盘中读取数据进行合并,瓶颈在于能够同时打开多少文件
# 重点在于如何从文件中读取一部分
# file_list 是打开的文件 num 为同时能够处理的文件
def combine_data(file_list, num):
    for i in range(0, len(file_list), num):
        combine_particle(file_list, i, num)

# 合并部分数据
def combine_particle(file_list, start_index, num):
    reader_list = []
    for i in range(start_index, start_index + num):
        if i < len(file_list):
            file_name = file_list[i]
            # 成块读入
            reader = pd.read_csv(file_name,
                                 header=None, sep=",", chunksize=50)
            reader_list.append(reader)
        else:
            break
    # todo 如何利用计算机的多核进行合并数据
# 对每块进行归并




combine_data(["data.csv"],0)
# 语料为planjson,分析的数据为商品ID，位置，包围盒
# 关联性用包围盒的粘合情况
# 有了二元组之后就能够进行PangeRank算法

# 有了图之后相当于有了“词库”

# 对“词库”进行前后缀构建，我认为一个商品就是前缀或者后缀，他的吸附面相当于锚点，有方向属性，本地会计算出当前“棋盘”下，下一步放置的分数
# 进行排序提示。
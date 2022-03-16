from numpy import *;#导入numpy的库函数
import numpy as np; #这个方式使用numpy的函数时，需要以np.开头。

a1=mat([[0, 2, 4, 0, 0, 0,3],
        [-1, 0, 2, 0, 0, 1, 0],
        [10, -2, 0, 0, 10, 0, 0],
        [0, 0, 0, 0, 0, 10, -1]])

class line_matrix:
    def __init__(self, in_mat):
        self.col_val = []
        self.row_start = []
        self.row_index = []
        self.col_start = []

        # 收集行索引的数据表
        self.collect_row_table(in_mat)
        self.collect_col_table(in_mat)

    def collect_row_table(self, in_mat):
        rows, cols = in_mat.shape
        for row in range(rows):
            bfindstart = False
            for col in range(cols):
                if(in_mat[row, col] !=0):
                    self.col_val.append((col, in_mat[row, col]))
                    if not bfindstart:
                        self.row_start.append(len(self.col_val) - 1)
                        bfindstart = True
            if(not bfindstart):
                self.row_start.append(len(self.col_val))

    def collect_col_table(self, in_mat):
        # 收集列索引的表
        startIndex = 0
        endIndex = 0
        rows, cols = in_mat.shape
        for col in range(cols):
            bfindstart = False
            for row in range(rows):
                if (in_mat[row, col] != 0):
                    if (row == rows - 1):
                        startIndex = self.row_start[-1]
                        endIndex = len(self.col_val)
                    else:
                        startIndex = self.row_start[row]
                        endIndex = self.row_start[row + 1]
                    for i in range(startIndex, endIndex, 1):
                        if (col == self.col_val[i][0]):
                            self.row_index.append((row, i))
                            if not bfindstart:
                                self.col_start.append(len(self.row_index) - 1)
                                bfindstart = True
                            break
            if (not bfindstart):
                self.col_start.append(len(self.row_index))
test = line_matrix(a1)
print()


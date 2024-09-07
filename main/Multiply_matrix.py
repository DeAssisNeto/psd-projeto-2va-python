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


class MultiplyMatrix():
    def __init__(self, mat1, mat2):
        self.mat1 = mat1
        self.mat2 = mat2
        self.size = len(mat1)
        self.size2 = len(mat2[0])

    def get_colun(self, num):
        return [i for i in self.mat1[num]]

    def get_line(self, num):
        return [i[num] for i in self.mat2]

    def multiply_l_c(self, line, colun):
        mult = 0
        for i in range(len(line)):
            mult += line[i] * colun[i]
        return mult

    def multiply(self):
        mat_ret = []
        mat_line = []
        for i in range(self.size):
            mat_ret.append([0] * self.size2)

        for i in range(len(mat_ret[0])):
            for j in range(len(mat_ret)):
                mat_ret[j][i] = self.multiply_l_c(self.get_line(i), self.get_colun(j))
        return mat_ret


mult_mat = MultiplyMatrix(matOne, matTwo)
mult_mat2 = MultiplyMatrix(matThree, matFour)

print(mult_mat.multiply())
print(mult_mat2.multiply())

from turtle import down


def pointwiseMultiplication(mat1, mat2):
    result = [[0 for x in range(3)] for y in range(3)] 
    for i in range(3):
        for j in range(3):
            result[i][j] = mat1[i][j] * mat2[i][j]
    return result
    
def rightMove(mat):
    result = [[0 for x in range(3)] for y in range(3)] 
    for i in range(3):
        for j in range(3):
            if (i == 2):
                if (j != 1):
                    result[i][j] = mat[i][j]
            elif (j == 1):
                result[i][j] = mat[i][j-1] * .9 + mat[i][j] * .1
            elif (j == 0):
                result[i][j] = mat[i][j] * .1
            elif (j == 2):
                result[i][j] = mat[i][j-1] * .9 + mat[i][j]

    return result

def downMove(mat):
    result = [[0 for x in range(3)] for y in range(3)] 
    for i in range(3):
        for j in range(3):
            if (i == 1):
                result[i][j] = mat[i-1][j] * .9 + mat[i][j] * .1
                if (j == 1):
                    result[i][j] += mat[i][j] * .9
            elif (i == 0):
                result[i][j] = mat[i][j] * .1
            elif (i == 2):
                result[i][j] = mat[i-1][j] * .9 + mat[i][j]
                if (j == 1): 
                    result[i][j] = 0

    return result

def normalize(mat):
    sum = summation(mat)
    for i in range(3):
        for j in range(3):
            mat[i][j] /= sum
    
def summation(mat):
    sum = 0
    for i in range(3):
        for j in range(3):
            sum += mat[i][j]
    return sum

mat = [[0 for x in range(3)] for y in range(3)] 
for i in range(3):
    for j in range(3):
        mat[i][j] = .125
mat[2][1] = 0

matE = [[0 for x in range(3)] for y in range(3)] 
matE = [[.0167, .0167, .05],[.225, .225, .225],[.225, 0, .0167]]
matF = [[0 for x in range(3)] for y in range(3)] 
matF = [[.3, .3, .05], [.0125, .0125, .0125], [.0125, 0, .3]]

mat2 = rightMove(mat)
mat3 = pointwiseMultiplication(mat2, matE)
normalize(mat3)
print(mat3)

mat4 = rightMove(mat3)
mat5 = pointwiseMultiplication(mat4, matE)
normalize(mat5)
print(mat5)

mat6 = downMove(mat5)
mat7 = pointwiseMultiplication(mat6, matF)
normalize(mat7)
print(mat7)

mat8 = downMove(mat7)
mat9 = pointwiseMultiplication(mat8, matF)
normalize(mat9)
print(mat9)
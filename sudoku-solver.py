from z3 import *
from math import sqrt


# 3 constraints to satisfy
# each digit appears one and only one time in each single square, line and column

matrix = [[2, 5, 0, 0, 3, 0, 9, 0, 1],[0, 1, 0, 0, 0, 4, 0, 0, 0],[4, 0, 7, 0, 0, 0, 2, 0, 8],[0, 0, 5, 2, 0, 0, 0, 0, 0],[0, 0, 0, 0, 9, 8, 1, 0, 0],[0, 4, 0, 0, 0, 3, 0, 0, 0],[0, 0, 0, 3, 6, 0, 0, 7, 2],[0, 7, 0, 0, 0, 0, 0, 0, 3],[9, 0, 3, 0, 0, 0, 6, 0, 4]]
side_length = int(math.sqrt(len(matrix)))
upper_bound = 10 # the number of solutions we wish to look for


#replacing each "0" with a symbolic variable while mainting the information about its place in its name
def treatMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                matrix[i][j] = Int("X"+str(i)+str(j))
    return matrix


# there are sqrt(len(matrix)) squares, we extract them using this function
def getSquare(matrix, n, m):
    square = []
    side_length = int(math.sqrt(len(matrix)))
    for i in range(side_length):
        for j in range(side_length):
            square.append(matrix[side_length*n+i][side_length*m+j])
    return square

# extracting each line
def getLine(matrix, n):
    return matrix[n]

#extracting each column
def getColumn(matrix, m):
    column = []
    for i in range(len(matrix)):
        column.append(matrix[i][m])
    return column


new_matrix = treatMatrix(matrix)

solver = Solver()


for i in range(len(matrix)):
    #adding the constraint that the valus in each line/column are pairwise distinct 
    #included in this for loop for optimization purposes
    solver.add(Distinct(getColumn(new_matrix, i)))
    solver.add(Distinct(getLine(new_matrix, i)))

    for j in range(len(matrix)):
        #adding the constraint that each element in the matrix is between 1 and length of matrix which should be a perfect square
        solver.add(matrix[i][j] < len(matrix) + 1)
        solver.add(matrix[i][j] > 0)

    
#adding the constraint that the element od each square should be pairwise distinct distinct
for i in range(side_length):
    for j in range(side_length):
        solver.add(Distinct(getSquare(new_matrix, i, j)))

#solver.check()
#solution = solver.model()


def get_solutions(solver):
    result = solver.check()
    # while there still are solutions
    while (result == z3.sat):
      model = solver.model()
      yield model
      # add a solution a constraint to generate a different one next time
      block = []
      for var in model:
          block.append(var() != model[var])
      solver.add(z3.Or(block))
      result = solver.check()

solutions = get_solutions(solver)
for solution, _ in zip(solutions, range(upper_bound)):

    #replacing each symbolic variable in the matrix by its value
    for i in range(len(new_matrix)):
        for j in range(len(new_matrix)):
            if isinstance(new_matrix[i][j], int):
                continue
            new_matrix[i][j] = solution.evaluate(new_matrix[i][j])

    print(new_matrix)








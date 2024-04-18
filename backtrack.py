# Import required modules
# Python Equivalent
import random
import time
import numpy as np
 
# Directional Arrays
dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]


# Stores the number of rows
# and columns of the matrix
N, M = 7, 7
 
# Stores the final generated input
arr = [[0 for _ in range(M)] for _ in range(N)]

# Function to check if the cell (x, y) is valid or not
def isValid(x, y, N, M):
    return (x >= 0 and y >= 0 and x < N and y < M)
 
# Function to generate a valid minesweeper
# matrix of size ROW * COL with P being
# the probability of a cell being a mine
def generateMineField(ROW, COL, P):
    # Generates the random
    # number every time
    random.seed(time.time())
 
    # Stores whether a cell
    # contains a mine or not
    mines = [[False for _ in range(COL)] for _ in range(ROW)]
 
    # Iterate through each cell
    # of the matrix mine
    for x in range(ROW):
        for y in range(COL):
            # Generate a random value
            # from the range [0, 100]
            rand_val = random.randint(0, 100)
            # If rand_val is less than P
            if rand_val < P:
                # MArk mines[x][y] as True
                mines[x][y] = True
            # Otherwise, mark
            # mines[x][y] as False
            else:
                mines[x][y] = False
 
    print("Generated Input:")
 
    # Iterate through each cell (x, y)
    for x in range(ROW):
        for y in range(COL):
            arr[x][y] = 0
            # Count the number of mines
            # around the cell (x, y)
            # and store in arr[x][y]
            for k in range(9):
                # If current adjacent cell is valid
                if isValid(x + dx[k], y + dy[k], N, M) and mines[x + dx[k]][y + dy[k]]:
                    arr[x][y] += 1
            # Print the value at
            # the current cell
            print(arr[x][y], end=" ")
        print()
 
# Function to print the matrix grid[][]
def printGrid(grid):
    print("Generated Solution:")
    for row in grid:
        for cell in row:
            if cell:
                print("x", end=" ")
            else:
                print("_", end=" ")
        print()
 
# Function to check if the cell (x, y) is valid to have a mine or not
def isSafe(arr, x, y, N, M):
    # Check if the cell (x, y) is a valid cell or not
    if not isValid(x, y, N, M):
        return False
 
    # Check if any of the neighbouring cell of (x, y) supports (x, y) to have a mine
    for i in range(9):
        if isValid(x + dx[i], y + dy[i], N, M) and (arr[x + dx[i]][y + dy[i]] - 1 < 0):
            return False
 
    # If (x, y) is valid to have a mine
    for i in range(9):
        if isValid(x + dx[i], y + dy[i], N, M):
            # Reduce count of mines in the neighboring cells
            arr[x + dx[i]][y + dy[i]] -= 1
 
    return True
 
# Function to check if there exists any unvisited cell or not
def findUnvisited(visited):
    for x in range(len(visited)):
        for y in range(len(visited[0])):
            if not visited[x][y]:
                return x, y
    return -1, -1
 
# Function to check if all the cells are visited or not and the input array is satisfied with the mine assignments
def isDone(arr, visited):
    done = True
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            done = done and (arr[i][j] == 0) and visited[i][j]
    return done
 
# Function to solve the minesweeper matrix
def SolveMinesweeper(grid, arr, visited, N, M):
    # Function call to check if each cell is visited and the solved grid is satisfying the given input matrix
    done = isDone(arr, visited)
 
    # If the solution exists and all cells are visited
    if done:
        return True
 
    x, y = findUnvisited(visited)
 
    # Function call to check if all the cells are visited or not
    if x == -1 and y == -1:
        return False
 
    # Mark cell (x, y) as visited
    visited[x][y] = True
 
    # Function call to check if it is safe to assign a mine at (x, y)
    if isSafe(arr, x, y, N, M):
        # Mark the position with a mine
        grid[x][y] = True
 
        # Recursive call with (x, y) having a mine
        if SolveMinesweeper(grid, arr, visited, N, M):
            # If solution exists, then return true
            return True
 
        # Reset the position x, y
        grid[x][y] = False
        for i in range(9):
            if isValid(x + dx[i], y + dy[i], N, M):
                arr[x + dx[i]][y + dy[i]] += 1
 
    # Recursive call without (x, y) having a mine
    if SolveMinesweeper(grid, arr, visited, N, M):
        # If solution exists then return true
        return True
 
    # Mark the position as unvisited again
    visited[x][y] = False
 
    # If no solution exists
    return False
 
# Function to perform generate and solve a minesweeper
def minesweeperOperations(arr, N, M):
    # Stores the final result
    grid = np.zeros((N, M), dtype=bool)
 
    # Stores whether the position (x, y) is visited or not
    visited = np.zeros((N, M), dtype=bool)
 
    # If the solution to the input minesweeper matrix exists
    if SolveMinesweeper(grid, arr, visited, N, M):
        # Function call to print the grid[][]
        printGrid(grid)
    # No solution exists
    else:
        print("No solution exists")
 
# Driver Code
if __name__ == "__main__":
    # print('Enter rows:')
    # N = input()
    # print('Enter column:')
    # M = input()
    # print('Enter mine:')
    # P = input()
    
    generateMineField(N, M, 15)
    # Function call to perform generate and solve a minesweeper
    minesweeperOperations(arr, N, M)
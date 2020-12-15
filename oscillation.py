#Time complexity O(N-1) = O(N)
#Space complexity O(N+N+N) = O(3N) = O(N)
def longest_oscillation(list):
    if len(list) < 3:
        if list[0] != list[1]:
            return (2, [0,1])
        else:
            return (1, [0])
    elif len(list) == 0:
        return(0,[])

    memo_down = [0] * len(list)
    memo_up = [0] * len(list)
    solution = []
    solution.append(0)              #base case (first item in sequence is a startin point, so it is either first peak or first bottom point)
    for i in range(1,len(list)):        #goes through each element starting from index 1

        if list[i] > list[i-1]:                 #case 1: number > previous number, therefore sequence is going up
            memo_up[i] = memo_down[i-1] + 1     #memo_up[i] is the last element in memo_down[i-1] + 1
            memo_down[i] = memo_down[i-1]       #memo_down carrying previous element

        elif list[i] < list[i-1]:               #case 2: number < previous number, therefore sequence is going down
            memo_down[i] = memo_up[i-1] + 1     #memo_down[i] is the last element in memo_up[i-1] + 1
            memo_up[i] = memo_up[i-1]           #memo_up carrying last element

        else:                                   #case else: number = previous number
            memo_up[i] = memo_up[i-1]           #since sequence doesnt change both up and down lists carrying previous number
            memo_down[i] = memo_down[i-1]


        #finding oscilation
        if memo_up[i] - memo_down[i] == 1 and memo_up[i] > memo_up[i-1]:        #if memo_up and memo_down are different by 1 at the same index, and memo_up[i] > memo_up[i-1],
            if i > 1:                                                           #therefore previous number was the top point
                solution.append(i-1)

        elif memo_down[i] - memo_up[i] == 1 and memo_down[i] > memo_down[i-1]:  #if memo_up and memo_down are different by 1 at the same index, and memo_up[i] > memo_up[i-1],
            if i > 1:                                                           #therefore previous number was the bottom point
                solution.append(i-1)

    #dealing with last number by comparing last number in sequence and last number in solution, if they are different - append to the solution
    if list[len(list) - 1] != list[solution[len(solution) - 1]]:
        solution.append(len(list) - 1)

    return (len(solution), solution)




######################################################################## longest "walk" ########################################################################


# space complexity O(1), since nothing is stored inside aux function
# time complexity is constant
def longest_walk_aux(row, col, memo, M, n, m):
    if memo[row][col] != 0:  # if item at index is not 0, it's been already processed, so return it
        return memo[row][col]

    for i in range(8):  # since there are only 8 possible ways to go we iterate only 8 times once for every way
        possible_moves = [(row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col),
                          (row + 1, col - 1), (row, col - 1),
                          (row - 1, col - 1)]  # list of all possible moves for given index

        next_row = possible_moves[i][0]
        next_col = possible_moves[i][1]

        if (next_row >= 0 and next_row < n) and (
                next_col >= 0 and next_col < m):  # check if next possible way is out of bounds
            if M[next_row][next_col] > M[row][col]:  # check if the next number is bigger than current
                memo[row][col] = max(memo[row][col], longest_walk_aux(next_row, next_col, memo, M, n,
                                                                      m))  # record maximum path value for current index taken from neighouring items

    memo[row][col] += 1  # and adding 1
    return memo[row][col]


# find maximum element in memo matrix
# time complexity O(N * M)
# space complexity O(1)
def maximum_position(memo):
    maximum = 0
    for row in range(len(memo)):
        for col in range(len(memo[0])):
            if memo[row][col] > maximum:
                maximum = memo[row][col]
                i = row
                j = col
    row = i
    col = j

    return row, col, maximum


# returns all coordinates for numbers that belong to longest path
# time complexity O(1)
# space complexity ~O(N*M), if all the elements of matrix fall in longest path
def backtrack(memo, maximum, n, m, M, row, col):
    solution = []
    solution.append((row, col))

    # for every item in distance
    for z in range(maximum):
        for v in range(8):  # for every possible way
            possible_moves = [(row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col),
                              (row + 1, col - 1), (row, col - 1), (row - 1, col - 1)]

            next_row = possible_moves[v][0]
            next_col = possible_moves[v][1]
            if (next_row >= 0 and next_row < n) and (next_col >= 0 and next_col < m):  # if next element is in bounds

                if M[row][col] < M[next_row][
                    next_col]:  # if element in original matrix is smaller than the next element
                    b = memo[row][col]
                    a = memo[next_row][next_col]

                    if b - a == 1 and M[row][col] != M[next_row][next_col]:  # and their difference in memo list is = 1
                        row = next_row  # make next element to be current element
                        col = next_col
                        solution.append((row, col))  # append coordinates to solution

    solution = (len(solution), solution)

    return solution


# space complexity is O(N*M + N*M) = O(2 * N * M) = O(N * M)  because of the memo matrix and maximum_position
# time complextiy is O(N*M), since we iterate through every element in matrix
def longest_walk(M):
    n = len(M)
    m = len(M[0])

    if n == 0 or m == 0:  # check for correct input
        return (0, [])

    memo = [[0] * m for z in range(n)]  # create memo matrix of same size as original matrix

    # for every number in matrix
    for row in range(n):
        for col in range(m):
            longest_walk_aux(row, col, memo, M, n, m)  # longest path for every number

    row, col, maximum = maximum_position(memo)
    solution = backtrack(memo, maximum, n, m, M, row, col)

    return solution



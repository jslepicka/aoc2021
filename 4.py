def mark_board(number, board):
    if board[0] & 512:
        #already won; skip
        return
    for i, n in enumerate(board):
        if n == number:
            #mark the number
            board[i] |= 256

def check_board(board):
    if board[0] & 512:
        #already won; skip
        return False
    #check horizontally
    for i in range(5):
        bingo = True
        for j in range(5):
            x = board[i*5 + j]
            if not (x & 256):
                bingo = False
                break
        if bingo == True:
            #mark the board as won
            board[0] |= 512
            return True
    #check vertically
    for i in range(5):
        bingo = True
        for j in range(5):
            x = board[i + j*5]
            if not (x & 256):
                bingo = False
                break
        if bingo == True:
            #mark the board as won
            board[0] |= 512
            return True
    return False
        
def get_score(board):
    score = 0
    for pos in board:
        #if this number is not marked, add it to the score
        if not pos & 256:
            score += (pos & 255)
    return score

def part1(numbers, boards):
    for number in numbers:
        for board in boards:
            mark_board(number, board)
            if check_board(board) == True:
                score = get_score(board)
                return score * number
    return None

def part2(numbers, boards):
    last_winner = None
    last_number = 0
    for number in numbers:
        for b, board in enumerate(boards):
            mark_board(number, board)
            if check_board(board) == True:
                last_winner = b
                last_number = number
    score = get_score(boards[last_winner])
    return score * last_number

def main():
    numbers = None
    input = []
    boards = []
    with open("4.txt") as file:
        numbers = [int(x) for x in file.readline().strip().split(",")]
        file.readline()
        board = []
        count = 0
        for x in [x.strip() for x in file.readlines()]:
            if x == "":
                continue
            x = " ".join(x.split())
            for i in x.strip().split(" "):
                board.append(int(i))
            count += 1
            if (count == 5):
                boards.append(board)
                board = []
                count = 0


    print("Part 1: " + str(part1(numbers, boards.copy())))
    print("Part 2: " + str(part2(numbers, boards.copy())))

if __name__ == "__main__":
    main()

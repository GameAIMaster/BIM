def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show(board):
    "Print the board."
    ###Your code here.
    for line in board:
        for a in line:
            print(a, end='')
        print('\n')

show(a_board())
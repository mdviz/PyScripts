# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 18:02:09 2014

@author: mdowd
"""

##tic-tac-toe
from random import sample

def tic_tac_toe():    
    
    def quit(moveI, moveJ):
        if (moveI, moveJ) == (0,0): 
            return None
        else:
            return True
        
    def computer_move(board, index_dict, index):
        import random
        print board
        moves = []
        print 'move=', moves
        for item in index[0]:
            for item2 in index[1]:
                if not board[index_dict[item]][item2-1]:
                    print item, item2
                    moves.append((item,item2))

        search = True
        while search:
            #First Search to See if Computer can just win
            for move in moves:
                board[index_dict[move[0]]][move[1]-1] = -1
                if match_check(board) is False:
                    board[index_dict[move[0]]][move[1]-1] = 0
                    move = move[0]+str(move[1])
                    return move
                else:
                    board[index_dict[move[0]]][move[1]-1] = 0

            #Next See if Computer can Block Player 1
            for move in moves:
                board[index_dict[move[0]]][move[1]-1] = 1
                if match_check(board) is False:
                    if random.random() > .2: #Just to add some randomness, reduce the number of draws. 
                        move = move[0]+str(move[1])
                        return move
                else:
                    board[index_dict[move[0]]][move[1]-1] = 0
            break
        #Otherwise Just Randomely choose a slot
        move = sample(moves, 1)[0]
        move = move[0]+str(move[1])
        print board
        return move
        
                
    def pretty_print_board(board, index, index_dict):
        count = -1
        print ' ',
        for item in index[1]: print item,
        print ''
        for row in board:
            count +=1
            print index[0][count],
            for cell in row:
                if not cell:
                    print '-',
                elif cell == 1:
                    print 'X',
                else:
                    print 'O',
            print ''
    
    #Handles weather a move is valid or not
    def move_call(index, turn_count, board, index_dict, computer):
        try:
            if i != None or j != None:
                if board[index_dict[i]][j-1] != 0:
                    print 'already taken'
                    return move_call(index, turn_count)
                else:
                    return i,j
                    
        except UnboundLocalError:
            if not (turn_count % 2):
                move = raw_input('Player 1 Enter Move: ')
            elif (turn_count % 2):
                if not computer:
                    move = raw_input('Player 2 Enter Move: ')
                    'print got player 2 move'
#                    continue
                else:
                    raw_input('Computer playing move: hit enter')
                    move = computer_move(board, index_dict, index)
            try:
                #print 'about to try the move'
                i, j =  move[0].upper(),int(move[1])
                if not(i in index[0] and j in index[1]):
                    return move_call(index, turn_count-1)
                if board[index_dict[i]][j-1] != 0:
                    print 'That spot is Already taken - Hit Enter: '
                    return move_call(index, turn_count)
                #print 'returning i.j'
                return i, j
            except:
                quit = raw_input('Would you like to Quit? If so press Q, If not press enter. ')
                if quit.upper() == 'Q':
                    return (0,0)
                else:
                    return move_call(index, turn_count, board, index_dict,computer)

    def match_check(board):
        count = -1
        column_dict= {0:0,1:0,2:0}
        
        #Control for all Cell Full
        board_tot = []
        [board_tot.extend(i) for i in board]
        if sum(abs(i) for i in board_tot) == 9:  
            return False
            
        #Control for Horizontal Wins
        for row in board:
            if abs(sum(i for i in row)) == 3:
                return False
            for column in row: 
                count += 1
                column_dict[count] += column
            count = -1
        
        #Control for Vertical Wins
        for i in range(len(board)):
            if abs(column_dict[i]) == 3:
                return False
                
        #Control Diagnols 
        if abs(sum(board[i][i] for i in range(len(board)))) == 3:
            return False
        board.reverse()
        if abs(sum(board[i][i] for i in range(len(board)))) == 3:
            return False
        else: 
            board.reverse()
            return True                
                
    #Actual Game Play
    def playing():
        #Initil Variables
        board = [3*[0],3*[0],3*[0]]
        index = [['A','B','C'],[1,2,3]]
        index_dict = {'A':0, 'B':1, 'C':2}
        
        #Introduction & First Move
        print 'Welcome to game!'
        
        #Determine Whether the Player wants to Play with Another Human or Against the Computer
        
        man_machine = raw_input('Would you like to pass and play, or play against the computer?, Please type H for Human or C for Computer: ')
        if man_machine.upper() == 'H':
            computer = False
        else:
            computer = True
            
        pretty_print_board(board, index, index_dict)
        print 'Please enter the index (Letter followed by Number: \n For Example -> A1 to put X in first column first row \n What is your move? '
        
        turn_count = 2
        moveI, moveJ = move_call(index, turn_count, board, index_dict, computer)
        
        if  quit(moveI, moveJ) is None:
            return None
        board[index_dict[moveI]][moveJ-1] = 1
        pretty_print_board(board, index, index_dict)
        turn_count = 0
        
        while match_check(board):    
            #pretty_print_board(board, index, index_dict)
            turn_count += 1
            
            moveI, moveJ = move_call(index, turn_count, board, index_dict, computer)
            if quit(moveI, moveJ) is None: 
                play = None
                return play
            if not (turn_count % 2):
                board[index_dict[moveI]][moveJ-1] = 1                
            else:
                board[index_dict[moveI]][moveJ-1] = -1
            pretty_print_board(board, index, index_dict)
        print 30*'_'
        pretty_print_board(board, index, index_dict)
        
        #Print who won
        print (not match_check(board)), computer
        if (turn_count % 2)==0 and (not match_check(board)):
             print 'Player 1 Won'
        elif (not match_check(board)) and computer:
            print 'Computer Won'
        elif not match_check: 
            print 'Player 2 Won'
        else: print 'It\'s a draw!'
        play_again = raw_input('play_again? [Y/N]: ')
        if play_again.upper() == 'N': 
            play_again = None 
        return play_again
       
    play = playing()
    while play == 'Y' or play != None:
        print 'Starting New Game'
        moveI, moveJ = None, None
        play = playing()     
    print 'Goodbye'            
    


    
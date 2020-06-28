# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pygame
import sys
import math 
import random
ROW_COUNT=6
COL_COUNT=7
PLAYER_1=1
PLAYER_AI=2
WINDOW_LENGTH=4
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
EMPTY=0
PLAYER=0
AI=1
first_chance=PLAYER
#Creates initial board
def create_board():
    board= np.zeros((ROW_COUNT,COL_COUNT))
    return board

# Drop piece of the particular player
    
def drop_piece(board,row,col,piece):
    board[row][col]=piece

#Checks if the column is filled fully
def is_valid_location(board,col):
    return board[0][col]==0

# Finds the first row which is unfilled
def get_next_open_row(board,col):
    for r in range(ROW_COUNT-1,-1,-1):
        if board[r][col]==0:
            return r
def winning_move(board,piece):
    #Horizontal Win
    
    for r in range(ROW_COUNT):
        row_array=[int (i)for i in list(board[r,:])]
        for c in range(COL_COUNT-WINDOW_LENGTH+1):
            window= row_array[c:c+WINDOW_LENGTH]
            if window.count(piece)==4:
                return True
    #Vertical Win
    for c in range(COL_COUNT):
        col_array=[int (i)for i in list(board[:,c])]
        for r in range(ROW_COUNT-WINDOW_LENGTH+1):
            window= col_array[r:r+WINDOW_LENGTH]
            if window.count(piece)==4:
                return True
    #Diagonal positive slope
            
    for r in range(ROW_COUNT-WINDOW_LENGTH+1,ROW_COUNT):
        for c in range(COL_COUNT-WINDOW_LENGTH+1):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True
    # Diagonal Negative slope
    for r in range(ROW_COUNT-WINDOW_LENGTH+1,ROW_COUNT):
        for c in range(COL_COUNT-WINDOW_LENGTH,COL_COUNT):
            if board[r][c]==piece and board[r-1][c-1]==piece and board[r-2][c-2]==piece and board[r-3][c-3]==piece:
                return True
def evaluate_window(window,piece,difficulty):
            score=0
            index_AI=None
            index_PLAYER=None
            opponent_piece=PLAYER_1
            if piece==PLAYER_1:
                opponent_piece=PLAYER_AI
            if window.count(piece)==4:
                score+=1000    
            elif  window.count(piece)==3 and  window.count(EMPTY)==1:
                score+=10
                if difficulty=="expert":
                    for i in range(WINDOW_LENGTH):
                        if window[i]==EMPTY:
                            index_AI=i
                    
            elif window.count(piece)==2 and window.count(EMPTY)==2:
                score+=2
            if window.count(opponent_piece)==3 and window.count(EMPTY)==1:
                score-=400
                if difficulty=="expert":
                    for i in range(WINDOW_LENGTH):
                        if window[i]==EMPTY:
                            index_PLAYER=i
            if window.count(opponent_piece)==3 and window.count(PLAYER_AI)==1:
                score+=400
            return score,index_AI,index_PLAYER
def score_position(board,piece,difficulty):
    score =0
    # Score center
    center_array=[int (i)for i in list(board[:,COL_COUNT//2])]
    center_count=center_array.count(piece)
    score=score+ center_count*3
    
    #Horizontal Score
    
    for r in range(ROW_COUNT):
        row_array=[int (i)for i in list(board[r,:])]
        for c in range(COL_COUNT-WINDOW_LENGTH+1):
            window= row_array[c:c+WINDOW_LENGTH]
            score+=evaluate_window(window,piece,difficulty)[0]
            index=evaluate_window(window, piece, difficulty)[1]
            index_PLAYER=evaluate_window(window, piece, difficulty)[2]
            if index!=None:
                
                if first_chance ==AI:
                    if r==2 or r==4 or r==6:
                        score+=15
                else:
                    if r==1 or r==3 or r==5:
                        score+=15
            if index_PLAYER!=None:
                if first_chance ==AI:
                    if r%2==1:
                        score-=25
                else:
                    if r%2==0:
                        score-=25
                
    #Vertical score
    for c in range(COL_COUNT):
        col_array=[int (i)for i in list(board[:,c])]
        for r in range(ROW_COUNT-WINDOW_LENGTH+1):
            window= col_array[r:r+WINDOW_LENGTH]
            score+=evaluate_window(window,piece,difficulty)[0]
            index=evaluate_window(window, piece, difficulty)[1]
            index_PLAYER=evaluate_window(window, piece, difficulty)[2]
            if index!=None:
                if first_chance ==AI:
                    if (r+index+1)%2 ==0:
                        score=score+15
                else:
                    if (r+index+1) %2 ==1:
                        score+=15
            if index_PLAYER!=None:
                if first_chance ==AI:
                    if (r+index_PLAYER+1)%2 ==1:
                        score=score-25
                else:
                    if (r+index_PLAYER+1) %2 ==0:
                        score-=25
                    
    #Diagonal positive slope score
    for r in range(ROW_COUNT-WINDOW_LENGTH+1,ROW_COUNT):
        for c in range(COL_COUNT-WINDOW_LENGTH+1):
            window=[board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score+=evaluate_window(window,piece,difficulty)[0]
            index=evaluate_window(window, piece, difficulty)[1]
            index_PLAYER=evaluate_window(window, piece, difficulty)[2]
            if index!=None:
                if first_chance ==AI:
                    if (r-index+1)%2==0:
                         score=score+15
                else:
                    if (r-index+1)%2==1:
                         score=score+15
            if index_PLAYER!=None:
                if first_chance ==AI:
                    if (r-index_PLAYER+1)%2==1:
                         score=score-25
                else:
                    if (r-index_PLAYER+1)%2==0:
                         score=score-25
                        
                
    # Diagonal Negative slope
    for r in range(ROW_COUNT-WINDOW_LENGTH+1,ROW_COUNT):
        for c in range(COL_COUNT-WINDOW_LENGTH,COL_COUNT):
            window=[board[r-i][c-i] for i in range(WINDOW_LENGTH)]
            score+=evaluate_window(window,piece,difficulty)[0]
            index=evaluate_window(window, piece, difficulty)[1]
            index_PLAYER=evaluate_window(window, piece, difficulty)[2]
            if index!=None:
                if first_chance ==AI:
                    if (r-index+1)%2==0:
                         score=score+15
                else:
                    if (r-index+1)%2==1:
                         score=score+15
            if index_PLAYER!=None:
                if first_chance ==AI:
                    if (r-index_PLAYER+1)%2==1:
                         score=score-25
                else:
                    if (r-index_PLAYER+1)%2==0:
                         score=score-25
    return score

def get_valid_locations(board):
    valid_locations=[]
    for c in range(COL_COUNT):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations

def pick_best_move(board,piece):
    valid_locations=get_valid_locations(board)
    best_score=0
    best_col=random.choice(valid_locations)
    for col in valid_locations:
        tempboard=board.copy()
        row=get_next_open_row(board,col)
        drop_piece(tempboard,row,col,piece)
        score=score_position(tempboard,piece,difficulty)
        if score>best_score:
            best_score=score
            best_col=col
    return best_col
def is_terminal_node(board):
    return winning_move(board,PLAYER_1) or winning_move(board,PLAYER_AI) or len(get_valid_locations(board))==0

def minimax(board,depth,alpha,beta,maximizing_player):
    valid_locations=get_valid_locations(board)
    is_terminal=is_terminal_node(board)
    if depth==0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_AI):
                return (None,10000000000)
            elif winning_move(board, PLAYER_1):
                return (None,-1000000000)
            else:
                return (None,0) 
        else:
            return (None,score_position(board, PLAYER_AI,difficulty))
    if maximizing_player:
        value=-math.inf
        column=random.choice(valid_locations)
        for col in valid_locations:
            row=get_next_open_row(board, col)
            board_copy=board.copy()
            drop_piece(board_copy, row, col, PLAYER_AI)
            new_score=minimax(board_copy,depth-1,alpha,beta,False)[1]
            if new_score>value:
                value=new_score
                column=col
            alpha=max(value,alpha)
            if alpha>=beta:
                break
        return column,value
    else:
        value=math.inf
        column=random.choice(valid_locations)
        for col in valid_locations:
            row=get_next_open_row(board, col)
            board_copy=board.copy()
            drop_piece(board_copy, row, col, PLAYER_1)
            new_score=minimax(board_copy,depth-1,alpha,beta,True)[1]
            if new_score<value:
                value=new_score
                column=col
            beta=min(value,beta)
            if alpha>=beta:
                break
        return column,value
        
    
def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            if board[r][c]==0:
                pygame.draw.circle(screen,BLACK,(c*SQUARE_SIZE+SQUARE_SIZE//2,r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE//2),RADIUS)
            elif board[r][c]==PLAYER_1:
                pygame.draw.circle(screen,RED,(c*SQUARE_SIZE+SQUARE_SIZE//2,r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE//2),RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(c*SQUARE_SIZE+SQUARE_SIZE//2,r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE//2),RADIUS)
    pygame.display.update()           
# board=create_board()
# game_over= False
# turn =0

pygame.init()
SQUARE_SIZE=100
RADIUS= int(SQUARE_SIZE//2)-5
height=(ROW_COUNT+1) *SQUARE_SIZE
width= COL_COUNT *SQUARE_SIZE
size =(width,height)
screen =pygame.display.set_mode(size)
# draw_board(board)
pygame.display.update()
myfont=pygame.font.SysFont("momospace",30)
win_font=pygame.font.SysFont("momospace",60)
# turn=random.randint(PLAYER,AI)



img=pygame.image.load('images/connect4_resized.jpg')

def find_difficulty(posx,posy):
    if posy >=20 and posy<=80 and posx>=20 and posx<=140:
        return "easy"
    elif posy >=120 and posy<=180 and posx>=20 and posx<=140:
        return "medium"
    elif posy >=220 and posy<=280 and posx>=20 and posx<=140:
        return "hard"
    elif posy >=320 and posy<=380 and posx>=20 and posx<=140:
        return "expert"
    
    else:
        return "none"
while True:
    #screen.fill(white)
    
    screen.blit(img,(0,0))
    pygame.draw.rect(screen,BLACK,(20,20,120,60))
    label=myfont.render("EASY",1,RED)
    screen.blit(label,(40,40))
    pygame.draw.rect(screen,BLACK,(20,120,120,60))
    label=myfont.render("MEDIUM",1,RED)
    screen.blit(label,(40,140))
    pygame.draw.rect(screen,BLACK,(20,220,120,60))
    label=myfont.render("HARD",1,RED)
    screen.blit(label,(40,240))
    pygame.draw.rect(screen,BLACK,(20,320,120,60))
    label=myfont.render("EXPERT",1,RED)
    screen.blit(label,(40,340))
    # pygame.draw.rect(screen,BLACK,(20,420,170,60))
    # label=myfont.render("MULTIPLAYER",1,RED)
    # screen.blit(label,(40,440))
    turn=random.randint(PLAYER,AI)
    if turn==AI:
        first_chance=AI
    board=create_board()
    game_over= False
    difficulty="none"
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            posx=event.pos[0]
            posy=event.pos[1]
            print(posx)
            print(posy)
            difficulty= find_difficulty(posx,posy)
            print(difficulty)
            if difficulty!="none":
                draw_board(board)
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()







    while not game_over and difficulty!="none":
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEMOTION:
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
                posx=event.pos[0]
                if turn ==0:
                    pygame.draw.circle(screen,RED,(posx,int(SQUARE_SIZE//2)),RADIUS)
               
            pygame.display.update()    
            if event.type== pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
                # print("")
                #Player 1 turn
                if turn==PLAYER:
                    posx=event.pos[0]//SQUARE_SIZE
                    col=int(posx)
                    if is_valid_location(board,col):
                        row= get_next_open_row(board,col)
                        drop_piece(board,row,col,PLAYER_1)
                        if winning_move(board,PLAYER_1):
                            # print("PLAYER 1 WINS!!")
                            label=win_font.render("PLAYER 1 WINS!!",1,RED)
                            screen.blit(label,(40,10))
                            game_over=True
                        turn+=1
                        turn=turn%2
                        print(board)
                        draw_board(board)
                #Player 2 turn    
        if turn ==AI and not game_over:
                    col=None
                    if difficulty=="easy":
                        col=random.randint(0,COL_COUNT-1)
                    #col=int(input("Player 2 make a selction from 0-6"))
                    #col=pick_best_move(board,PLAYER_AI)
                    elif difficulty=="medium":
                        col,new_score=minimax(board, 2,-math.inf,math.inf, True)
                    elif difficulty=="hard":
                        col,new_score=minimax(board, 4,-math.inf,math.inf, True)
                    elif difficulty=="expert":
                        col,new_score=minimax(board, 5,-math.inf,math.inf, True)
                    
                        
                    if is_valid_location(board,col):
                        pygame.time.wait(500)
                        row= get_next_open_row(board,col)
                        drop_piece(board,row,col,PLAYER_AI)
                        if winning_move(board,PLAYER_AI):
                            label=win_font.render("PLAYER 2 WINS!!",1,YELLOW)
                            screen.blit(label,(40,10))
                            game_over=True
                        turn+=1
                        turn=turn%2       
        #print(board)
        draw_board(board)
        if game_over==True:
                    pygame.time.wait(5000)
                    break       
    

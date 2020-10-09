# TIC TAC TOE by hriday Algh
#AI done by the Minimax algorithm, researched online.
board = [[0,0,0],
         [0,0,0],
         [0,0,0]]
# 2D array for board
screen = "start" # Current screen
turn = 1 # Turn 1 == X, 2 == O

def setup():
    size(700,700)
    global x,o
    x = loadImage("x.png")
    o = loadImage("o.png") # images
    imageMode(CENTER)
    rectMode(CENTER)
    noStroke()
    
def draw():
    global screen, board, turn
    if screen == "start":
        background(128,128,128) # grey
        textAlign(LEFT)
        fill(255,255,255)
        rect(350,350,600,600)
        fill(0,0,0)
        textSize(20)
        # instructions
        text("1. The game is played on a 3 by 3 grid of squares.\n2. 2 Players place X or O markers on empty \n    squares by taking turns.\n3. If you are playing vs AI, the AI is O.\n4. The first player too get 3 in a row, column, or diagonal \n    wins! Otherwise, it's a draw.\nIf you choose 1 Player, AI is O. Whoever goes first is random.\nThe AI is unbeatable, unless you go first :P.", 60, 100)
        textSize(70)
        textAlign(CENTER, CENTER)
        rect(350, 400, textWidth("2 Player"), 70) # rectangle for button
        fill(255,255,255)
        text("2 Player", 350, 400)# button text
        fill(0,0,0)
        rect(350, 500, textWidth("1 Player"), 70) # rectangle for button
        fill(255,255,255)
        text("1 Player", 350, 500) # button text
    if screen in ["AI", "1v1"]:
        background(128,128,128)
        fill(0,0,0)
        rect(350, 250, 600, 10)
        rect(350,450,600,10) # 4 lines for drawing board
        rect(250,350,10,600)
        rect(450,350,10,600)
        for p in range(3): # Use 2D for loop to draw out images based on board
            for q in range(3):
                if board[p][q] == 1:
                    image(x, q*200+150, p*200+150) # Draw x if 1
                if board[p][q] == 2:
                    image(o, q*200+150, p*200+150) # draw O if 2
        textSize(30)
        textAlign(CENTER,CENTER)
        if turn == 1:
            text("Turn: X", 200,675) # Thing that shows whos turn it is
        if turn == 2:
            text("Turn: O", 200, 675)
        winner = evaluate()
        if winner == 1:
            screen = 1
        if winner == 2:
            screen = 2
        if winner == None and not isMovesLeft(board):
            screen = 3
    if screen in range(1,4): # If there is a winner or tie
        global tex # no background function, so it writes the screen above the game ( so people can see how they won/lost)
        if screen == 3:
            tex = "It's a Tie"
        if screen == 1:
            tex = "Player 1 Wins!"
        if screen == 2:
            tex = "Player 2 Wins!"
        textAlign(CENTER,CENTER)
        fill(0,255,255)
        textSize(60)
        text(tex, 350,350)
        text("Go to home", 350,450) # This is meant to be a button
        
def mouseReleased():
    global screen, board, turn
    if screen == "start": # collision boxes for home screen buttons
        if mouseX in range(int(350-textWidth("2 Player")/2), int(350+textWidth("2 Player")/2)) and mouseY in range(400-35, 400+35):
            screen = "1v1"
            board = [[0,0,0],[0,0,0],[0,0,0]]
        if mouseX in range(int(350-textWidth("1 Player")/2), int(350+textWidth("1 Player")/2)) and mouseY in range(500-35, 500+35):
            screen = "AI"
            if int(random(2)) == 1:
                board = [[0,0,0],[0,0,0],[0,0,0]]
            else: 
                board = [[2,0,0],[0,0,0],[0,0,0]]
            turn = 1
    elif screen in ["1v1", "AI"]:
        for x in range(3): # double for loop to check every box if it was clicked on
            for y in range(3):
                if screen == "1v1" or (screen == "AI" and turn == 1): # if they are playing 1v1, or its AI but the players turn
                    if mouseX in range(x*200+50, x*200+250) and mouseY in range(y*200+50, y*200+250): 
                        # uses the double for loop to check all 9 boxes, no need to write 9 if statements
                        if board[y][x] == 0: # if box is empty, 
                            board[y][x] = turn # Do the move
                            if turn == 1: # Switch turn
                                turn = 2
                            elif turn == 2:
                                turn = 1
                        else:
                            return
                if screen == "AI" and turn == 2 and evaluate() != 1: # If it's the AIs turn
                    bestmov = bestMove(board)
                    board[bestmov[0]][bestmov[1]] = 2
                    turn = 1
                    return
    elif screen in range(1,4): # if Winner/Tie
        if mouseX in range(int(350-textWidth(tex)/2), int(350+textWidth(tex)/2)) and mouseY in range(450-35,450+35): # Go to Home button
            screen = "start" 

def isMovesLeft(b):
    # Is the board done
    for i in b:
        if 0 in i:
            return True
    return False

def evaluate():
    # A function that returns the winner, tie, or none.
    for i in range(3):
        if board[i] == [1,1,1]:
            return 1
        if board[i] == [2,2,2]:
            return 2
    
    for i in range(3):
        if [board[0][i], board[1][i], board[2][i]] == [1,1,1]:
            return 1
        if [board[0][i], board[1][i], board[2][i]] == [2,2,2]:
            return 2
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]
    return None

def bestMove(board):
    #Starts up the minimax recursion function for every possible move.
    #It returns the move with the best score.
    bestScore = -999999999999
    move = [-1,-1]
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, 0, False) # minimax every move
                board[i][j] = 0
                if score > bestScore:
                    bestScore = score
                    move = [i,j]
    return move

def minimax(board,depth,isMax):
    # Recursively goes through all possibilities, and scores it based on who
    # the winner was (and depth)
    result = evaluate()
    if result != None:
        # if game over, return the games score deppending on winner
        if result == 1:
            return -10 + depth
        if result == 2:
            return 10 - depth
    if isMax: # If AI's turn
        bestScore = -9999999
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minimax(board, depth+1,False) # Keep minimaxing every possible move and increse depth. Switch player turn as well
                    board[i][j] = 0
                    bestScore = max(score, bestScore) # We want to get the highest possible score between all moves
    else: # If humans turn
        bestScore = 999999999
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minimax(board, depth+1, True) # Minimax again
                    board[i][j] = 0
                    bestScore = min(score,bestScore) # the human will want the lowest possible score
    return bestScore
                
    

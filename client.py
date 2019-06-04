import socketio
import math as m
import random as r

tileRep = ["_", "X", "O"]

N = 8

letters = "abcdefgh"
numbers = "12345678"

def ix(row, col):
    return (row - 1) * N + letters.index(col)

def humanBoard(board):
    result = '   A  B  C  D  E  F  G  H'
    for i in range(0, len(board)):
        if i % N == 0:
            result += '\n\n ' + str(int(m.floor(i / N) + 1)) + ' '
        
        result += " " + tileRep[board[i]] + " "

    return result

def validateHumanPosition(position):
    validated = len(position) == 2

    if validated == True:
        row = int(position[0])
        col = position[1].lower()

        return (1 <= row and row <= N) and ('abcdefgh'.index(col) >= 0)

    return False

sio = socketio.Client()

sio.connect("http://127.0.0.1:4000")
userName = 'Rodrigo_X'
tournamentID = '12'

@sio.on('connect')
def on_connect():
    print("Conectado: " + userName)
    
    sio.emit('signin', {'user_name': userName, "tournament_id": tournamentID, "user_role": "player"})

@sio.on('ready')
def on_ready(data):
    print(humanBoard(data['board']))
    movement = " "
    choices = []
    for i in range(0, len(data['board'])):
        if data['board'][i] == 0:
            choices.append(i)
    choice = r.randint(0, len(choices)-1)
    print(choice)
    movement = choices[choice]
    '''
    while validateHumanPosition(movement) == False:
        randNum = r.randint(1,8)
        randLet = r.choice("ABCDEFGH")
        movement = str(randNum) + randLet
        choices.append(movement)
        '''
    print(movement)
    sio.emit('play', {'player_turn_id': data['player_turn_id'], "tournament_id": tournamentID, "game_id": data['game_id'], "movement": movement})

@sio.on('finish')
def on_finish(data):
    print("game has finished")
    sio.emit('player_ready', {'tournament_id': tournamentID, 'game_id': data['game_id'], 'player_turn_id': data['player_turn_id']})
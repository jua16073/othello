import math as m
import socket
import socketio
import random
import copy


HOST = '127.0.0.1'
PORT = 3000
userName = "Rodrigo_X2"
tournamentID = 12

depth = 1

tileRep = ['_', 'X', 'O']
N = 8
letters = "abcdefgh"
numbers = "12345678"

def ix(row, col):
  return(row-1)*N +letters.index(col)

def humanBoard(board):
  result = '   A  B  C  D  E  F  G  H'
  for i in range(0, len(board)):
      if i % N == 0:
          result += '\n\n ' + str(int(m.floor(i / N) + 1)) + ' '
      
      result += " " + tileRep[board[i]] + " "

  return result

def validateHumanPosition(position):
  validated = len(position) == 2
  
  if (validated):
    row = int(position[0])
    col = position[1].lower()

    return (1 <= row and row <= N) and ('abcdefgh'.index(col) >= 0);
  
  return False

sio = socketio.Client()
sio.connect("http://127.0.0.1:4000")
@sio.on('connect')
def on_connect():
  #Cliente Conectado
  print("Conectado "+ userName)

  # Entrar
  sio.emit('signin', {
    'user_name':userName,
    'tournament_id': tournamentID,
    'user_role': "player"
    })

@sio.on('ready')
def on_ready(data):
  print(humanBoard(data['board']));
  movement = " "

  (x, y) = bestMove(data['board'], data['player_turn_id'])
  print("x", x)
  print("y", y)
  movement = x + y *8
  print("movimiento ",movement)

  sio.emit('play', {
    'player_turn_id': data['player_turn_id'],
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'movement': movement
  })

@sio.on('finish')
def on_finish(data):
  print("Game ", data['game_id'], " has finished")
  print("Ready to play again!")
  sio.emit('player_ready', {
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'player_turn_id': data['player_turn_id'],
  })


dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]
maxEvalBoard = N * N + 4 * N +4 +1


def validMove(board, x, y, player):
  if x < 0 or x > N - 1 or y < 0 or y > N - 1:
        return False
  if board[y*8 + x] != 0:
      return False
  (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
  if totctr == 0:
      return False
  return True

def MakeMove(board, x, y, player): # assuming valid move
    totctr = 0 # total number of opponent pieces taken
    board[x+ y*8] = player
    for d in range(8): # 8 directions
        ctr = 0
        for i in range(N):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > N - 1 or dy < 0 or dy > N - 1:
                ctr = 0; break
            elif board[dy*8 +dx] == player:
                break
            elif board[dy * 8 + dx] == 0:
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            board[dy*8 + dx] = player
        totctr += ctr
    return (board, totctr)

def IsTerminalNode(board, player):
  for y in range(N):
      for x in range(N):
          if validMove(board, x, y, player):
              return False
  return True

def EvalBoard(board, player):
  tot = 0
  for y in range(N):
      for x in range(N):
          if board[x+y*8] == player:
              if (x == 0 or x == N - 1) and (y == 0 or y == N - 1):
                  tot += 4 # corner
              elif (x == 0 or x == N - 1) or (y == 0 or y == N - 1):
                  tot += 2 # side
              else:
                  tot += 1
  return tot


def swapPlayer(player):
  if player ==1:
    return 2
  else:
    return 1

    
#board, player, depth
def minimax(board,player, depth, maximizing):
  if depth == 0 or IsTerminalNode(board, player):
        return EvalBoard(board, player)
  if maximizing:
      bestValue = -1
      for y in range(N):
          for x in range(N):
              if validMove(board, x, y, player):
                  (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                  v = minimax(boardTemp, player, depth - 1, False)
                  bestValue = max(bestValue, v)
  else: # minimizingPlayer
      bestValue = maxEvalBoard
      for y in range(N):
          for x in range(N):
              if validMove(board, x, y, player):
                  (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                  v = minimax(boardTemp, player, depth - 1, True)
                  bestValue = min(bestValue, v)
  return bestValue

def bestMove(board, player):
  maxPoints = 0
  mx = -1
  my = -1
  depth = 2
  for y in range(N):
    for x in range(N):
      if validMove(board, x, y, player):
        (boardTemp, totCtr) = MakeMove(copy.deepcopy(board), x, y, player)
        points = minimax(boardTemp,player, depth, True)
        print("points", points)
        print("maxPoings", maxPoints)
        if points>maxPoints:
          mx = x
          my = y
          maxPoints = points
          print(mx," ", my)
  return (mx, my)
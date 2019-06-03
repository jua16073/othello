import math as m
import socket
import socketio
import random
import copy


HOST = '127.0.0.1'
PORT = 3000
userName = "Rodrigo_X"
tournamentID = 123

depth = 2

tileRep = ['_', 'X', 'O']
N = 8
letters = "abcdefgh"
numbers = "12345678"

def ix(row, col):
  return(row-1)*N +letters.index(col)

def humanBoard(board):
  result = '    A  B  C  D  E  F  G  H'
  for i in range(0, len(board)):
    if i % N == 0:
      result += '\n\n' + (int(m.floor(i/N)) + 1) + ' '
    
    result += ' '+ tileRep[board[i]] + ' '

  return result

def validateHumanPosition(position):
  validated = len(position) == 2
  
  if (validated):
    row = int(position[0])
    col = position[1].lower()

    return (1 <= row and row <= N) and ('abcdefgh'.indexOf(col) >= 0);
  
  return False

s = socketio.Client()
s.connect("http://127.0.0.1:3001")
@s.on('connect')
def on_connect():
  #Cliente Conectado
  print("Conectado "+ userName)

  # Entrar
  s.emit('signing', {
    'user_name':userName,
    'tournament_id': tournamentID,
    'user_role': "player"
    })

@s.on('ready')
def on_ready(data):
  print(humanBoard(data['board']));
  movement = " "

  x, y = bestMove(data['board'], data['player_turn_id'])
  movement = y+x
  #while not(validateHumanPosition(movement)):
    ##print("Insert your next move (1A - 8G:")
    ##movement = input()

  print(movement)
  s.emit('play', {
    'player_turn_id': data.player_turn_id,
    'tournament_id': tournamentID,
    'game_id': data.game_id,
    'movement': ix(int(movement[0]), movement[1].lower())
  })

  s.emit('play', {
    'player_turn_id': data.player_turn_id,
    'tournamentID': tournamentID,
    'game_id': data.game_id,
    'movement': ix(int(movement[0], movement[1].lower()))
  })

@s.on('finish')
def on_finish(data):
  print("Game "+ data.game_id + " has finished")
  print("Ready to play again!")
  s.emit('player_ready', {
    'tournament_id': tournamentID,
    'game_id': data.game_id,
    'player_turn_id': data.player_turn_id,
  })


dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]
maxEvalBoard = N * N + 4 * N +4 +1
def validMove(board, x, y, player):
  if validateHumanPosition(x+y):
    if (x+y) in board:
      return False
    else:
      return True
  return False

def makeMove(board, x, y, player):
  taken = 0
  pos_x = letters.indexOf(x)
  pos_y = 8 * y
  pos = pos_x + pos_y
  board[pos] = player
  for d in range(N):
    ctr =0
    for i in range(N):
      dx = pos_x + dirx[d] * (i + 1)
      dy = y + diry[d] * (i+1)

      if dx < 0 or dx > N - 1 or dy < 0 or dy > N - 1:
          ctr = 0; break
      elif board[(letters[dx] + (dy*8))] == player:
          break
      elif board[(letters[dx] + (dy*8))]== '0':
          ctr = 0; break
      else:
          ctr += 1
    for i in range(ctr):
      dx = pos_x + dirx[d] * (i + 1)
      dy = y + diry[d] * (i+1)
      board[(letters[dx] + (dy*8))] = player
    taken+= ctr
  return(board, taken)

#board, player, depth
def minimax(board, x, y, player, depth):
  
  if player == 1:
    bestValue = -1
    for y in range(N):
      for x in letters:
        if validMove(board, x, y, player):
          (boardTemp, totctr) = makeMove(copy.deepcopy(board), x, y, player)
          v = minimax(boardTemp, player, depth - 1, False)
          bestValue = max(bestValue)
  else: 
    bestValue = maxEvalBoard
    for y in range(N):
      for x in letters:
        if validMove(board, x, y, player):
          v = minimax(boardTemp, player, depth -1, True)
          bestValue = min(bestValue, v)
  return bestValue

def bestMove(board, player):
  maxPoints = 0
  mx = -1
  my = -1
  for y in range(N):
    for x in random(letters):
      if validMove(board, x, y, player):
        points = minimax(board, x, y, player)
      if points>maxPoints:
        mx = x
        my = y
  return (mx, my)
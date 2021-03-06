import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#2b8020", "headType": "fang", "tailType": "round-bum"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
  #  data = bottle.request.json
  #  boardInfo = (json.loads(data))
    boardInfo = bottle.request.json
    
    ## Interpret the board
    head = boardInfo['you']['body'][0]
    tempBoard = boardInfo['board']
    board = interpretBoard(tempBoard)
    board[head['x']][head['y']] = 0 # (our space is "clear", since we need to check for adjacent snake heads but obviously don't care about our own)
    
    ## See which moves are possible (IE do not result in instant death)
    moveOptions = []
    moveWeights = []
    if head['y'] > 0:
        if board[head['x']][head['y']-1] < 100:
            moveOptions.append("up")
            moveWeights.append(0)
    if head['y'] < (boardInfo['board']['height']-1):
        if board[head['x']][head['y']+1] < 100:
            moveOptions.append("down")
            moveWeights.append(0)
    if head['x'] > 0:
        if board[head['x']-1][head['y']] < 100:
            moveOptions.append("left")
            moveWeights.append(0)
    if head['x'] < (boardInfo['board']['width']-1):
        if board[head['x']+1][head['y']] < 100:
            moveOptions.append("right")
            moveWeights.append(0)
    
    move = "down"   # Default move
    
    
    if len(moveOptions) > 0:
        move = moveOptions[random.randint(0, len(moveOptions)-1)]
    
    shout = "I am a python snake at " + str(head['x']) + "," + str(head['y']) + " with " + str(len(moveOptions)) + " options "
    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def interpretBoard(boardInfo):
    board = [[-1 for i in range(boardInfo['height'])] for j in range(boardInfo['width'])] 
    for food in boardInfo['food']:
        board[food['x']][food['y']] = 1
    for snake in boardInfo['snakes']:
        snakeln = len(snake['body'])
        for segment in snake['body']:
            board[segment['x']][segment['y']] = 99 + snakeln    # It's 99+snakeln because I want the very tail end to be clear in ZERO turns; IE you can actually move into that square now
            if snakeln == len(snake['body']):
                board[segment['x']][segment['y']] += 100    # (it's a head! double it)
            snakeln -= 1
    return board

@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()

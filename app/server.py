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
        
    head = boardInfo['you']['body'][0]
    board = interpretBoard(boardInfo['board'], head['x'], head['y'])
    moveOptions = []
    if head['y'] > 0:
        if board[head['x']][head['y']-1] < 100:
            moveOptions.append('up')
    if head['y'] < (boardInfo['board']['height']-1):
        if board[head['x']][head['y']+1] < 100:
            moveOptions.append('down')
    if head['x'] > 0:
        if board[head['x']-1][head['y']] < 100:
            moveOptions.append('left')
    if head['x'] < (boardInfo['board']['width']-1):
        if board[head['x']+1][head['y']] < 100:
            moveOptions.append('right')
    
    move = moveOptions[randint(0, len(moveOptions)-1)]

    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def interpretBoard(boardInfo, headx, heady):
    board = [[-1 for i in range(boardInfo["height"])] for j in range(boardInfo["width"])] 
    for food in boardInfo["food"]:
        board[food["x"]][food["y"]] = 1
    for snake in boardInfo["snakes"]:
        snakeln = len(snake["body"])
        for segment in snake["body"]:
            board[segment["x"]][segment["y"]] = 100 + snakeln
            snakeln -= 1
    board[headx][heady] += 100
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

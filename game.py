import checkers
import agent
import sys
import mongo

# import player types
import slowpoke as sp
import magikarp as magi
import human

Black, White, empty = 0, 1, -1

"""
Displays the ASCII Board and other various information.
"""
def printStatus(B):
    print("--------")
    print (B)
    print(B.pdn)
    print(B.AIBoardPos)
    # print(B.moves())
    print("--------")

def playGame(black_player, white_player, options={}):
    B = checkers.CheckerBoard()
    current_player = B.active

    choice = 0
    # take as input agents.
    while not B.is_over():
        print(B)
        if  B.turnCount % 2 != choice:
            print("blacks turn")
            B.make_move(black_player.make_move(B, White))
        else:
            print("whites turn")
            B.make_move(white_player.make_move(B, Black))
        # If jumps remain, then the board will not update current player
        if B.active == current_player:
            print ("Jumps must be taken.")
            continue
        else:
            current_player = B.active

    print (B)
    B.getWinnerMessage()
    return B

def debugPrint(check, msg):
    if check:
        print(msg)

def generateDebugMsg(debug, moveCount, B):
    gameCountMsg = "Game: " + str(debug['gameCount']).zfill(2) + "/" + str(debug['totalGames']).zfill(2)
    moveMsg = "Move: " + str(moveCount).zfill(3) 
    GenerationMsg = "Gen: " + str(debug['genCount']).zfill(3) 
    PlayersMsg = "B: " + str(B.pdn['Black']) + " | W: " + str(B.pdn['White'])
    msg = [GenerationMsg, gameCountMsg, moveMsg, PlayersMsg]
    msg = ' | '.join(msg)
    debugPrint(debug['printDebug'], msg)

def tournamentMatch(blackCPU, whiteCPU, gameID="NULL", dbURI=False, debug=False, multiProcessing=False):
    # initiate connection to mongoDB
    # this is needed because pymongo screams if you init prior fork.
    db = mongo.Mongo()
    if dbURI != False:
        db.initiate(dbURI)

    # assign colours
    blackCPU.assignColour(Black)
    whiteCPU.assignColour(White)

    # initiate checkerboard.
    B = checkers.CheckerBoard()
    # set the ID for this game.
    B.setID(gameID)
    B.setColours(blackCPU.id, whiteCPU.id)

    # add the game to mongo.
    mongoGame_id = db.write('games', B.pdn)

    # set game settings
    current_player = B.active
    choice = 0
    # Start the game loop.
    while not B.is_over():
        # print move status.
        if debug != False:
            generateDebugMsg(debug, str(B.turnCount), B)

        # game loop!
        if  B.turnCount % 2 != choice:
            botMove = blackCPU.make_move(B, Black)
            B.make_move(botMove)
        else:
            botMove = whiteCPU.make_move(B, White)
            B.make_move(botMove)
        if B.active == current_player:
            # Jumps must be taken; don't assign the next player.
            continue
        else:
            current_player = B.active

        # print board.
        if debug != False:
            debugPrint(debug['printBoard'], B)
        # store the game to MongoDB.
        db.update('games', mongoGame_id, B.pdn)
    # once game is done, update the pdn with the results and return it.
    db.update('games', mongoGame_id, B.pdn)
    return B.pdn

# -----------

def main():
    # handlePlayerOption()
    # play2Player()
    print("You shouldn't be able to load this program directly. It is only called.")
    print("Terminating..")
    # slowpokeGame()

if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except KeyboardInterrupt:
        print ("Game terminated.")
        sys.exit(1)

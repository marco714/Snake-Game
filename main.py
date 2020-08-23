from game import Game
'''
    1.)Behavior:
        Game Over
            -snake hits the edge of the screen
            -snake touches itself
        
        Snake Movement:
            -body trails its head
        
        Snake:
            -Eats an apple, grows by one
        
        Score:
            -How much food has been eaten
    2.)constants
    3.)Data Definition
    4.)Function
'''
'''
#draw Window 
#update the game logic
#handle the input
#use the data to draw the graphics
    -clear the screen
    -update the game
    -draw the game
#clear the screen
'''
def main():
    game = Game()
    game.run()
    quit()

if __name__ == '__main__':

    main()


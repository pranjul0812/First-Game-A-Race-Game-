# Creating A basic game of saving your car from falling blocks/objects by moving left/right.
# Car should always remain within the game boundaries. boundary touch will be considered as crash.
# If any block touches the car from any side, it will be considered as a crash.
# If car dodged the falling blocks/objects successfully, user will get the points.
# Game displays the live scoring along with the overall HighScore.
# Game can be paused at any time and unpaused to start from the same state.
# Game can be restarted if crashed and live scoring will restart from 0.
# User can quit the game at any point by closing the game board or by pausing and quit.
# Game is having start and play sound along with crash sound.
# Game can be started/paused/unpaused/replay by the keyboard key spacebar also.


# Importing required packages
import pygame
import time
import random
import os

# Initialising the game
pygame.init()

# Defining the size of the game board
display_width = 800
display_length = 600

# Defining various color code(rgb) to use in the game for displaying various objects.
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lime = (0, 128, 0)
blue = (0, 0, 150)
green = (0, 200, 0)
bright_green = (0, 100, 0)
bright_blue = (0, 0, 100)
orange = (128, 90, 70)

# Creating the gameDisplay board to display our game board along with the caption.
gameDisplay = pygame.display.set_mode((display_width, display_length))
pygame.display.set_caption('Racey')

# Creating a Clock object to control the game runtime speed
clock = pygame.time.Clock()

# loading the car image in the game.
carImg = pygame.image.load('racecar.jpg')


# Defining the crash sound
crash_sound = pygame.mixer.Sound("crash.wav")


def car(x, y):
    # Creating a function to display our car image at (x,y) co-ordinates of the game board.
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    # Creating a function with text and font as parameter to show them with the required color(red) and font.
    text_surface = font.render(text, True, red)
    return text_surface, text_surface.get_rect()


def text_objects_white(text, font):
    # Creating a function with text and font as parameter to show them with the required color(white) and font.
    # Can merge this function with text_objects(with adding one more parameter for color)
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text):
    # Creating a function to display a large text
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), ((display_length / 2) - 25))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def things(thingx, thingy, thingw, thingh, color):
    # Creating a function to draw blocks/faliing objects taking color/length/width/(x,y)co-ordinates as parameters
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def button(x, y, button_width, button_height, text, bright_color, light_color, action=None):
    # Creating a function to display buttons on game board when required.
    # For ex:- when pause show 2 buttons continue and quit
    # Buttons are dynamic(change color when cursor is within the box and will do desired function when pressed
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (x + button_width) > mouse[0] > x and (y + button_height) > mouse[1] > y:
        pygame.draw.rect(gameDisplay, bright_color, [x, y, button_width, button_height])
        if click[0] == 1 and action != None:
                action()
    else:
        pygame.draw.rect(gameDisplay, light_color, [x, y, button_width, button_height])

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects_white(text, smallText)
    TextRect.center = ((x + (button_width/2)), (y + (button_height / 2)))
    gameDisplay.blit(TextSurf, TextRect)


def play():
    # Defining a play function to call another game_loop function(main game function) whenever called.
    game_loop()


def quitgame():
    # Defining a quitgame function to quit the game.
    # Whenever user will press the quit button this function will call
    pygame.quit()
    quit()


def pause():
    # Defining a pause function to pause the game along with the sound.
    # Pause function will display paused text along with 2 buttons continue and quit.
    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpause()
        message_display("Paused")
        button(150, 350, 100, 50, 'Continue', bright_green, green, unpause)
        button(550, 350, 100, 50, 'Quit', bright_blue, blue, quitgame)

        pygame.display.update()
        clock.tick(15)


def unpause():
    # Defining a unpause function to unpause the game along with the sound.
    # This function will be called when continue button will be pressed by user.
    global paused
    pygame.mixer.music.unpause()
    paused = False


def high_score(hs):
    # Function to display the high score in the gameDisplay.
    font = pygame.font.SysFont(None, 30)
    text = "High Score: " + str(hs)
    display = font.render(text, True, black)
    gameDisplay.blit(display, (635, 0))
    pygame.display.update()


def score(count):
    # Function to display the live score in the gameDisplay.
    scoring = count*5
    font = pygame.font.SysFont(None, 30)
    text = "Score: " + str(scoring)
    display = font.render(text, True, black)
    gameDisplay.blit(display, (0, 0))
    return scoring


def crash(finalscore, highscore):
    # Defining a crash function will be initiated whenever crash will occur.
    # A crash sound will be played along with the crashed display.
    # User will be asked to replay/quit the game after crashed
    # High score will be updated based on the final score before crashed.

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    if int(highscore) < finalscore:
        os.remove("score.txt")
        f = open("score.txt", 'w')
        f.write(str(finalscore))
        f.close()
    message_display("You Crashed")
    time.sleep(1)
    gameDisplay.fill(black)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        message_display("You Crashed")

        # Creating the button to display on crashed screen.
        button(150, 350, 100, 50, 'Replay', bright_green, green, play)
        button(550, 350, 100, 50, 'Quit', bright_blue, blue, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    # Defining a function to display the first screen of the game along with sound
    # Game_into will display game name along with two buttons to start/quit the game
    intro = True

    # Loading the sound
    pygame.mixer.music.load("piano.mp3")
    pygame.mixer.music.play(-1)

    # Checking the key press event.
    # If space bar is pressed will start the game
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        gameDisplay.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects("A Race Game", largeText)
        TextRect.center = ((display_width/2), (display_length/2)-25)
        gameDisplay.blit(TextSurf, TextRect)

        # Creating the button to display on Game_Intro screen
        button(150, 350, 100, 50, 'Go', bright_green, green, play)
        button(550, 350, 100, 50, 'Quit', bright_blue, blue, quitgame)

        # Updating the display
        pygame.display.update()
        clock.tick(15)


def game_loop():
    # Defining main game loop which will start once user will start the game after game_intro screen display.
    # Game will be played along with the game sound.
    global paused

    # Adding music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('police car.wav')
    pygame.mixer.music.play(-1)

    # Defining x and y to display initial car positions
    x = display_width * 0.45
    y = display_length * 0.7
    x_change = 0
    dodged = 0

    # Reading the high score of the game
    f = open("score.txt", 'r')
    hs = f.read()
    f.close()

    # randomising the falling blocks/objects position
    thing_startx = random.randrange(0, (display_width-90))
    thing_startx1 = random.randrange(0, (display_width-90))

    # defining other parameters for blocks/objects
    thing_starty = -600
    thing_Speed = 10
    thing_width = 80
    thing_height = 80

    # Checking if user is creating any event by pressing keyboard keys and performing function accordingly
    # If left key move car to left and if right key move car to right
    # If space bar or p is pressed pause the game.
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

                elif event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    paused = True
                    pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # creating the falling objects and blocks
        things(thing_startx, thing_starty, thing_width, thing_height, orange)
        things(thing_startx1, thing_starty, thing_width, thing_height, orange)
        thing_starty += thing_Speed
        car(x, y)
        final_score = score(dodged)
        high_score(hs)

        # Defining game display boundary crash conditions
        if x > (display_width-87) or x < 0:
            gameExit = True
            crash(final_score, hs)

        # If dodged successfully, update the live score and draw next blocks
        if thing_starty > display_length:
            thing_starty = 0 - thing_height
            dodged += 2
            thing_startx = random.randrange(0, (display_width-90))
            thing_startx1 = random.randrange(0, (display_width-90))

        # Defining game block/objects crash conditions
        if y+10 < (thing_starty+80):
            if x > thing_startx and  x < (thing_startx + 80) or (x + 87) > thing_startx and (x+87) < (thing_startx+90):
                gameExit = True
                crash(final_score, hs)
            elif x > thing_startx1 and  x < (thing_startx1 + 80) or (x + 87) > thing_startx1 and (x+87) < (thing_startx1+90):
                gameExit = True
                crash(final_score, hs)
        pygame.display.update()
        clock.tick(70)


# Calling the game_intro function to start the game
game_intro()
pygame.quit()
quit()

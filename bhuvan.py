import pygame
from pygame.locals import *
from timeit import default_timer as timer
import math
import random
fps = 30
# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
black = (0,0,0)
white = (255,255,255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126,178,255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)

textBoxSpace = 5
textBoxNumber = 0
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

def button(word,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))

    buttonText = pygame.font.Font("freesansbold.ttf",20)
    buttonTextSurf = buttonText.render(word, True, white)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(buttonTextSurf, buttonTextRect)

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)


# game variables
def hangman():
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        space = 10
        textBoxSpace = 5

        text = pygame.font.Font("freesansbold.ttf", 20)
        textSurf = text.render("Choose a catagory", True, black)
        textRect = textSurf.get_rect()
        textRect.center = ((WIDTH / 2), (HEIGHT / 2))
        screen.blit(textSurf, textRect)

        button("Animals", 150, 450, 150, 100, black, lightgrey, Animals)
        button("Vehicles", 550, 450, 150, 100, black, lightgrey, Vehicles)
        button("Food", 150, 50, 150, 100, black, lightgrey, Foods)
        button("Sports", 550, 50, 150, 100, black, lightgrey, Sports)

        pygame.display.update()
        clock.tick(fps)
        hangman_status = 0
        words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
        guessed = []
        word = random.choice(words)
        level = 1



def draw():
    win.fill(white)
    global level
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, black)
    name = WORD_FONT.render("level "+str(level),1, black)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    win.blit(name,(WIDTH/2 - text.get_width()/2 + 80,60))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, black)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, black, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, black)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    #win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(500)
    win.fill(white)
    text = WORD_FONT.render(message, 1, black)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)

def main():
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman!")
    clock = pygame.time.Clock()
    run = True
    global word
    global guessed
    global hangman_status
    global level
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            level += 1
            if level == 25:
                display_message("You are the CHAMPION")
            else:
                display_message("You WON!")
                #words.remove(word)
                #word = random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                draw()
                main()
            
            pygame.quit()

        if hangman_status == 6:
            display_message("You LOST!")
            pygame.quit()

def Animals():
    animal = [['cow', 'dog', 'cat', 'pig', 'fox'],['lion', 'bird', 'bear','panda', 'horse'],
              ['zebra','whale','tiger','shark','chicken'], ['giraffe', 'penguin', 'hamster',
               'cheetah', 'ostrich'], ['meerkat', 'monkey', 'octopus',
               'kitten', 'kangaroo']]
    print("animal")
    title = "Animals"
    #hangmanGame(animal, title)

def Vehicles():
    vehicle = [['car', 'bus','van', 'taxi','ship',],['tank', 'boat','bike','tram','train'],
               ['wagon','coach','plane', 'lorry','lorry'],['scooter', 'sleigh','rocket', 'caravan','tractor'],
               ['airplane', 'motorbike',   'ambulance', 'fire engine',  'spaceship']]
    print("vehicle")
    title = "Vehicles"
    #hangmanGame(vehicle, title)

def Foods():
    food = [['rice','cheese', 'soup', 'fish', 'egg'],['bread','nuts','apple','pasta', 'pizza'],
            ['chips','carrot', 'orange', 'peach', 'donut'], ['banana',  'cookie', 'potato', 'tomato', 'yogurt'],
            ['ice cream', 'pancake',   'cucumber','sweetcorn','sandwich']]
    print("food")
    title = "Foods"
    #hangmanGame(food, title)

def Sports():
    sport = [['rugby','golf','karate','tennis','cricket'],['football', 'netball', 'basketball', 'swimming','curling'],
             ['running','badmington', 'archery', 'volleyball', 'bowling'], ['dancing', 'skating', 'baseball',
             'rounders','boxing'], ['climbing', 'cycling', 'fencing',  'shooting','kabaddi']]
    print("sport")
    title = "Sports"
    #hangmanGame(sport, title)



while True:
    main()
pygame.quit()
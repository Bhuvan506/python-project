import pygame
from pygame.locals import *
from timeit import default_timer as timer
import math
import random
from timeit import default_timer as timer

FPS = 30

# setup display
pygame.init()
WIDTH, HEIGHT = 1000, 600
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


def button(word, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))

    buttonText = pygame.font.Font("freesansbold.ttf", 20)
    buttonTextSurf = buttonText.render(word, True, WHITE)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    win.blit(buttonTextSurf, buttonTextRect)


# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)

# game variables
hangman_status = 0
level = 1
LOSING_SOUND = pygame.mixer.Sound("C:/Users/jsbhu/OneDrive/Desktop/python-project/losing.wav")
WINNING_SOUND = pygame.mixer.Sound("C:/Users/jsbhu/OneDrive/Desktop/python-project/winning.wav")
pygame.mixer.music.load("C:/Users/jsbhu/OneDrive/Desktop/python-project/drums.wav")


def hangman():
    clock = pygame.time.Clock()
    win.fill(WHITE)
    textBoxSpace = 5

    text = pygame.font.Font("freesansbold.ttf", 20)
    textSurf = text.render("Choose a category", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ((WIDTH / 2), (HEIGHT / 2))
    win.blit(textSurf, textRect)

    button("Animals", 200, 450, 150, 100, BLACK, GREY, animals)
    button("Vehicles", 600, 450, 150, 100, BLACK, GREY, vehicles)
    button("Food", 200, 50, 150, 100, BLACK, GREY, foods)
    button("Sports", 600, 50, 150, 100, BLACK, GREY, sports)

    pygame.display.update()
    clock.tick(FPS)


def draw():
    win.fill(WHITE)
    global level
    # draw title
    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    name = WORD_FONT.render("level " + str(level), True, BLACK)
    chances = WORD_FONT.render("chances:" + str(10 - hangman_status), True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    win.blit(name, (WIDTH / 2 - text.get_width() / 2 + 80, 60))
    win.blit(chances, (WIDTH / 2 - text.get_width() / 2 + 40, 100))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    win.blit(text, (600, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    pygame.draw.rect(win, BLACK, [100, 350, 100, 10])
    pygame.draw.rect(win, BLACK, [200, 350, 100, 10])
    pygame.draw.rect(win, BLACK, [195, 100, 10, 250])
    pygame.draw.rect(win, BLACK, [100, 350, 100, 10])
    if hangman_status >= 1:
        pygame.draw.rect(win, BLACK, [195, 100, 75, 10])
    if hangman_status >= 2:
        pygame.draw.rect(win, BLACK, [270, 100, 75, 10])
    if hangman_status >= 3:
        pygame.draw.rect(win, BLACK, [265, 100, 10, 50])
    if hangman_status >= 4:
        pygame.draw.circle(win, BLACK, [270, 180], 30)
    if hangman_status >= 5:
        pygame.draw.rect(win, BLACK, [265, 210, 10, 40])
    if hangman_status >= 6:
        pygame.draw.rect(win, BLACK, [265, 250, 10, 40])
    if hangman_status >= 7:
        pygame.draw.line(win, BLACK, [270, 230], [230, 260], 10)
    if hangman_status >= 8:
        pygame.draw.line(win, BLACK, [270, 230], [310, 260], 10)
    if hangman_status >= 9:
        pygame.draw.line(win, BLACK, [270, 290], [230, 320], 10)
    if hangman_status >= 10:
        pygame.draw.line(win, BLACK, [270, 290], [310, 320], 10)
    pygame.display.update()


def display_message(message):
    pygame.time.delay(500)
    win.fill(WHITE)
    text = WORD_FONT.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)


def main(lst):
    fps = 60
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    run = True
    global hangman_status
    global level
    global word
    global guessed
    words = lst
    guessed = []
    if level <= 5:
        word = random.choice(words[0])
    elif level <= 10:
        word = random.choice(words[1])
    elif level <= 15:
        word = random.choice(words[2])
    elif level <= 20:
        word = random.choice(words[3])
    elif level <= 25:
        word = random.choice(words[4])
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    xx, yy, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((xx - m_x) ** 2 + (yy - m_y) ** 2)
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
            display_message("You WON!")
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(WINNING_SOUND)
            words.remove(word)
            word = random.choice(words)
            guessed = []
            for letter in letters:
                letter[3] = True
            if level == 26:
                display_message("You are the CHAMPION")
            if level <= 5:
                hangman_status = 1
                draw()
                main(words)
            elif level <= 10:
                hangman_status = 3
                draw()
                main(words)
            elif level <= 15:
                hangman_status = 5
                draw()
                main(words)
            elif level <= 20:
                hangman_status = 6
                draw()
                main(words)
            elif level <= 25:
                hangman_status = 7
                draw()
                main(words)

            pygame.quit()

        if hangman_status == 10:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(LOSING_SOUND)
            display_message("You LOST!")
            pygame.quit()


def animals():
    animal = [['cow', 'dog', 'cat', 'pig', 'fox'], ['lion', 'bird', 'bear', 'panda', 'horse'],
              ['zebra', 'whale', 'tiger', 'shark', 'chicken'], ['giraffe', 'penguin', 'hamster', 'cheetah', 'ostrich'],
              ['meerkat', 'monkey', 'octopus', 'kitten', 'kangaroo']]

    print("animal")
    main(animal)


def vehicles():
    vehicle = [['car', 'bus', 'van', 'taxi', 'ship'], ['tank', 'boat', 'bike', 'tram', 'train'],
              ['wagon', 'coach', 'plane', 'lorry', 'lorry'], ['scooter', 'sleigh', 'rocket', 'caravan', 'tractor'],
              ['airplane', 'motorbike',   'ambulance', 'fire engine',  'spaceship']]
    print("vehicle")
    main(vehicle)


def foods():
    food = [['rice', 'cheese', 'soup', 'fish', 'egg'], ['bread', 'nuts', 'apple', 'pasta', 'pizza'],
            ['chips', 'carrot', 'orange', 'peach', 'donut'], ['banana',  'cookie', 'potato', 'tomato', 'yogurt'],
            ['ice cream', 'pancake',   'cucumber', 'sweetcorn', 'sandwich']]
    print("food")
    main(food)


def sports():
    sport = [['rugby', 'golf', 'karate', 'tennis', 'cricket'], ['football', 'netball', 'basketball', 'swimming',
              'curling'], ['running', 'badminton', 'archery', 'volleyball', 'bowling'], ['dancing', 'skating',
              'baseball', 'rounders', 'boxing'], ['climbing', 'cycling', 'fencing',  'shooting', 'kabaddi']]
    print("sport")
    main(sport)


while True:
    hangman()
pygame.quit()
import pygame
from pygame.locals import *
from timeit import default_timer as timer
import math
import random

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

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images.
images = []
for i in range(7):
    
    image = pygame.image.load("/home/prasanth/c/python/project/image/hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
guessed = []
word = random.choice(words)
level = 1
LOSING_SOUND = pygame.mixer.Sound("python/project/losing.wav")
WINNING_SOUND = pygame.mixer.Sound("python/project/winning.wav")
pygame.mixer.music.load("python/project/drums.wav")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw():
    win.fill(WHITE)
    global level
    # draw title
    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    name = WORD_FONT.render("level "+str(level), True, BLACK)
    chances = WORD_FONT.render("chances:"+str(10-hangman_status), True, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    win.blit(name, (WIDTH/2 - text.get_width()/2 + 80, 60))
    win.blit(chances, (WIDTH/2 - text.get_width()/2 + 40, 100))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        xx, yy, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (xx, yy), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (xx - text.get_width()/2, yy - text.get_height()/2))

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
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)


def main():
    fps = 60
    pygame.mixer.music.play(-1)
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
                    xx, yy, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((xx - m_x)**2 + (yy - m_y)**2)
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
                hangman_status = 0
                draw()
                main()
            elif level <= 10:
                hangman_status = 2
                draw()
                main()
            elif level <= 15:
                hangman_status = 4
                draw()
                main()
            elif level <= 20:
                hangman_status = 6
                draw()
                main()
            elif level <= 25:
                hangman_status = 7
                draw()
                main()

        pygame.quit()


while True:
    main()
pygame.quit()

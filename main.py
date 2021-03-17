import pygame
from pygame.locals import *
from timeit import default_timer as timer
import math
import sys
import random
import os
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
    buttonTextSurf = buttonText.render(word, 1, WHITE)
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
score = 0
directory = os.getcwd()
LOSING_SOUND = pygame.mixer.Sound(directory + "/losing.wav")
WINNING_SOUND = pygame.mixer.Sound(directory + "/winning.wav")
pygame.mixer.music.load(directory + "/drums.wav")


def hangman():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock = pygame.time.Clock()
        win.fill(WHITE)
        textBoxSpace = 5

        text = pygame.font.Font("freesansbold.ttf", 20)
        textSurf = text.render("Choose a category", 1, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = ((WIDTH / 2), (HEIGHT / 2))
        win.blit(textSurf, textRect)

        button("Animals", 200, 450, 150, 100, BLACK, GREY, animals)
        button("PythonTAs", 600, 450, 150, 100, BLACK, GREY, pythonTAs)
        button("Subjects", 200, 50, 150, 100, BLACK, GREY, subjects)
        button("Professors", 600, 50, 150, 100, BLACK, GREY, professors)

        pygame.display.update()
        clock.tick(FPS)


def draw():
    win.fill(WHITE)
    global level
    global score
    # draw title
    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    name = WORD_FONT.render("Level " + str(level), True, BLACK)
    chances = WORD_FONT.render("Chances " + str(10 - hangman_status), True, BLACK)
    scores = WORD_FONT.render("Score: " + str(score), True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    win.blit(name, (WIDTH / 2 - text.get_width() / 2 + 80, 60))
    win.blit(chances, (WIDTH / 2 - text.get_width() / 2 + 40, 100))
    win.blit(scores, (WIDTH-text.get_width(), 50))

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
    wrong_guess = 0
    start = timer()
    fps = 60
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    run = True
    global hangman_status
    global level
    global word
    global guessed
    global score
    words = lst
    guessed = []
    word = random.choice(words)
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
            end = timer()
            level += 1
            if level == 6:
                timetaken = end - start
                display_message("Time taken: " + str(round(timetaken)) + "s")
                score += 1000 - (round(timetaken)) * 10 + (len(set(word))-len(guessed)) * 100 + level * 50
                display_message("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                display_message("Your Total Score: " + str(score))
                display_message("You are the CHAMPION")
                pygame.time.delay(6000)
            else:
                timetaken = end - start
                display_message("Time taken: " + str(round(timetaken)) + "s")
                score += 1000 - (round(timetaken))*10 + (len(set(word))-len(guessed))*100 + level*50
                display_message("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                pygame.time.delay(6000)
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                if level == 5:
                    hangman_status = 7
                    draw()
                    main(words)
                elif level == 4:
                    hangman_status = 6
                    draw()
                    main(words)
                elif level == 3:
                    hangman_status = 4
                    draw()
                    main(words)
                elif level == 2:
                    hangman_status = 2
                    draw()
                    main(words)
                elif level == 1:
                    hangman_status = 0
                    draw()
                    main(words)

            pygame.quit()

        if hangman_status == 10:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(LOSING_SOUND)
            display_message("You LOST!")
            display_message("Your Total Score: " + str(score))
            pygame.quit()


def animals():
    animal = ['COW', 'LION', 'HORSE', 'TIGER', 'CHICKEN']

    print("animal")
    main(animal)


def pythonTAs():
    pythonTA = ['PRATEEKSHA', 'ADVAITH', 'RAHUL', 'LUBIANA', 'KESHAV', 'ESHITHA']
    print("pythonTAa")
    main(pythonTA)


def subjects():
    subject = ['PYTHON', 'DIGITALDESIGN', 'MATHS', 'YOGA', 'ENGLISH']
    print("subjects")
    main(subject)


def professors():
    professor = ['SUBAJIT', 'RADHA', 'AMITH', 'SRIDHAR', 'NEHA', 'YASWANTH', 'SRINIVAS']
    print("Professors")
    main(professor)


while True:
    hangman()

pygame.quit()
exit()

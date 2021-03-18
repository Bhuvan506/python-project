import pygame
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
icon = pygame.image.load('hangman_icon.png')
pygame.display.set_icon(icon)

# fonts
OPTION_FONT = pygame.font.SysFont('georgia', 25)
LETTER_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('arial', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
END_FONT = pygame.font.SysFont('georgia', 50)


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
CYAN = (224, 255, 255)
GAINS = (220, 220, 220)
BLUE = (0, 206, 209)
PEACH = (255, 218, 185)
PURPLE = (128, 0, 128)
RED = (139, 0, 0)

# button variables
RADIUS = 23
GAP = 15
letters = []
startx = round((WIDTH - ((RADIUS * 2 + GAP) * 12 + RADIUS*2)) / 2)
starty = 450
A = 65
for i in range(26):
    x = startx + RADIUS + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


def button(word, x, y, w, h, c1, c2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, c2, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(win, c1, (x, y, w, h))
    pygame.mixer.Sound.play(CATEGORY_SOUND)
    buttonTextSurf = OPTION_FONT.render(word, True, WHITE)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    win.blit(buttonTextSurf, buttonTextRect)


# game variables
hangman_status = 0
level = 1
score = 0
directory = os.getcwd()
LOSING_SOUND = pygame.mixer.Sound(directory + "/losing.wav")
WINNING_SOUND = pygame.mixer.Sound(directory + "/winning.wav")
CATEGORY_SOUND = pygame.mixer.Sound(directory + "/wrong_guess.wav")
CORRECT_GUESS_SOUND = pygame.mixer.Sound(directory + "/correct_guess.wav")
WRONG_GUESS_SOUND = pygame.mixer.Sound(directory + "/wrong_guess.wav")
pygame.mixer.music.load(directory + "/game.wav")


def hangman():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock = pygame.time.Clock()
        win.fill(PEACH)

        textSurf = END_FONT.render("Choose a category", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = ((WIDTH / 2), (HEIGHT / 2))
        win.blit(textSurf, textRect)

        button("Team members", 200, 450, 200, 100, BLUE, GREY, members)
        button("PythonTAs", 600, 450, 200, 100, BLUE, GREY, pythonTAs)
        button("Subjects", 200, 50, 200, 100, BLUE, GREY, subjects)
        button("Professors", 600, 50, 200, 100, BLUE, GREY, professors)

        pygame.display.update()
        clock.tick(FPS)


def draw():
    win.fill(CYAN)
    global level
    global score
    # draw title
    text = TITLE_FONT.render("HANGMAN", True, RED)
    name = WORD_FONT.render("Level " + str(level), True, PURPLE)
    chances = WORD_FONT.render("Chances " + str(10 - hangman_status), True, PURPLE)
    scores = WORD_FONT.render("Score: " + str(score), True, PURPLE)
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
            pygame.draw.circle(win, RED, (x, y), RADIUS, 3)
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
    win.fill(PEACH)
    text = END_FONT.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)


def main(lst):
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
                            if ltr in word:
                                pygame.mixer.music.stop()
                                pygame.mixer.Sound.play(CORRECT_GUESS_SOUND)
                                pygame.time.delay(500)
                                pygame.mixer.Sound.stop(CORRECT_GUESS_SOUND)
                                pygame.mixer.music.play(-1)
                            if ltr not in word:
                                hangman_status += 1
                                pygame.mixer.music.stop()
                                pygame.mixer.Sound.play(WRONG_GUESS_SOUND)
                                pygame.time.delay(500)
                                pygame.mixer.Sound.stop(WRONG_GUESS_SOUND)
                                pygame.mixer.music.play(-1)

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
                pygame.time.delay(3000)
                pygame.mixer.Sound.stop(WINNING_SOUND)
            else:
                timetaken = end - start
                display_message("Time taken: " + str(round(timetaken)) + "s")
                score += 1000 - (round(timetaken))*10 + (len(set(word))-len(guessed))*100 + level*50
                display_message("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                pygame.time.delay(3000)
                pygame.mixer.Sound.stop(WINNING_SOUND)
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
            display_message("Correct word is: " + str(word))
            display_message("Your Total Score: " + str(score))
            pygame.quit()


def members():
    member = ['MAURYA', 'KEERTHAN', 'BHUVAN', 'OISHI', 'PRASANTH']
    print("Members in project")
    main(member)


def pythonTAs():
    pythonTA = ['PRATEKSHA', 'ADVAIT', 'RAHUL', 'LUBAIANA', 'KESHAV', 'ESHITA']
    print("PythonTAa")
    main(pythonTA)


def subjects():
    subject = ['PYTHON', 'DIGITALDESIGN', 'MATHS', 'YOGA', 'ENGLISH', 'PHYSICS', 'CHEMISTRY']
    print("Subjects")
    main(subject)


def professors():
    professor = ['SUBAJIT', 'SUJITH', 'RADHA', 'AMITH', 'SRIDHAR', 'NEHA', 'YASHVANTH', 'SRINIVAS', 'PRADEESHA']
    print("Professors")
    main(professor)


while True:
    hangman()

pygame.quit()
exit()

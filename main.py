import pygame
# from pygame.locals import *
# from timeit import default_timer as timer
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
    
    image = pygame.image.load("C:/Users/jsbhu/OneDrive/Desktop/python-project/hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
guessed = []
word = random.choice(words)
level = 1


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw():
    win.fill(WHITE)
    global level
    # draw title
    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    name = WORD_FONT.render("level "+str(level), True, BLACK)
    chances = WORD_FONT.render("chances:"+str(6-hangman_status), True, BLACK)
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

    win.blit(images[hangman_status], (150, 100))
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
            if level == 5:
                display_message("You are the CHAMPION")
            if level == 3:
                display_message("You WON!")
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                hangman_status = 4
                draw()
                main()
            else:
                display_message("You WON!")
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                hangman_status = 2
                draw()
                main()
            
            pygame.quit()

        if hangman_status == 6:
            display_message("You LOST!")
            pygame.quit()


while True:
    main()
# pygame.quit()

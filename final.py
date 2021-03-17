import pygame
import math
import random

pygame.init()

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")
icon = pygame.image.load('hangman-game.png')
pygame.display.set_icon(icon)

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# hangman images
images = []
for i in range(7):
    image_name = ("hangman" + str(i) + ".png")
    images.append(pygame.image.load(image_name))

# music
LOSING_SOUND = pygame.mixer.Sound("loss.wav")
WINNING_SOUND = pygame.mixer.Sound("win.wav")
pygame.mixer.music.load("music.mp3")

# game variable
hangman_status = 0
words = ["A", "AB", "ABC"]
word = random.choice(words)
guessed = []
level = 1
win_time = 0
# button variables
RADIUS = 20
GAP = 15
keyboard = []
startx = round((WIDTH - ((RADIUS * 2 + GAP) * 12 + 2 * RADIUS)) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + RADIUS + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    keyboard.append([x, y, chr(A + i), True])


def keyboard_buttons():
    for letter in keyboard:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, (0, 0, 0), (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, (0, 0, 0))
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


def word_guess():
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + ""
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, (0, 0, 0))
    screen.blit(text, (400, 200))


def display_text(message):
    pygame.time.delay(500)
    screen.fill((255, 255, 255))
    text = WORD_FONT.render(message, 1, (0, 0, 0))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)


def draw():
    screen.fill(WHITE)
    global level
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    name = WORD_FONT.render("level " + str(level), 1, BLACK)
    chances = WORD_FONT.render("chances:" + str(6 - hangman_status), 1, BLACK)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    screen.blit(name, (WIDTH / 2 - text.get_width() / 2 + 80, 60))
    screen.blit(chances, (WIDTH / 2 - text.get_width() / 2 + 40, 100))

    word_guess()
    keyboard_buttons()

    screen.blit(images[hangman_status], (150, 100))
    pygame.display.update()


# Game Loop
def main():
    FPS = 60
    clock = pygame.time.Clock()
    global word
    global guessed
    global hangman_status
    global level

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            clock.tick(FPS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in keyboard:
                    x, y, ltr, visible = letter
                    if visible:
                        distance = math.sqrt((m_x - x) ** 2 + (m_y - y) ** 2)
                        if distance < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        win = True
        for letter in word:
            if letter not in guessed:
                win = False
                break

        if win:
            level += 1
            pause = 1
            if level == 4:
                display_text("You are the CHAMPION!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                pygame.quit()
                break
            if level == 3:
                display_text("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in keyboard:
                    letter[3] = True
                hangman_status = 4
                draw()
                main()
            else:
                display_text("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in keyboard:
                    letter[3] = True
                hangman_status = 2
                draw()
                main()

            pygame.quit()

        if hangman_status == 6:
            display_text("YOU LOST")
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(LOSING_SOUND)
            pygame.quit()


while True:
    main()

pygame.quit()
quit()
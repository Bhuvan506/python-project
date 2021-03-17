import pygame
import math
import random


# setup display
pygame.init()
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")
FPS = 60

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
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["A", "AB", "ABC"]
guessed = []
word = random.choice(words)
level = 1
LOSING_SOUND = pygame.mixer.Sound("loss.wav")
WINNING_SOUND = pygame.mixer.Sound("win.wav")
pygame.mixer.music.load("music.mp3")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
black = (0,0,0)
white = (255,255,255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126,178,255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)


def Animals():
    animal = ['cow', 'dog', 'cat']
    print("animal")
    title = "Animals"
    #hangmanGame(animal, title)
    main(animal, title)

def Vehicles():
    vehicle = ['car', 'bus', 'train']
    print("vehicle")
    title = "Vehicles"
    #hangmanGame(vehicle, title)
    main(vehicle, title)

def Foods():
    food = ['apple', 'banana', 'orange']
    print("food")
    title = "Foods"
    #hangmanGame(food, title)
    main(food, title)

def Sports():
    sport = ['rugby', 'football', 'netball']
    print("sport")
    title = "Sports"
    #hangmanGame(sport, title)
    main(sport, title)

def button(word,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win,ic,(x,y,w,h))

    buttonText = pygame.font.Font("freesansbold.ttf",20)
    buttonTextSurf = buttonText.render(word, True, WHITE)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    win.blit(buttonTextSurf, buttonTextRect)

def draw():
    win.fill(WHITE)
    global level
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    name = WORD_FONT.render("level " + str(level), 1, BLACK)
    chances = WORD_FONT.render("chances:" + str(6 - hangman_status), 1, BLACK)
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
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(500)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)

def main2():
    global clock, win, play
    play = True
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman!")

    while True:
        hangman()

def hangman():
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        win.fill(white)
        space = 10
        textBoxSpace = 5

        text = pygame.font.Font("freesansbold.ttf", 20)
        textSurf = text.render("Choose a catagory", True, black)
        textRect = textSurf.get_rect()
        textRect.center = ((WIDTH / 2), (HEIGHT / 2))
        win.blit(textSurf, textRect)

        button("Animals", 150, 450, 150, 100, black, lightgrey, Animals)
        button("Vehicles", 550, 450, 150, 100, black, lightgrey, Vehicles)
        button("Food", 150, 50, 150, 100, black, lightgrey, Foods)
        button("Sports", 550, 50, 150, 100, black, lightgrey, Sports)

        pygame.display.update()
        clock.tick(FPS)

def main(category, title):

    pygame.mixer.music.play(-1)
    FPS = 60
    clock = pygame.time.Clock()

    global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start


    pick = random.choice(category)
    pickSplit = [pick[i:i + 1] for i in range(0, len(pick), 1)]

    win.fill(white)

    run = True
    global word
    global guessed
    global hangman_status
    global level
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
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
            if level == 4:
                display_message("You are the CHAMPION")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)

            if level == 3:
                display_message("You WON!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WINNING_SOUND)
                words.remove(word)
                word = random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                hangman_status = 4
                draw()
                main()
            else:
                if level == 4:
                    pygame.quit()
                else:
                    display_message("You WON!")
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(WINNING_SOUND)
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
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(LOSING_SOUND)
            display_message("You LOST!")

            pygame.quit()


if __name__ == "__main__":
    main2()
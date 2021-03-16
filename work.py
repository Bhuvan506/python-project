import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

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
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)


def draw():
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

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
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
            display_message("You WON!")
            break

        if hangman_status == 6:
            display_message("You LOST!")
            break


def Animals():
    animal = ['cow', 'dog', 'cat', 'pig', 'zebra', 'bird', 'giraffe', 'lion', 'tiger', 'penguin', 'hamster', 'fox',
              'panda', 'bear', 'cheetah', 'ostrich', 'meerkat', 'whale', 'shark', 'horse', 'monkey', 'octopus',
              'kitten', 'kangaroo', 'chicken', 'fish', 'rabbit', 'sheep']
    print("animal")
    title = "Animals"
    hangmanGame(animal, title)


def Vehicles():
    vehicle = ['car', 'bus', 'train', 'airplane', 'plane', 'ship', 'jet', 'boat', 'lorry', 'tractor', 'bike',
               'motorbike', 'tram', 'van', 'ambulance', 'fire engine', 'rocket', 'taxi', 'caravan', 'coach', 'lorry',
               'scooter', 'sleigh', 'tank', 'wagon', 'spaceship']
    print("vehicle")
    title = "Vehicles"
    hangmanGame(vehicle, title)


def Foods():
    food = ['apple', 'banana', 'orange', 'peach', 'pizza', 'donut', 'chips', 'sandwich', 'cookie', 'cucumber', 'carrot',
            'sweetcorn', 'ice cream', 'pancake', 'bread', 'potato', 'tomato', 'nuts', 'yogurt', 'pasta', 'rice',
            'cheese', 'soup', 'fish', 'egg', 'meat', 'ham', 'sausage']
    print("food")
    title = "Foods"
    hangmanGame(food, title)


def Sports():
    sport = ['rugby', 'football', 'netball', 'basketball', 'swimming', 'hockey', 'curling', 'running', 'golf', 'tennis',
             'badmington', 'archery', 'volleyball', 'bowling', 'dancing', 'gym', 'skating', 'baseball', 'rounders',
             'boxing', 'climbing', 'canoe', 'cycling', 'fencing', 'karate', 'shooting', 'cricket']
    print("sport")
    title = "Sports"
    hangmanGame(sport, title)


while True:
    main()

pygame.quit()
sys.exit()
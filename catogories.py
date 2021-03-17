import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")


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
guessed = []
words = []
# word = random.choice(words)
level = 1
LOSING_SOUND = pygame.mixer.Sound("losing.wav")
WINNING_SOUND = pygame.mixer.Sound("winning.wav")
pygame.mixer.music.load("drums.wav")

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)


def draw(word):
    win.fill(WHITE)
    global level
    
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
        
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    name = WORD_FONT.render("level "+str(level),1, BLACK)
    chances = WORD_FONT.render("chances:"+str(6-hangman_status),1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    win.blit(name,(WIDTH/2 - text.get_width()/2 + 80,60))
    win.blit(chances,(WIDTH/2 - text.get_width()/2 + 40,100))
    
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

catogories = {'Animals':['cow','dog','cat','pig','zebra','bird','giraffe','lion','tiger','penguin','hamster','fox','panda','bear','cheetah','ostrich','meerkat','whale','shark','horse','monkey','octopus','kitten','kangaroo','chicken','fish','rabbit','sheep'],
'Vehicles':['car','bus','train','airplane','plane','ship','jet','boat','lorry','tractor','bike','motorbike','tram','van','ambulance','fire engine','rocket','taxi','caravan','coach','lorry','scooter','sleigh','tank','wagon','spaceship'],
'Foods':['apple','banana','orange','peach','pizza','donut','chips','sandwich','cookie','cucumber','carrot','sweetcorn','ice cream','pancake','bread','potato','tomato','nuts','yogurt','pasta','rice','cheese','soup','fish','egg','meat','ham','sausage'],
'Sports':['rugby','football','netball','basketball','swimming','hockey','curling','running','golf','tennis','badmington','archery','volleyball','bowling','dancing','gym','skating','baseball','rounders','boxing','climbing','canoe','cycling','fencing','karate','shooting','cricket']}


def display_message(message):
    pygame.time.delay(500)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)

def game(words):
    pygame.mixer.music.play(-1)
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    word=random.choice(words)
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
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw(word)

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
                word= random.choice(words)
                guessed = []
                for letter in letters:
                    letter[3] = True
                hangman_status = 4
                draw()
                game()
            else:
                if level == 4 :
                    pygame.quit()
                else:
                    display_message("You WON!")
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(WINNING_SOUND)
                    words.remove(word)
                    word= random.choice(words)
                    guessed = []
                    for letter in letters:
                        letter[3] = True
                    hangman_status = 2
                    draw()
                    game()
            
            pygame.quit()

        if hangman_status == 6:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(LOSING_SOUND)
            display_message("You LOST!")

            pygame.quit()
    


def main():
    global word
    global guessed
    global hangman_status
    global words
    global level
    win.fill(WHITE)
    Animals = TITLE_FONT.render("Animals", 1, BLACK)
    Vechiles = TITLE_FONT.render("Vechiles", 1, BLACK)
    Foods = TITLE_FONT.render("Foods", 1, BLACK)
    Sports = TITLE_FONT.render("Sports", 1, BLACK)
    win.blit(Animals, (WIDTH/2 - Animals.get_width()/2-200, 40))
    win.blit(Vechiles, (WIDTH/2 - Vechiles.get_width()/2+200, 40))
    win.blit(Foods, (WIDTH/2 - Foods.get_width()/2-200, HEIGHT-40))
    win.blit(Sports, (WIDTH/2 - Sports.get_width()/2+200, HEIGHT-40))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            if m_x >width/2 -200 - Animals.get_width() and m_x < width/2 -200:
                if m_y >40 and m_y < Animals.get_height():
                    words = catogories['Animals']
            if m_x >width/2 +200 - Vechiles.get_width() and m_x < width/2 -200:
                if m_y >40 and m_y < Vechiles.get_height():
                    words = catogories['Vechiles']
            if m_x >width/2 -200 - Foods.get_width() and m_x < width/2 -200:
                if m_y <Height-40 and m_y < height-40-Foods.get_height():
                    words = catogories['Foods']
            if m_x >width/2 +200 - Sports.get_width() and m_x < width/2 +200:
                if m_y <Height-40 and m_y < height-40-Sports.get_height():
                    words = catogories['Sports']
            else:
                main()
        else:
            print("Mouse not clicked")
            
    game(words)

while True:
    main()
pygame.quit()

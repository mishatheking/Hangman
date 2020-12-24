import pygame
import math
import random
from words import words


# setting up display
# initializing pygame
pygame.init()

# fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)  # (font name,font size)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
HINT_FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)
WIDTH, HEIGHT = 800, 500
FPS = 60  # frames per second(games speed)
clock = pygame.time.Clock()
# run = True
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
playon = True


def main():
    global LETTER_FONT, WORD_FONT, TITLE_FONT, WIDTH, HEIGHT, FPS, clock, win, WHITE, BLACK, playon
    RADIUS = 20
    GAP = 15
    letters = []
    A = 65  # letters are defined by number and A is 65
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400  # doesnt have to be perfectly centered
    # this for loop will determine the x and y positions of each btn and where to draw them
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        # (i % 13) gives us the remainder of i,when i == 13 the value begins at 0 ie. the start point
        # GAP * 2 ensures we stay a lil bit offset from the edge of the screen
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

    # load images
    images = []
    for i in range(7):  # loads our images automatically
        image = pygame.image.load("hangman" + str(i) + ".png")
        images.append(image)

        # game variables
    hangman_status = 0
    word = random.choice(words).upper()
    guessed = []

    def draw():
        win.fill(WHITE)  # assigning a colour to our display screen
        # draw title
        text = TITLE_FONT.render("MISHA'S HANGMAN", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 15))

        # draw word

        display_word = ""
        for letter in word:
            if letter in guessed:
                display_word += letter + " "
            elif letter == " ":
                display_word += " " + " "
            else:
                display_word += "_ "
            text = WORD_FONT.render(display_word, 1, BLACK)
            win.blit(text, (400, 250))
            if hangman_status == 6:
                text = HINT_FONT.render(f"The word was {word}", 1, BLACK)
                win.blit(text, (400, 100))
                pygame.time.delay(2000)
            #if hangman_status >= 3:
            #    text = HINT_FONT.render("Hint \n try hard oga", 1, BLACK)
            #    win.blit(text, (400, 100))


        # drawing buttons
        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(win, BLACK, (x, y), RADIUS,3)  # (where,color,position,raius,width for circles boader)
                text = LETTER_FONT.render(ltr, 1, BLACK)
                win.blit(text, (x - text.get_width() / 2, y - (text.get_height() / 2) + 3))
                # blit simply means draw
        win.blit(images[hangman_status], (130, 100))  # (what to draw ,(coordinate to be drawn at))
        pygame.display.update()  # this will update the screen with the most recent things that we have drawn on it

    def display_message(message):
        pygame.time.delay(500)
        win.fill(WHITE)
        text = WORD_FONT.render(message, 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(600)

    run = True
    while run:
        # giving aid
        if len(guessed) < 1:
            if len(word) > 7:
                count = 2
                while count != 0:
                    aid = random.choice(word)  # gets the len of the word
                    if aid not in guessed:
                        guessed.append(aid)
                        count -= 1
                    else:
                        pass
            if len(word) <= 7:
                aid = random.choice(word)  # gets the len of the word
                guessed.append(aid)

        # ensuring our clock runs at the speed we initially set
        clock.tick(FPS)
        for events in pygame.event.get():  # checking for possible events
            if events.type == pygame.QUIT:
                pygame.quit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                # for collision we simply check if the mouse is in the button's radius range
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dist = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dist < RADIUS:
                            letter[3] = False
                            if " " in word:
                                guessed.append(" ")
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
            display_message("Correct! Go Again")
            break

        if hangman_status == 6:
            display_message("You LOST!")
            break


while True:
    main()
pygame.quit()

# as hint show few from the unchosen letters

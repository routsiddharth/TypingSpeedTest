import pygame, random, time

pygame.init()

MAX_FPS = 30
clock = pygame.time.Clock()
pygame.display.set_caption('Level999 - A Typing Test Anytime, Anywhere')

WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 102, 0, 255)
LIME = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
YELLOW = (255, 255, 0, 255)

dark_mode = False

if dark_mode == True:
    PRIMARY = BLACK
    SECONDARY = WHITE
else:
    PRIMARY = WHITE
    SECONDARY = BLACK

FONT_S = pygame.font.Font('Roboto_Mono/RM.ttf', 30)
FONT_M = pygame.font.Font('Roboto_Mono/RM.ttf', 45)
FONT_L = pygame.font.Font('Roboto_Mono/RM.ttf', 60)

LOGO = pygame.transform.scale(pygame.image.load("Images/logo.png"), (150, 150))
TITLE = pygame.image.load("Images/title.png")

LIGHTMODE = pygame.image.load("Images/light.png")
DARKMODE = pygame.image.load("Images/dark.png")

TEXT_HEIGHT = FONT_M.render("yeet.", 1, SECONDARY).get_height() + 10
NUM_WORDS = 10

status = "menu"
running = True

chosen = ""
typed = ""

see_words = MAX_FPS * 10
level_barriers = [(10*i)**3 for i in range(1001)]

f = open("xp.txt", "r")

for row in f:
    xp = int(row.strip())

f.close()

user_scores = []

f = open("user_scores.txt", "r")

for row in f:
    user_scores.append(float(row.strip()))

f.close()

def wrap(text, w = WIDTH - 30):
    words = {word: FONT_S.render(word, 1, SECONDARY).get_width() for word in text.split(" ")}

    lines = [""]

    space_len = FONT_S.render(" ", 1, SECONDARY).get_width()

    for word in words.keys():

        if FONT_S.render(lines[-1], 1, SECONDARY).get_width() + space_len + words[word] < w and len(lines) >= 1:

            lines[-1] = lines[-1] + " " + word

        else:

            s = " " + word
            lines.append(s)

    return lines


def draw():
    global chosen
    global see_words
    global typed
    global status
    global done
    global play_menu_button

    if status == "game":
        window.fill(PRIMARY)

        words = wrap(typed)

        w = words[-2::] if len(words) > 2 else words

        for i in range(len(w)):
            t = w[i].replace("I", "i")
            t = FONT_S.render(t, 1, SECONDARY)

            xpos = 20
            ypos = (TEXT_HEIGHT * i) + 20

            window.blit(t, (xpos, ypos))

        ypos = (3 * TEXT_HEIGHT) + 20
        xpos = 0

        width = WIDTH
        height = HEIGHT - ((3 * TEXT_HEIGHT) + 20)

        pygame.draw.rect(window, SECONDARY, (xpos, ypos, width, height))

        ypos = ((3 * TEXT_HEIGHT) + 20) - 20
        xpos = 0

        width = round((done / 100) * WIDTH)
        height = 20

        pygame.draw.rect(window, GREEN, (xpos, ypos, width, height))

        words = wrap(chosen)

        for i in range(len(words)):
            text = words[i].replace("I", "i")
            text = FONT_S.render(text, 1, PRIMARY)

            xpos = 20
            ypos = (TEXT_HEIGHT * i) + ((3 * TEXT_HEIGHT) + 40)

            window.blit(text, (xpos, ypos))

    elif status == "review":

        window.fill(PRIMARY)

        chosen = chosen.strip()
        typed = typed.strip()

        acc = accuracy(chosen, typed)

        t = FONT_M.render(f"Accuracy: {acc}%", 1, SECONDARY)

        xpos = WIDTH/2 - t.get_width()/2
        ypos = 20

        window.blit(t, (xpos, ypos))

        t = FONT_M.render(f"WPM: {wpm}", 1, SECONDARY)

        xpos = WIDTH/2 - t.get_width()/2
        ypos = 20 + 1*TEXT_HEIGHT

        window.blit(t, (xpos, ypos))

        t = FONT_M.render(f"Time Taken: {round(sec, 2)} sec", 1, SECONDARY)

        xpos = xpos = WIDTH/2 - t.get_width()/2
        ypos = 20 + 2 * TEXT_HEIGHT

        window.blit(t, (xpos, ypos))

        current_level = 0

        while True:
            if xp > level_barriers[current_level]:
                current_level += 1
            else:
                break

        full_bar = WIDTH - 100
        xp_in_level = xp - level_barriers[current_level-1]
        total_xp_in_level = level_barriers[current_level] - level_barriers[current_level-1]

        perc_filled = round(xp_in_level/total_xp_in_level, 2)
        length_bar = round(full_bar*perc_filled, 0)

        t = FONT_M.render(f"Level {current_level}: {xp_in_level}/{total_xp_in_level}", 1, SECONDARY)

        xpos = WIDTH/2 - t.get_width()/2
        ypos = 20 + 4 * TEXT_HEIGHT

        window.blit(t, (xpos, ypos))

        xpos = 50
        ypos = 20 + 5 * TEXT_HEIGHT

        width = full_bar
        height = 50

        pygame.draw.rect(window, SECONDARY, (xpos, ypos, width, height))

        xpos = 50
        ypos = 20 + 5 * TEXT_HEIGHT

        height = 50
        width = length_bar

        pygame.draw.rect(window, LIME, (xpos, ypos, width, height))

        if len(user_scores) > 15:
            user_score = round(sum(user_scores[-15::]) / 15, 2)
        else:
            user_score = round(sum(user_scores)/len(user_scores), 2)

        t = FONT_M.render(str(user_score), 1, SECONDARY)

        xpos = WIDTH/2 - t.get_width()/2
        ypos = 20 + 6 * TEXT_HEIGHT

        window.blit(t, (xpos, ypos))

        t = FONT_S.render("Press any button to play again.", 1, SECONDARY)

        xpos = WIDTH/2 - t.get_width()/2
        ypos = HEIGHT - (20 + t.get_height())

        window.blit(t, (xpos, ypos))

    elif status == "menu":

        window.fill(PRIMARY)

        if dark_mode == True:

            xpos = WIDTH - DARKMODE.get_width() - 10
            ypos = 10

            window.blit(DARKMODE, (xpos, ypos))

        else:

            xpos = WIDTH - LIGHTMODE.get_width() - 10
            ypos = 10

            window.blit(LIGHTMODE, (xpos, ypos))

        xpos = WIDTH/2 - LOGO.get_width()/2
        ypos = 50

        window.blit(LOGO, (xpos, ypos))

        xpos = 0
        ypos = 50 + LOGO.get_height() + 20

        window.blit(TITLE, (xpos,  ypos))

        t = FONT_L.render("PLAY", 1, PRIMARY)

        width = t.get_width() + 20
        height = t.get_height() + 20

        xpos = WIDTH/2 - width/2
        ypos = 400

        pygame.draw.rect(window, SECONDARY, (xpos, ypos, width, height))

        play_menu_button = [xpos, ypos, width, height]

        xpos = xpos + 10
        ypos = ypos + 10

        window.blit(t, (xpos, ypos))

    pygame.display.update()

def accuracy(chosen, typed):

    c = chosen.strip().split(" ")
    t = typed.strip().split(" ")

    accuracies = []

    if len(c) == len(t):
        extra = 0
    elif len(c) > len(t):
        extra = len(c) - len(t)
    else:
        extra = len(t) - len(c)

    for j in range(len(t)):

        word = c[j]
        typed_word = t[j]

        count = 0
        total = len(word)

        for i in range(len(word)):

            if not i > len(typed_word) - 1:
                if word[i] == typed_word[i]:
                    count += 1

        perc_accurate = (count/total)*100
        accuracies.append(perc_accurate)

    for _ in range(extra):
        accuracies.append(0)

    final_accuracy = round(sum(accuracies)/len(accuracies), 2)
    return final_accuracy

def new_game():

    global chosen
    global typed
    global start

    chosen = choose_words()
    typed = ""
    start = time.time()

def choose_words():

    file = open("wordlist.txt", "r")
    content = file.read()
    random_words = content.splitlines()
    file.close()

    returned = []

    while len(returned) < NUM_WORDS:
        word = random.choice(random_words)

        if len(word) > 1:
            returned.append(random.choice(random_words))
        else:
            pass

    return " ".join(returned) + "."

def end_game():

    global sec
    global xp
    global wpm
    global status
    global user_scores

    end = time.time()
    sec = end - start

    wpm = round(round(NUM_WORDS / sec, 5) * 60, 2)
    acc = accuracy(chosen, typed)

    xp_added = round(wpm*(acc) - (100 - acc)*wpm)

    if xp_added < 50:
        xp_added = 50
    elif xp_added > 10000:
        xp_added = 10000

    xp += xp_added

    f = open("xp.txt", "w")
    f.write(str(xp))
    f.close()

    score_barriers = {0:600, 30:800, 40:900, 50:1000, 60:1100, 70:1150, 80:1200, 90:1250, 100:1300, 110:1350,
                      120:1400, 130:1425, 140:1450, 150:1475, 160:1500, 170:1520, 180:1540, 190:1560,
                      200:1580, 210:1600, 190000:1601}

    score = [None, None]

    items = list(score_barriers.items())

    for i in range(len(items) - 1):
        required, sc = items[i]

        if wpm < required:
            required_next, score_next = items[i + 1]

            score_per_word = (score_next - sc)/(required_next - required)
            words_above = wpm - required

            score[0] = round(score_per_word * words_above) + sc

            break

    if score[0] == None:
        score[0] = 1600

    score[1] = round((acc/100) * 1600)
    final_score = round(sum(score)/len(score), 1)

    user_scores.append(final_score)

    f = open("user_scores.txt", "a")
    f.write(str(final_score) + "\n")
    f.close()

    status = "review"

while running:

    if dark_mode == True:
        PRIMARY = BLACK
        SECONDARY = WHITE

        LOGO = pygame.transform.scale(pygame.image.load("Images/logo_dark.png"), (150, 150))
    else:
        PRIMARY = WHITE
        SECONDARY = BLACK

        LOGO = pygame.transform.scale(pygame.image.load("Images/logo.png"), (150, 150))

    clock.tick(MAX_FPS)

    see_words -= 1

    if status == "game" and chosen == "":
        new_game()


    if status == "game":
        done = (len(typed.strip()) / len(chosen.strip())) * 100

    draw()

    if len(typed) >= 1 and status == "game":
        cond_1 = typed.strip()[-1] == "."

        if cond_1:
            end_game()


    for e in pygame.event.get():

        if e.type == pygame.QUIT:

            running = False

        elif e.type == pygame.KEYDOWN:

            keys = pygame.key.get_pressed()

            if status == "game":

                for letter in [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(46, 47)]:

                    if keys[ord(letter)]:
                        typed += letter

                if keys[pygame.K_SPACE]:
                    typed += " "

                if keys[pygame.K_BACKSPACE]:
                    typed = typed[:-1:]

            elif status == "review":

                status = "game"
                chosen = ""

        elif e.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            if status == "menu":

                xpos, ypos, width, height = play_menu_button

                if (mx > xpos and mx < xpos + width) and (my > ypos and my < ypos + height):

                    status = "game"
                    chosen = ""

                width = LIGHTMODE.get_width()
                height = LIGHTMODE.get_height()

                xpos = WIDTH - width - 10
                ypos = 10

                if (mx > xpos and mx < xpos + width) and (my > ypos and my < ypos + height):

                    if dark_mode == True:
                        dark_mode = False
                    else:
                        dark_mode = True

f.close()
pygame.quit()
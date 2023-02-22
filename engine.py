import pygame
from pygame import mixer

NAME = 'Tic Tac Toe'
ICON = pygame.image.load('images/icon.png')
X = pygame.image.load('images/x.png')
O = pygame.image.load('images/o.png')
WIDTH = 800
HEIGHT = 800
GRID_WIDTH = 60
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
LINE_THICKNESS = 6
LINE_LENGTH = 400
LINE_WIDTH = 400
GRID_SHIFT_VERTICAL = -100

BTN_WIDTH = 400
BTN_HEIGHT = 50
BTN_X = (WIDTH / 2) - (BTN_WIDTH / 2)
BTN_Y = 600
BTN_BORDER = 2

WHITE = (255, 255, 255)
MAROON = (128, 0, 0)

LINES = {
    'v1x': WIDTH/2 - GRID_WIDTH - LINE_THICKNESS,
    'v2x': WIDTH/2 + GRID_WIDTH + LINE_THICKNESS,
    'vy1': HEIGHT/2 - LINE_LENGTH/2 + GRID_SHIFT_VERTICAL,
    'vy2': HEIGHT/2 + LINE_LENGTH/2 + GRID_SHIFT_VERTICAL,
    'hx1': WIDTH/2 - LINE_WIDTH/2,
    'hx2': WIDTH/2 + LINE_WIDTH/2,
    'h1y': HEIGHT/2-GRID_WIDTH - LINE_THICKNESS + GRID_SHIFT_VERTICAL,
    'h2y': HEIGHT/2+GRID_WIDTH + LINE_THICKNESS + GRID_SHIFT_VERTICAL,
}

square_centers = {
    1: ((LINES['hx1']+LINES['v1x'])/2-32, (LINES['h1y']+LINES['vy1'])/2-32),
    2: ((LINES['v1x']+LINES['v2x'])/2-32, (LINES['h1y']+LINES['vy1'])/2-32),
    3: ((LINES['v2x']+LINES['hx2'])/2-32, (LINES['h1y']+LINES['vy1'])/2-32),
    4: ((LINES['hx1']+LINES['v1x'])/2-32, (LINES['h1y']+LINES['h2y'])/2-32),
    5: ((LINES['v1x']+LINES['v2x'])/2-32, (LINES['h1y']+LINES['h2y'])/2-32),
    6: ((LINES['v2x']+LINES['hx2'])/2-32, (LINES['h1y']+LINES['h2y'])/2-32),
    7: ((LINES['hx1']+LINES['v1x'])/2-32, (LINES['h2y']+LINES['vy2'])/2-32),
    8: ((LINES['v1x']+LINES['v2x'])/2-32, (LINES['h2y']+LINES['vy2'])/2-32),
    9: ((LINES['v2x']+LINES['hx2'])/2-32, (LINES['h2y']+LINES['vy2'])/2-32),
}


# Global Functions...
def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(NAME)
    pygame.display.set_icon(ICON)
    return screen


def play_hover_sound():
    mixer.init()
    mixer.music.load('sounds/effects/hover.mp3')
    mixer.music.play()


def get_square(x, y):
    if y < LINES['h1y'] and x < LINES['v1x']:
        return 1
    elif y < LINES['h1y'] and LINES['v1x'] < x < LINES['v2x']:
        return 2
    elif y < LINES['h1y'] and x > LINES['v2x']:
        return 3
    elif LINES['h1y'] < y < LINES['h2y'] and x < LINES['v1x']:
        return 4
    elif LINES['h1y'] < y < LINES['h2y'] and LINES['v1x'] < x < LINES['v2x']:
        return 5
    elif LINES['h1y'] < y < LINES['h2y'] and x > LINES['v2x']:
        return 6
    elif y > LINES['h2y'] and x < LINES['v1x']:
        return 7
    elif y > LINES['h2y'] and LINES['v1x'] < x < LINES['v2x']:
        return 8
    elif y > LINES['h2y'] and x > LINES['v2x']:
        return 9
    else:
        return None


def draw_line(window_object, line_color, starting_coor, ending_coor, thickness):
    pygame.draw.line(window_object, line_color, ending_coor, starting_coor, width=thickness)


def draw_grid(screen):
    draw_line(window_object=screen,
              line_color=LINE_COLOR,
              starting_coor=(LINES['v1x'], LINES['vy1']),
              ending_coor=(LINES['v1x'], LINES['vy2']),
              thickness=LINE_THICKNESS)
    draw_line(window_object=screen,
              line_color=LINE_COLOR,
              starting_coor=(LINES['v2x'], LINES['vy1']),
              ending_coor=(LINES['v2x'], LINES['vy2']),
              thickness=LINE_THICKNESS)
    draw_line(window_object=screen,
              line_color=LINE_COLOR,
              starting_coor=(LINES['hx1'], LINES['h1y']),
              ending_coor=(LINES['hx2'], LINES['h1y']),
              thickness=LINE_THICKNESS)
    draw_line(window_object=screen,
              line_color=LINE_COLOR,
              starting_coor=(LINES['hx1'], LINES['h2y']),
              ending_coor=(LINES['hx2'], LINES['h2y']),
              thickness=LINE_THICKNESS)


def place_signs(screen, plays):  # Draw the player symbols
    for key, val in plays.items():
        if val:  # draw x
            screen.blit(X, square_centers[key])
        else:
            screen.blit(O, square_centers[key])


def play(mouse_pos, turn, plays):  # Modify the (plays) dictionary...
    x = mouse_pos[0]
    y = mouse_pos[1]
    if (x >= LINES['hx1']) and (x <= LINES['hx2']):
        if (y >= LINES['vy1']) and (y <= LINES['vy2']):
            if get_square(x, y) and get_square(x, y) not in plays.keys():
                plays[get_square(x, y)] = turn
                return not turn
    return turn


def sort_array(array):
    if len(array) != 3:
        raise ValueError('Only arrays of length three are permitted!')
    minimum = min(array)
    maximum = max(array)
    middle = 0
    for item in array:
        if item != minimum and item != maximum:
            middle = item
    return [minimum, middle, maximum]


def winner(plays, player=True):
    x_positions = list()
    if player:
        for key, val in plays.items():
            if val:
                x_positions.append(key)
    else:
        for key, val in plays.items():
            if not val:
                x_positions.append(key)
    x2_positions = dict()
    for i in range(len(x_positions)):
        for j in range(len(x_positions)):
            if x_positions[j] != x_positions[i]:
                try:
                    x2_positions[x_positions[i]].append(x_positions[j])
                except KeyError:
                    x2_positions[x_positions[i]] = list()
                    x2_positions[x_positions[i]].append(x_positions[j])
    x3_positions = dict()
    for key, val in x2_positions.items():
        for num in x2_positions[key]:
            for n in x_positions:
                if n != num and n != key:
                    try:
                        x3_positions[(key, num)].append(n)
                    except KeyError:
                        x3_positions[(key, num)] = list()
                        x3_positions[(key, num)].append(n)
    for key, val in x3_positions.items():
        for elem in val:
            if abs(key[0] - key[1]) == abs(key[1] - elem):
                check_array = [key[0], key[1], elem]
                check_array = sort_array(check_array)
                if check_array != [1, 3, 5] and check_array != [2, 4, 6] and check_array != [5, 7, 9]:
                    return player
    return None


def end_game(plays):  # Checks if the game ended (in a win or a draw)
    if winner(plays=plays):
        return 'X Won!'
    elif winner(plays=plays, player=False) is not None:
        return 'O Won!'
    else:
        if len(plays.keys()) == 9:
            return 'Draw...'
        else:
            return None


def mouse_over_btn(mouse_pos):
    x = mouse_pos[0]
    y = mouse_pos[1]
    if BTN_X <= x <= BTN_X + BTN_WIDTH:
        if BTN_Y <= y <= BTN_Y + BTN_HEIGHT:
            return True
    return False


def render_btn(screen, btn, btn_txt, btn_txt_rect, hovered=False):
    if hovered:
        pygame.draw.rect(screen, WHITE, btn)
        screen.blit(btn_txt, btn_txt_rect)
    else:
        pygame.draw.rect(screen, WHITE, btn, BTN_BORDER)
        screen.blit(btn_txt, btn_txt_rect)

from engine import *


def main():
    # PyGame setup...
    screen = setup()

    # Playing variables...
    turn = True
    plays = dict()

    # Main game loop...
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                turn = play(pygame.mouse.get_pos(), turn, plays)
                if end_game(plays) is not None:
                    running = False
                    game_over(end_game(plays), plays)
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        place_signs(screen, plays)

        pygame.display.update()


def game_over(winner, plays):
    # PyGame setup...
    screen = setup()

    # Game over variables...
    font = pygame.font.Font('fonts/jack_pirate/JackPirate_PERSONAL_USE_ONLY.ttf', 40)
    title = font.render(winner, True, WHITE)
    title_rect = title.get_rect(center=(WIDTH / 2, 40))

    btn = pygame.Rect(BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
    off_btn = True

    # Main loop...
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_over_btn(pygame.mouse.get_pos()):
                    running = False
                    main()
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        place_signs(screen, plays)
        screen.blit(title, title_rect)
        if mouse_over_btn(pygame.mouse.get_pos()):
            if off_btn:
                play_hover_sound()
                off_btn = False
            btn_txt = font.render('Play Again', True, MAROON)
            btn_txt_rect = btn_txt.get_rect(center=(BTN_X + BTN_WIDTH / 2, BTN_Y + BTN_HEIGHT / 2))
            render_btn(screen, btn, btn_txt, btn_txt_rect, hovered=True)
        else:
            off_btn = True
            btn_txt = font.render('Play Again', True, WHITE)
            btn_txt_rect = btn_txt.get_rect(center=(BTN_X + BTN_WIDTH / 2, BTN_Y + BTN_HEIGHT / 2))
            render_btn(screen, btn, btn_txt, btn_txt_rect)

        pygame.display.update()


if __name__ == "__main__":
    main()

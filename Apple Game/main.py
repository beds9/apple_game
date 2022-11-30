# made for game off 2022 game jam

# unfinished right now
# line 3 is not true if this game is finished now

import pygame

import ctypes

from constants import *

from classes import *

pygame.init()

ctypes.windll.user32.SetProcessDPIAware()

window = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()

sounds = {
"beep_eat": pygame.mixer.Sound("sounds\\beep_eat.wav"),
"lose": pygame.mixer.Sound("sounds\\lose.wav"),
"music": pygame.mixer.Sound("sounds\\music.wav")
}

# def get_game_over():
#     global game_over

#     return game_over

# def get_touch_apple():
#     global touch_apple

#     return touch_apple

player = pygame.sprite.GroupSingle(Player())
apple = pygame.sprite.GroupSingle(Apple(player))
doctor = pygame.sprite.GroupSingle(Doctor())
play_button = pygame.sprite.GroupSingle(PlayButton())

font = pygame.font.Font(None, 128)
small_font = pygame.font.Font(None, 48)

ouch = font.render("ouch", False, "white")
how_to_play_again = small_font.render("Press SPACEBAR to play again.", False, "white")
# how_to_play_go_to_title_screen = small_font.render("Press ESCAPE to go to title screen.", False, "white")
# how_to_play_to_title_screen = small_font.render("Press ESCAPE to go to title screen.", False, "white")
how_to_go_to_title_screen = small_font.render("Press ESCAPE to go to title screen.", False, "white")
title_part_0 = font.render("Apple", True, "red")
title_part_1 = font.render("Game", True, "deepskyblue4")

game_over = False
touch_apple = False

title_screen = True

area = "title_screen"

pygame.mouse.set_visible(False)

cursor_circle = pygame.image.load("sprites\\cursor_circle.png").convert_alpha()

apple_sprite = pygame.transform.scale_by(pygame.image.load("sprites\\apple.png").convert_alpha(), (4, 4))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if area == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        game_over = False
                        player = pygame.sprite.GroupSingle(Player())
                        apple = pygame.sprite.GroupSingle(Apple(player))
                        doctor = pygame.sprite.GroupSingle(Doctor())
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        play_button.sprite.area = "title_screen"
                        game_over = False
                        player = pygame.sprite.GroupSingle(Player())
                        apple = pygame.sprite.GroupSingle(Apple(player))
                        doctor = pygame.sprite.GroupSingle(Doctor())

    clock.tick(60)

    left_click = pygame.mouse.get_pressed()[0]

    if area == "game":
        if not game_over:
            player.update()
            apple.update()
            touch_apple = apple.sprite.touch_player
            doctor.update(player.sprite.rect, touch_apple)
            game_over = doctor.sprite.game_over

            if touch_apple:
                sounds["beep_eat"].play()

            if game_over:
                sounds["lose"].play()
            
            # reset_doctor_speed = apple.update()
            # if reset_doctor_speed:
            #     doctor.sprite.speed = 0.00125
            # game_over = doctor.update(player.sprite.rect)

            if apple.sprite:
                score = font.render("Score: {}".format(apple.sprite.score), False, "white")

        if game_over:
            window.fill(DARK_GRAY)
            window.blit(ouch, ouch.get_rect(center=(randint(958, 962), randint(538, 542))))
            window.blit(how_to_play_again, how_to_play_again.get_rect(center=(randint(959, 961), randint(269, 271))))
            window.blit(how_to_go_to_title_screen, how_to_go_to_title_screen.get_rect(center=(randint(959, 961), randint(809, 811))))

        if not game_over:
            window.fill("skyblue")# LIGHT_BLUE)
            apple.draw(window)
            doctor.draw(window)
            player.draw(window)
            window.blit(score, score.get_rect(center=(960, 135)))
            window.blit(cursor_circle, pygame.mouse.get_pos())
    
    if area == "title_screen":
        play_button.update(cursor_circle.get_rect(center=pygame.mouse.get_pos()), left_click)
        area = play_button.sprite.area
        window.fill("deepskyblue")
        window.blit(title_part_0, title_part_0.get_rect(center=(960, 270)))
        window.blit(title_part_1, title_part_1.get_rect(center=(960, 405)))
        window.blit(apple_sprite, apple_sprite.get_rect(center=(1140, 405)))
        play_button.draw(window)
        window.blit(cursor_circle, pygame.mouse.get_pos())

    area = play_button.sprite.area


    pygame.display.update()

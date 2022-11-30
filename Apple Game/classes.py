import pygame

from copy import deepcopy

from random import randint, random

# class SpriteFactory:
#     def __init__(self):
#         touch_apple = False
#         game_over = False
#         self.touch_apple = touch_apple
#         self.game_over = game_over

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("sprites\\player.png").convert_alpha(), (8, 8))
        self.position = pygame.math.Vector2((960, 810))
        self.rect = self.image.get_rect(center=self.position)
        self.velocity = [0, 0]
        # self.direction_to_move = int()
        self.mouse_position = pygame.mouse.get_pos()
    def update(self):
        self.mouse_position = pygame.mouse.get_pos()

        # self.position = self.position.move_towards(self.mouse_position, 4)

        self.position = self.position.lerp(self.mouse_position, 0.04)

        self.rect.center = (round(self.position.x), round(self.position.y))

class Apple(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.GroupSingle):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("sprites\\apple.png").convert_alpha(), (8, 8))
        self.position = pygame.math.Vector2(randint(0, 1920), randint(0, 1080))
        self.rect = self.image.get_rect(center=self.position)
        self.player = player
        self.score = 0
        self.touch_player = False
    def new_position(self):
        self.position = pygame.math.Vector2(randint(0, 1920), randint(0, 1080))
    def update(self): 
        self.position = self.position.lerp(pygame.math.Vector2((self.position.x + randint(-8, 8), self.position.y + randint(-8, 8))), pygame.math.clamp(random(), 0, 0.25))
        self.position
        if self.rect.colliderect(self.player.sprite.rect):
            self.touch_player = True
            self.new_position()
            self.score += 1
        else:
            self.touch_player = False

        self.rect.center = (round(self.position.x), round(self.position.y))

class Doctor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("sprites\\doctor.png").convert_alpha(), (8, 8))
        self.position = pygame.Vector2((960, 270))
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 0.02
        self.counter = 0
        self.game_over = False
        self.player_safe = True
        self.player_safe_counter = 0
        self.player_safe_counter_count = True
    def update(self, player_rect: pygame.rect.Rect, player_touch_apple):
        if not self.player_safe:
            self.counter += 1

            if self.counter == 4:
                self.counter = 0
                self.speed += 0.0005

            if player_touch_apple:
                self.speed -= 0.02
            
            self.speed = pygame.math.clamp(self.speed, 0, 1)

            self.position = self.position.lerp(player_rect.center, self.speed)

        if self.player_safe_counter_count:
            self.player_safe_counter += 1
            if self.player_safe_counter == 64:
                self.player_safe = False
                self.player_safe_counter_count = False

        self.rect.center = (round(self.position.x), round(self.position.y))

        if self.rect.colliderect(player_rect): 
            if not self.player_safe: 
                self.game_over = True
        
    #     self.Player = Player
    #     self.Apple = Apple
    #     self.Doctor = Doctor
    # def create_sprite(self, type, *args, **kwargs):
    #     if type == "player": return self.Player(*args, **kwargs)
    #     if type == "apple": return self.Apple(*args, **kwargs)
    #     if type == "doctor": return self.Doctor(*args, **kwargs)

class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("sprites\\play_button.png").convert_alpha(), (8, 8))
        # self.original_image = deepcopy(self.image)
        self.transparent_black_rectangle = pygame.surface.Surface((384, 128)).convert_alpha()
        self.transparent_black_rectangle.fill(pygame.color.Color(0, 0, 0, 64))
        self.hover_image = self.image
        self.hover_image.blit(self.transparent_black_rectangle, (0, 0))
        self.position = (960, 540)
        self.rect = self.image.get_rect(center=self.position)
        self.area = "title_screen"
    def update(self, cursor_circle_rect, left_click):
        if self.rect.colliderect(cursor_circle_rect):
            self.image = self.hover_image
            if left_click:
                self.area = "game"
        else:
            self.image = pygame.transform.scale_by(pygame.image.load("sprites\\play_button.png").convert_alpha(), (8, 8)) # self.original_image

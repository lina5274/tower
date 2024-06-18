import pygame
from pygame.math import Vector2
import random

paths = [
    [(100, 200), (150, 250), (200, 300)],
    [(50, 350), (100, 400), (150, 450)],
    [(300, 500), (350, 550), (400, 600)]
]

class Enemy(pygame.sprite.Sprite):
    ENEMY_TYPES = {
        'fast': {'speed': 5, 'health': 5},
        'strong': {'speed': 3, 'health': 15},
        'balanced': {'speed': 4, 'health': 10}
    }
    def __init__(self, path, type='balanced', speed=2, health=10, image_path=None, game = None):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.path = random.choice(paths)
        self.path_index = 0
        self.type = type
        self.speed, self.health = self.ENEMY_TYPES[type]['speed'], self.ENEMY_TYPES[type]['health']
        self.position = Vector2(path[0])
        self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        if self.path_index < len(self.path) - 1:
            start_point = Vector2(self.path[self.path_index])
            end_point = Vector2(self.path[self.path_index + 1])
            direction = (end_point - start_point).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

            if self.position.distance_to(end_point) < self.speed:
                self.path_index += 1

            if self.path_index >= len(self.path) - 1:
                self.game.game_over()
                self.kill()

import math

import pygame

import constants
import notes


class Point:
    def __init__(self, x, y, radius=3):
        self.translation_x = constants.WIDTH/2
        self.translation_y = constants.HEIGHT/2

        self.x = x + self.translation_x
        self.y = y + self.translation_y

        self.radius = radius

    def draw(self, screen, color):
        rect = (self.x, self.y, self.radius, self.radius)
        pygame.draw.ellipse(screen, color, rect)


class FadingPoint(Point):
    def __init__(self, x, y, life):
        super(FadingPoint, self).__init__(x, y)
        self.life = life
        self.radius = 30

    def update(self):
        self.life -= 1

    def draw(self, screen):
        super(FadingPoint, self).draw(screen, pygame.Color(0, 255, 0, self.life))


class FadingLine:
    def __init__(self):
        self.life = 60
        self.points = []

    def add_point(self, x, y):
        point = FadingPoint(x, y, self.life)
        self.points.append(point)

    def update(self):
        to_be_deleted = []
        for point in self.points:
            point.update()
            if point.life == 0:
                to_be_deleted.append(point)

        for point in to_be_deleted:
            self.points.remove(point)

    def draw(self, screen):
        if len(self.points) >= 2:
            pygame.draw.lines(screen, (0, 255, 0), False, [(p.x, p.y) for p in self.points])


class Visualizer:
    def __init__(self):
        self.fading_line = FadingLine()
        self.scale_factor = min(constants.WIDTH, constants.HEIGHT)/4
        self.movement_speed_scale = 1/constants.BASE_NOTE_FREQUENCY * 1/4

    def determine_visualization_function(self, active_notes):

        def f(t):
            result = [0, 0]


            for i, note in enumerate(active_notes):
                note_frequency = notes.note_to_frequency(note)
                result[i % 2] += self.scale_factor * math.sin(note_frequency * t * self.movement_speed_scale)

            return result

        return f

    def update(self, keys_pressed, frame_count):
        active_notes = notes.notes_pressed(keys_pressed)

        visualization_function = self.determine_visualization_function(active_notes)
        x, y = visualization_function(frame_count)

        self.fading_line.add_point(x, y)
        self.fading_line.update()

    def draw(self, screen):
        self.fading_line.draw(screen)





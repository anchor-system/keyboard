import math

import numpy

import functools

import pygame

import constants
import helpers
from anchor import notes


class NoteVisualizer:
    def __init__(self):
        self.scale_factor_x = constants.WINDOW_WIDTH / 4
        self.scale_factor_y = constants.WINDOW_HEIGHT / 4
        self.movement_speed_scale = 1 / constants.BASE_NOTE_FREQUENCY * 1 / 4

    def num_notes_visualized_on_x_axis(self, active_notes):
        return len(active_notes) // 2 + 1

    def num_notes_visualized_on_y_axis(self, active_notes):
        return len(active_notes) // 2

    def get_visualization_function(self, active_notes):

        # add in zero functions so reduce will work
        x_components = [lambda x: 0]
        y_components = [lambda x: 0]

        def add_functions(f, g):
            return lambda t: f(t) + g(t)

        def multiply_function(f, a):
            return lambda t: f(t) * a

        def one_component_visualization_function(note_frequency, x_axis):
            return lambda t: (
                self.scale_factor_x if x_axis else self.scale_factor_y
            ) * math.sin(note_frequency * t * self.movement_speed_scale)

        for i, note in enumerate(active_notes):
            note_frequency = notes.note_to_frequency(note)
            working_on_x_axis = i % 2 == 0

            if working_on_x_axis:
                chosen_component = x_components
            else:
                chosen_component = y_components

            chosen_component.append(
                one_component_visualization_function(note_frequency, working_on_x_axis)
            )

        x_component_sum = functools.reduce(add_functions, x_components)
        y_component_sum = functools.reduce(add_functions, y_components)

        x_scale = 1 / max(self.num_notes_visualized_on_x_axis(active_notes), 1)
        y_scale = 1 / max(self.num_notes_visualized_on_y_axis(active_notes), 1)

        x_component_final = multiply_function(x_component_sum, x_scale)
        y_component_final = multiply_function(y_component_sum, y_scale)

        return (x_component_final, y_component_final)

    def sample_visualization_function(self, frame_count, active_notes):

        interval_length = (2 * math.pi) * 5
        interval = [frame_count, frame_count + interval_length]
        (f, g) = self.get_visualization_function(active_notes)

        num_points_to_sample = 1000

        sampling_points = numpy.linspace(interval[0], interval[1], num_points_to_sample)
        sampled_function_points = list(map(lambda t: (f(t), g(t)), sampling_points))

        return sampled_function_points

    def draw(self, screen, frame_count, notes_pressed):
        sampled_function_points = self.sample_visualization_function(
            frame_count, notes_pressed
        )
        centered_points = list(map(screen.center_point, sampled_function_points))
        if len(centered_points) >= 2:
            pygame.draw.lines(screen.surface, (0, 255, 0), False, centered_points)

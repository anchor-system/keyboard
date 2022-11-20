from typing import List

import constants
import pygame

from anchor import analysis


class InstrumentVisualizer:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)

    def display_anchor_note(self, screen):
        text = self.font.render(f"{constants.ANCHOR_NOTE}*", True, (255, 255, 255))
        text_rect = text.get_rect(center=(constants.WIDTH / 10, constants.HEIGHT / 10))
        screen.blit(text, text_rect)

    def display_chord_analysis(self, screen, anchor_intervals: List[int]):
        interval_structure = analysis.analyze_canonical_interval_structure(anchor_intervals)
        text = self.font.render(f"{interval_structure}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 10))
        screen.blit(text, text_rect)

    def display_relative_interval_collection_structure(self, screen, anchor_intervals: List[int]):
        for interval, interval_frequency in analysis.analyze_relative_anchor_interval_structure(anchor_intervals).items():
            font_size = 50 + interval_frequency * 20
            font = pygame.font.Font(None, font_size)
            text = font.render(str(interval), True, (255, 255, 255))
            draw_point = (constants.WIDTH/20 + interval * 100, constants.HEIGHT - (constants.HEIGHT/10))
            text_rect = text.get_rect(center=draw_point)
            screen.blit(text, text_rect)


    def display_anchor_intervals(self, screen, anchor_intervals) -> None:
        for anchor_interval in anchor_intervals:
            octave, octave_position = divmod(anchor_interval, constants.NUM_NOTES)

            octave_notation = ("'" if octave >= 0 else ",") * abs(octave)

            text = self.font.render(
                f"{octave_position}{octave_notation}", True, (255, 255, 255)
            )

            text_position = (
                50 + octave_position * 50,
                150 + (constants.NUM_OCTAVES - octave) * 50,
            )

            text_rect = text.get_rect(center=text_position)
            screen.blit(text, text_rect)

        #     note_grid[q][r] = f'{r}{octave}'
        #
        #     s += f'{r}{octave} '
        #
        # note_table = helpers.two_dimensional_list_to_string(note_grid)
        #
        # text = font.render(note_table, True, (255, 255, 255))
        # text_rect = text.get_rect(center=(constants.WIDTH/2, constants.HEIGHT/2))
        # screen.blit(text, text_rect)

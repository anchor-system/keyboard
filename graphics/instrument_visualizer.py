from typing import List

import constants
import pygame

from anchor import analysis


class InstrumentVisualizer:

    def display_anchor_note(self, screen):
        text = screen.font.render(f"{constants.ANCHOR_NOTE}*", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.width / 10, screen.height / 10))
        screen.surface.blit(text, text_rect)

    def display_chord_analysis(self, screen, anchor_intervals: List[int]):
        interval_structure = [str(i) for i in analysis.analyze_canonical_interval_structure(anchor_intervals)]
        text = screen.font.render(' '.join(interval_structure), True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.width * (1 / 2), screen.height * (1 / 6)))
        screen.surface.blit(text, text_rect)

    def display_relative_interval_collection_complexity_score(self, screen, anchor_intervals: List[int]) -> None:
        score = analysis.anchor_intervals_complexity_score(anchor_intervals)

        text = screen.font.render(str(score), True, (255, 255, 255))

        text_position = (
            screen.width * (1 - 1 / 10),
            screen.height * 1/2
        )

        text_rect = text.get_rect(center=text_position)
        screen.surface.blit(text, text_rect)

    def display_relative_interval_collection_structure(self, screen, anchor_intervals: List[int]):
        for interval, interval_frequency in analysis.analyze_relative_anchor_interval_structure(anchor_intervals).items():
            font_size = int(screen.text_size + interval_frequency * screen.text_size * 2/5)
            font = pygame.font.Font(None, font_size)
            text = font.render(str(interval), True, (255, 255, 255))
            draw_point = (screen.width / 20 + interval * screen.text_size * 1.5, screen.height - (screen.height / 10))
            text_rect = text.get_rect(center=draw_point)
            screen.surface.blit(text, text_rect)

    def display_anchor_intervals(self, screen, anchor_intervals) -> None:

        notation = []

        for anchor_interval in anchor_intervals:
            octave, octave_position = divmod(anchor_interval, constants.NUM_NOTES)

            octave_notation = ("'" if octave >= 0 else ",") * abs(octave)

            notation.append(f"{octave_position}{octave_notation}")

        text = screen.font.render(
            ' '.join(notation), True, (255, 255, 255)
        )

        text_rect = text.get_rect(center=(screen.width/2, screen.height/10))
        screen.surface.blit(text, text_rect)

    def display_anchor_intervals_2D(self, screen, anchor_intervals) -> None:
        for anchor_interval in anchor_intervals:
            octave, octave_position = divmod(anchor_interval, constants.NUM_NOTES)

            octave_notation = ("'" if octave >= 0 else ",") * abs(octave)

            text = screen.font.render(
                f"{octave_position}{octave_notation}", True, (255, 255, 255)
            )

            text_position = (
                screen.width/10 + octave_position * screen.text_size,
                # subtract one because tab row is zeroth octave
                screen.height/2 + -(octave - 1) * screen.text_size
            )

            text_rect = text.get_rect(center=text_position)
            screen.surface.blit(text, text_rect)
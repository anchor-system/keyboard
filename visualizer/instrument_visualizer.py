import constants
import pygame


class InstrumentVisualizer:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)

    def display_anchor_note(self, screen):
        text = self.font.render(f"{constants.ANCHOR_NOTE}*", True, (255, 255, 255))
        text_rect = text.get_rect(center=(constants.WIDTH / 10, constants.HEIGHT / 10))
        screen.blit(text, text_rect)

    def offset_interval_so_left_is_zero(self, anchor_interval):
        """
        This method takes an anchor interval and converts it so that
        :param anchor_interval:
        :return:
        """

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

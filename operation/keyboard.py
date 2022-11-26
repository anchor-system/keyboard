from typing import List, Sequence

import pygame

import constants

class Keyboard:
    def __init__(self):

        # ESCAPE_AND_CAPS_SWAPPED = True
        self.ESCAPE_AND_CAPS_SWAPPED = False
        self.ESCAPE_AND_TILDE_SWAPPED = False

        if self.ESCAPE_AND_TILDE_SWAPPED:
            top_left_key = pygame.K_BACKQUOTE
        else:
            top_left_key = pygame.K_ESCAPE



        # We want Caps Lock to be our starting point, so we'll map Caps Lock to 0, then we'll use
        # distance to caps lock to produce an offset to the note C4.

        self.TOP_ROW = [
            top_left_key,
            # pygame.K_CAPSLOCK if self.ESCAPE_AND_CAPS_SWAPPED else pygame.K_ESCAPE,
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
            pygame.K_0,
            pygame.K_MINUS,
        ]

        self.TAB_ROW = [
            pygame.K_TAB,
            pygame.K_q,
            pygame.K_w,
            pygame.K_e,
            pygame.K_r,
            pygame.K_t,
            pygame.K_y,
            pygame.K_u,
            pygame.K_i,
            pygame.K_o,
            pygame.K_p,
            pygame.K_LEFTBRACKET,
        ]

        self.CAPS_ROW = [
            pygame.K_ESCAPE if self.ESCAPE_AND_CAPS_SWAPPED else pygame.K_CAPSLOCK,
            pygame.K_a,
            pygame.K_s,
            pygame.K_d,
            pygame.K_f,
            pygame.K_g,
            pygame.K_h,
            pygame.K_j,
            pygame.K_k,
            pygame.K_l,
            pygame.K_SEMICOLON,
            pygame.K_QUOTE,
        ]

        self.SHIFT_ROW = [
            pygame.K_LSHIFT,
            pygame.K_z,
            pygame.K_x,
            pygame.K_c,
            pygame.K_v,
            pygame.K_b,
            pygame.K_n,
            pygame.K_m,
            pygame.K_COMMA,
            pygame.K_PERIOD,
            pygame.K_SLASH,
            pygame.K_RSHIFT,
        ]

        self.LAYOUT = [
            *self.SHIFT_ROW,
            *self.CAPS_ROW,
            *self.TAB_ROW,
            *self.TOP_ROW,
        ]

        # The base key is the "origin"
        self.BASE_KEY = pygame.K_TAB
        self.BASE_KEY_LAYOUT_INDEX = 24


    def set_base_key_row(self, row_choice: int):
        self.BASE_KEY_LAYOUT_INDEX = row_choice * 12

    def notes_pressed(self, keys_pressed: Sequence[bool]) -> List[int]:
        """
        Given the current state of the keyboard, return the notes
        which are pressed.
        :param keys_pressed:
        :return:
        """
        notes = []
        for i, key in enumerate(self.LAYOUT):
            if keys_pressed[key]:
                notes.append(self.key_to_note(key))
        return notes


    def key_in_layout(self, key) -> bool:
        """
        Returns true iff the key is within the defined layout

        :param key: pygame.event.key
        :return: bool
        """
        return key in self.LAYOUT


    def key_to_note(self, key) -> int:
        """
        Given a key, return the note that it represents.
        See note.py to understand our representation of a note

        Additionally we want the leftmost key of each row
        to always represent the anchor interval 0, so we will
        remap the notes according to the current anchor note.

        This allows the device to only have one "position"

        :param key: pygame.event.key
        :return: int
        """
        return self.key_to_offset(key) + constants.ANCHOR_NOTE


    def key_to_offset(self, key) -> int:
        """
        Given a key, convert it to an offset from the base key
        with respect to the layout

        :param key: pygame.event.key
        :return: int
        """
        key_index = self.LAYOUT.index(key)
        return key_index - self.BASE_KEY_LAYOUT_INDEX  # so BASE_KEY gets mapped to 0

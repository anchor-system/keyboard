from typing import List, Sequence

import pygame

import constants

# ESCAPE_AND_CAPS_SWAPPED = True
ESCAPE_AND_CAPS_SWAPPED = False

# We want Caps Lock to be our starting point, so we'll map Caps Lock to 0, then we'll use
# distance to caps lock to produce an offset to the note C4.

NOTE_OFFSET = 24  # implies that tab is C4 and tab will map to zero then add 60.

ESCAPE_ROW = [
    pygame.K_CAPSLOCK if ESCAPE_AND_CAPS_SWAPPED else pygame.K_ESCAPE,
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

TAB_ROW = [
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

CAPS_ROW = [
    pygame.K_ESCAPE if ESCAPE_AND_CAPS_SWAPPED else pygame.K_CAPSLOCK,
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

SHIFT_ROW = [
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

LAYOUT = [
    *SHIFT_ROW,
    *CAPS_ROW,
    *TAB_ROW,
    *ESCAPE_ROW,
]

# The base key is the "origin"
BASE_KEY = pygame.K_TAB
BASE_KEY_LAYOUT_INDEX = 24


def notes_pressed(keys_pressed: Sequence[bool]) -> List[int]:
    """
    Given the current state of the keyboard, return the notes
    which are pressed.
    :param keys_pressed:
    :return:
    """
    notes = []
    for i, key in enumerate(LAYOUT):
        if keys_pressed[key]:
            notes.append(key_to_note(key))
    return notes


def key_in_layout(key) -> bool:
    """
    Returns true iff the key is within the defined layout

    :param key: pygame.event.key
    :return: bool
    """
    return key in LAYOUT


def key_to_note(key) -> int:
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
    return key_to_offset(key) + constants.ANCHOR_NOTE


def key_to_offset(key) -> int:
    """
    Given a key, convert it to an offset from the base key
    with respect to the layout

    :param key: pygame.event.key
    :return: int
    """
    key_index = LAYOUT.index(key)
    return key_index - BASE_KEY_LAYOUT_INDEX  # so BASE_KEY gets mapped to 0

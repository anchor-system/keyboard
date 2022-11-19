"""
Note:
In this situation a note is number which represents a certain offset
from a base frequency. For example if we set C3 to be our base note,
then D3 would be represented by 2. B4 would be -1, C#4 would be 12.

Anchor Note:
An Anchor note is a note which is considered the main note and what
other notes are compared against

Anchor Interval:
An anchor interval is defined in terms of an anchor note and a normal
note, it is the number of notes between the anchor note and the note.
If we set our anchor note to 8, then 11 has an anchor interval of 3.
If we set our anchor note to -3, then 3 has an anchor interval of 6.
If we set our anchor note to 24, then 57 has an anchor interval of 33.
"""
from typing import List

import keyboard
import constants
import helpers


def notes_to_anchor_intervals(anchor_note: int, notes: List[int]) -> List[int]:
    """
    return the anchor intervals of a list of notes.

    :param anchor_note:
    :param notes:
    :return:
    """
    return [note_to_anchor_interval(anchor_note, note) for note in notes]

def note_to_anchor_interval(anchor_note: int, note: int) -> int:
    """
    Given a note, and an anchor note, return the notes anchor interval

    :param anchor_note: int
    :param note: int
    :return: int
    """
    return note - anchor_note


def notes_pressed(keys_pressed):
    notes = []
    for i, key in enumerate(keyboard.LAYOUT):
        if keys_pressed[key]:
            notes.append((i - keyboard.NOTE_OFFSET))
    return notes


def note_to_frequency(note):
    return 2 ** (note/12) * constants.BASE_NOTE_FREQUENCY


def display_notes(screen, font, notes):
    note_grid = [[' ' for _ in constants.NUM_NOTES] for _ in constants.NUM_OCTAVES]


def display_notes_old(screen, font, notes):
    note_grid = [[' ' for _ in constants.NUM_NOTES] for _ in constants.NUM_OCTAVES]
    notes = [n + keyboard.NOTE_OFFSET for n in notes]
    for note in notes:
        absolute_octave, absolute_note = divmod(note, constants.NUM_NOTES)
        anchored_octave, anchored_note = divmod(note - keyboard.NOTE_OFFSET, constants.NUM_NOTES)

        r_x = (r_x - constants.ANCHOR_NOTE) % constants.NUM_NOTES
        r_s = (r_s - constants.ANCHOR_NOTE) % constants.NUM_NOTES

        octave = ("'" if q_s >= 0 else ",") * abs(q_s)

        text = font.render(f'{r_s}{octave}', True, (255, 255, 255))

        text_position = (50 + r_x * 50, 150 + (constants.NUM_OCTAVES - q_y) * 50)

        text_rect = text.get_rect(center=text_position)
        screen.blit(text, text_rect)

        note_grid[q][r] = f'{r}{octave}'

        s += f'{r}{octave} '

    note_table = helpers.two_dimensional_list_to_string(note_grid)
    #
    # text = font.render(note_table, True, (255, 255, 255))
    # text_rect = text.get_rect(center=(constants.WIDTH/2, constants.HEIGHT/2))
    # screen.blit(text, text_rect)


def note_to_midi(note):
    """
    zero gets mapped to middle C which is 60
    :param note:
    :return:
    """
    return note + 60


def get_note_from_key(key_pressed):
    key_index = keyboard.LAYOUT.index(key_pressed)
    note = key_index - keyboard.NOTE_OFFSET + constants.ANCHOR_NOTE
    return note


NOTE_ON_STATUS_BYTE = 0x90
NOTE_OFF_STATUS_BYTE = 0x80
CONTROL_CHANGES_BYTE = 0xb0
SUSTAIN_PEDAL_STATUS_NUMBER = 64
def enable_sustain(midiout):
    midi_message = [CONTROL_CHANGES_BYTE, SUSTAIN_PEDAL_STATUS_NUMBER, 127]
    midiout.send_message(midi_message)

def disable_sustain(midiout):
    midi_message = [CONTROL_CHANGES_BYTE, SUSTAIN_PEDAL_STATUS_NUMBER, 0]
    midiout.send_message(midi_message)


def start_midi_note(midiout, key_pressed):
    note = get_note_from_key(key_pressed)
    midi_note_on = [0x90, note_to_midi(note), 112]
    midiout.send_message(midi_note_on)


def end_midi_note(midiout, key_pressed):
    note = get_note_from_key(key_pressed)
    midi_note_off = [0x80, note_to_midi(note), 0]
    midiout.send_message(midi_note_off)



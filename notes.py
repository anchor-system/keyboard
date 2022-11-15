import keyboard_layout
import constants
import helpers


def notes_pressed(keys_pressed):
    notes = []
    for i, key in enumerate(keyboard_layout.LAYOUT):
        if keys_pressed[key]:
            notes.append((i - keyboard_layout.NOTE_OFFSET))
    return notes


def note_to_frequency(note):
    return 2 ** (note/12) * constants.BASE_NOTE_FREQUENCY


def display_notes(screen, font, notes):
    notes = [n + keyboard_layout.NOTE_OFFSET for n in notes]
    for note in notes:
        q_y, r_x = divmod(note, constants.NUM_NOTES)
        q_s, r_s = divmod(note - keyboard_layout.NOTE_OFFSET, constants.NUM_NOTES)

        # r_x = (r_x - constants.ANCHOR_NOTE) % constants.NUM_NOTES
        # r_s = (r_s - constants.ANCHOR_NOTE) % constants.NUM_NOTES

        octave = ("'" if q_s >= 0 else ",") * abs(q_s)

        text = font.render(f'{r_s}{octave}', True, (255, 255, 255))

        text_position = (50 + r_x * 50, 150 + (constants.NUM_OCTAVES - q_y) * 50)

        text_rect = text.get_rect(center=text_position)
        screen.blit(text, text_rect)

        # note_grid[q][r] = f'{r}{octave}'

        # s += f'{r}{octave} '

    # note_table = helpers.two_dimensional_list_to_string(note_grid)
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
    key_index = keyboard_layout.LAYOUT.index(key_pressed)
    note = key_index - keyboard_layout.NOTE_OFFSET + constants.ANCHOR_NOTE
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



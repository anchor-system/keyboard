from anchor.notes import note_to_midi

NOTE_ON_STATUS_BYTE = 0x90
NOTE_OFF_STATUS_BYTE = 0x80
CONTROL_CHANGES_BYTE = 0xB0
SUSTAIN_PEDAL_STATUS_NUMBER = 64


def enable_sustain(midiout):
    midi_message = [CONTROL_CHANGES_BYTE, SUSTAIN_PEDAL_STATUS_NUMBER, 127]
    midiout.send_message(midi_message)


def disable_sustain(midiout):
    midi_message = [CONTROL_CHANGES_BYTE, SUSTAIN_PEDAL_STATUS_NUMBER, 0]
    midiout.send_message(midi_message)


def start_midi_note(midiout, note):
    midi_note_on = [0x90, note_to_midi(note), 112]
    midiout.send_message(midi_note_on)


def end_midi_note(midiout, note):
    midi_note_off = [0x80, note_to_midi(note), 0]
    midiout.send_message(midi_note_off)

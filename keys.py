import pygame

import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

#print(available_ports)

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

pygame.init()

screen = pygame.display.set_mode((640, 480))

WIDTH, HEIGHT = pygame.display.get_surface().get_size()

WHITE = (255, 255, 255)

ESCAPE_AND_CAPS_SWAPPED = True


# We want Caps Lock to be our starting point, so we'll map Caps Lock to 0, then we'll use 
# distance to caps lock to produce an offset to the note C4.

NOTE_OFFSET = 24

ESCAPE_ROW = [pygame.K_CAPSLOCK if ESCAPE_AND_CAPS_SWAPPED else pygame.K_ESCAPE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS]

TAB_ROW = [ pygame.K_TAB, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET]

CAPS_ROW = [ pygame.K_ESCAPE if ESCAPE_AND_CAPS_SWAPPED else pygame.K_CAPSLOCK , pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE]

SHIFT_ROW = [ pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT]

LAYOUT = [ 
        *SHIFT_ROW,
        *CAPS_ROW,
        *TAB_ROW,
        *ESCAPE_ROW,
]


# draw text
font = pygame.font.Font(None, 50)

def notes_pressed(keys_pressed):
    notes = []
    for i, key in enumerate(LAYOUT):
        if keys_pressed[key]:
            notes.append((i - NOTE_OFFSET))
    return notes

def display_notes(screen, notes):
    s = ''
    for note in notes:
        q, r = divmod(note, 12)
        octave = ("'" if q >= 0 else ",") * abs(q)
        s += f'{r}{octave} '
        #s += f'{note}'

    text = font.render(s[:-1], True, WHITE)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)

def note_to_midi(note):
    return note + 60

with midiout:
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():

            match event.type:
                case pygame.QUIT:
                    running = False
                    pygame.quit()
                case pygame.KEYDOWN:
                    if event.key in LAYOUT:
                        key_index = LAYOUT.index(event.key)
                        note = key_index - NOTE_OFFSET
                        midi_note_on = [0x90, note_to_midi(note), 112]
                        midiout.send_message(midi_note_on)
                case pygame.KEYUP:
                    if event.key in LAYOUT:
                        key_index = LAYOUT.index(event.key)
                        note = key_index - NOTE_OFFSET
                        midi_note_off = [0x80, note_to_midi(note), 0]
                        midiout.send_message(midi_note_off)
            

        keys_pressed = pygame.key.get_pressed()

        active_notes = notes_pressed(keys_pressed)


        screen.fill(pygame.Color("black"))
                
        display_notes(screen, active_notes)

        pygame.display.flip()

del midiout

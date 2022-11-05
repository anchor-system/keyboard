import pygame
import rtmidi
import constants
import input

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()


if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

# draw text
font = pygame.font.Font(None, 50)

user_has_quit = False

with midiout:
    while not user_has_quit:
        current_time = pygame.time.get_ticks()

        user_has_quit = input.process_events(screen, font, midiout, pygame.event.get(), pygame.key.get_pressed())

del midiout

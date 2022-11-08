import pygame
import rtmidi
import constants
import input
from visualizer import Visualizer

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

visualizer = Visualizer()

frame_count = 0

with midiout:
    while not user_has_quit:
        current_time = pygame.time.get_ticks()
        screen.fill(pygame.Color("black"))

        user_has_quit = input.process_events(screen, font, midiout, pygame.event.get(), pygame.key.get_pressed())

        # visualizer.update(pygame.key.get_pressed(), frame_count)
        # visualizer.draw(screen)

        frame_count += 1

        pygame.display.flip()

del midiout

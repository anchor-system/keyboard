import pygame
import rtmidi
import constants
import input
import keyboard
import notes
from visualizer.instrument_visualizer import InstrumentVisualizer

from visualizer.note_visualizer import NoteVisualizer


class Instrument:

    """
    An instrument is a device which takes in inputs from a user, and represents that information
    mainly through audio but optionally visually as well
    """

    def __init__(self, graphical_mode: bool, fullscreen: bool):

        pygame.init()

        self.midi_port = 1
        self.midiout = self.initialize_midi()

        self.pressed_keys = []

        self.command_started = False
        self.command_key = pygame.K_SPACE

        if graphical_mode:

            self.frame_count = 0

            if fullscreen:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((400, 400))

            surface = (
                pygame.display.get_surface()
            )  # get the surface of the current active display
            constants.WIDTH, constants.HEIGHT = (
                surface.get_width(),
                surface.get_height(),
            )  # create an array of surface.width and surface.height

            self.graphical_mode = True

        self.instrument_visualizer = InstrumentVisualizer()
        self.note_visualizer = NoteVisualizer()

    def initialize_midi(self):
        """
        Set up the midi output and return the configured
        midi object
        :return:
        """
        midiout = rtmidi.MidiOut()
        available_ports = midiout.get_ports()

        if available_ports:
            midiout.open_port(self.midi_port)
        else:
            midiout.open_virtual_port("My virtual output")

        return midiout

    def start_playing(self):
        playing = True
        with self.midiout:
            while playing:
                current_time = pygame.time.get_ticks()

                keys_pressed = pygame.key.get_pressed()
                notes_pressed = keyboard.notes_pressed(keys_pressed)

                playing = self.process_events(
                    self.midiout, pygame.event.get(), keys_pressed
                )

                if self.graphical_mode:
                    self.visualize(notes_pressed)
                    pygame.display.flip()

                self.frame_count += 1

        del self.midiout

    def visualize(self, notes_pressed):
        anchor_intervals_pressed = notes.notes_to_anchor_intervals(
            constants.ANCHOR_NOTE, notes_pressed
        )
        self.screen.fill(pygame.Color("black"))
        self.note_visualizer.draw(self.screen, self.frame_count, notes_pressed)
        self.instrument_visualizer.display_anchor_intervals(
            self.screen, anchor_intervals_pressed
        )
        self.instrument_visualizer.display_anchor_note(self.screen)

    # also volume and stuff.
    def process_key_down(self, key, midiout):
        if key in keyboard.LAYOUT:
            notes.start_midi_note(midiout, key)

    def process_commands(self, midiout, keys_pressed):
        def all_pressed(keys):
            return all(keys_pressed[key] for key in keys)

        if keys_pressed[self.command_key]:
            self.command_started = True

        # transposition
        if all_pressed([self.command_key, pygame.K_t]):
            for i, key in enumerate(keyboard.ESCAPE_ROW):
                if keys_pressed[key]:
                    constants.ANCHOR_NOTE = i
        elif all_pressed([self.command_key, pygame.K_s]):
            notes.enable_sustain(midiout)
        elif all_pressed([self.command_key, pygame.K_m]):
            notes.disable_sustain(midiout)

    def process_key_up(self, key: pygame.key, midiout) -> None:

        if key in keyboard.LAYOUT:
            notes.end_midi_note(midiout, key)

    def process_transposition(self, keys_pressed) -> None:
        if keys_pressed[pygame.K_SPACE]:
            for i, key in enumerate(keyboard.ESCAPE_ROW):
                if keys_pressed[key]:
                    constants.ANCHOR_NOTE = i

    def process_events(self, midiout, events, keys_pressed):
        user_has_quit = False
        for event in events:
            if event.type == pygame.QUIT:
                user_has_quit = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not keys_pressed[self.command_key]:
                    self.process_key_down(event.key, midiout)

            elif event.type == pygame.KEYUP:
                if not keys_pressed[self.command_key]:
                    self.process_key_up(event.key, midiout)

        command_completed = self.process_commands(midiout, keys_pressed)

        return not user_has_quit

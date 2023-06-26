import pygame
import rtmidi
import constants
from operation import keyboard
import midi
from screeninfo import get_monitors
from anchor import notes
from graphics.screen import Screen
from graphics.instrument_visualizer import InstrumentVisualizer

from graphics.note_visualizer import NoteVisualizer
from operation.keyboard import Keyboard


class Instrument:

    """
    An instrument is a device which takes in inputs from a user, and represents that information
    mainly through audio but optionally visually as well
    """

    def __init__(self, graphical_mode: bool, fullscreen: bool):

        pygame.init()

        self.midi_port = 1
        self.midiout = self.initialize_midi()

        self.keyboard = Keyboard()

        self.pressed_keys = []

        self.command_started = False
        self.command_key = pygame.K_SPACE
        self.option_key = pygame.K_LSHIFT

        self.monitor_choice = 0

        if graphical_mode:

            self.frame_count = 0

            if constants.INITIALLY_FULLSCREEN:
                monitor = get_monitors()[self.monitor_choice]
                w, h = monitor.width, monitor.height
                self.screen = Screen(pygame.display.set_mode((0, 0), pygame.FULLSCREEN), True, w, h)
            else:
                self.screen = Screen(
                    pygame.display.set_mode((constants.INITIAL_WINDOW_WIDTH, constants.INITIAL_WINDOW_HEIGHT), pygame.RESIZABLE),
                    False,
                    constants.INITIAL_WINDOW_WIDTH, constants.INITIAL_WINDOW_HEIGHT
                                     )

            surface = (
                pygame.display.get_surface()
            )  # get the surface of the current active display
            constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT = (
                surface.get_width(),
                surface.get_height(),
            )  # create an array of surface.width and surface.height

            self.graphical_mode = True

        self.instrument_visualizer = InstrumentVisualizer()
        self.note_visualizer = NoteVisualizer(self.screen)

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
                notes_pressed = self.keyboard.notes_pressed(keys_pressed)

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
        self.screen.surface.fill(pygame.Color("black"))
        self.note_visualizer.draw(self.screen, self.frame_count, notes_pressed)
        # self.instrument_visualizer.display_anchor_intervals_2D(self.screen, anchor_intervals_pressed)
        self.instrument_visualizer.display_anchor_intervals(self.screen, anchor_intervals_pressed)
        self.instrument_visualizer.display_anchor_note(self.screen)
        self.instrument_visualizer.display_chord_analysis(self.screen, anchor_intervals_pressed)
        self.instrument_visualizer.display_relative_interval_collection_structure(self.screen, anchor_intervals_pressed)
        self.instrument_visualizer.display_relative_interval_collection_complexity_score(self.screen, anchor_intervals_pressed)

    # also volume and stuff.
    def process_key_down(self, key, midiout):
        if key in self.keyboard.LAYOUT:
            midi.start_midi_note(midiout, self.keyboard.key_to_note(key))

    def process_commands(self, midiout, keys_pressed):
        def all_pressed(keys):
            return all(keys_pressed[key] for key in keys)

        if keys_pressed[self.command_key]:
            self.command_started = True

        if all_pressed([self.command_key, pygame.K_t]):
            for i, key in enumerate(self.keyboard.TOP_ROW):
                if keys_pressed[key]:
                    constants.ANCHOR_NOTE = i
        # elif all_pressed([self.command_key, pygame.K.b]): # bass mode
        #
        elif all_pressed([self.command_key, pygame.K_r]):
            if keys_pressed[pygame.K_ESCAPE]:
                self.keyboard.set_base_key_row(0)
            elif keys_pressed[pygame.K_1]:
                self.keyboard.set_base_key_row(1)
            elif keys_pressed[pygame.K_2]:
                self.keyboard.set_base_key_row(2)
            elif keys_pressed[pygame.K_3]:
                self.keyboard.set_base_key_row(3)
        elif all_pressed([self.command_key, pygame.K_s]):
            midi.enable_sustain(midiout)
        elif all_pressed([self.command_key, pygame.K_m]):
            midi.disable_sustain(midiout)
        elif all_pressed([self.command_key, pygame.K_v]):
            for i, key in enumerate(self.keyboard.TOP_ROW):
                if keys_pressed[key]:
                    midi.BASE_VELOCITY = midi.MAX_VELOCITY / len(self.keyboard.TOP_ROW) * (i + 1)
        elif all_pressed([self.command_key, self.option_key, pygame.K_f]):
            pygame.display.quit()
            pygame.display.init()
            if self.screen.fullscreen:
                self.screen.surface = pygame.display.set_mode((constants.INITIAL_WINDOW_WIDTH, constants.INITIAL_WINDOW_HEIGHT), pygame.RESIZABLE)
                self.screen.update_resolution(constants.INITIAL_WINDOW_WIDTH, constants.INITIAL_WINDOW_HEIGHT)
            else:
                self.screen.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                monitor = get_monitors()[self.monitor_choice]
                w, h = monitor.width, monitor.height
                self.screen.update_resolution(w, h)
            self.screen.fullscreen = not self.screen.fullscreen
        elif all_pressed([self.command_key, self.option_key, pygame.K_q]):
            pygame.quit()


            self.screen.fullscreen = not self.screen.fullscreen

    def process_key_up(self, key: pygame.key, midiout) -> None:

        if key in self.keyboard.LAYOUT:
            midi.end_midi_note(midiout, self.keyboard.key_to_note(key))

    def process_transposition(self, keys_pressed) -> None:
        if keys_pressed[pygame.K_SPACE]:
            for i, key in enumerate(self.keyboard.TOP_ROW):
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

            elif event.type == pygame.VIDEORESIZE:
                self.screen.update_resolution(event.w, event.h)

        command_completed = self.process_commands(midiout, keys_pressed)

        return not user_has_quit

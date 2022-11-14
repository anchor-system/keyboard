import pygame
import rtmidi
import constants
import input
import keyboard_layout
import notes

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
        self.suspended_keys_pressed = []

        self.keys_are_suspended = False

        if graphical_mode:

            self.frame_count = 0

            if fullscreen:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((400, 400))


            self.font = pygame.font.Font(None, 50)

            surface = pygame.display.get_surface() #get the surface of the current active display
            constants.WIDTH, constants.HEIGHT = surface.get_width(), surface.get_height()#create an array of surface.width and surface.height

            self.graphical_mode = False

        # self.instrument_visualizer = InstrumentVisualizer
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

                 if self.graphical_mode:
                     self.screen.fill(pygame.Color("black"))
                     self.note_visualizer.draw(self.screen, self.frame_count, pygame.key.get_pressed())

                 playing = self.process_events(self.screen, self.font, self.midiout, pygame.event.get(), pygame.key.get_pressed())

                 self.frame_count += 1

                 if self.graphical_mode:
                     pygame.display.flip()

         del self.midiout


    def process_events(self,screen, font, midiout, events, keys_pressed):
        user_has_quit = False
        for event in events:
            if event.type == pygame.QUIT:
                user_has_quit = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:

                print(event.key)

                if event.key == pygame.K_SPACE:

                    if not self.keys_are_suspended:
                        self.suspended_keys_pressed = keys_pressed
                    else:
                        for key in keyboard_layout.LAYOUT:
                            if self.suspended_keys_pressed[key]:
                                notes.end_midi_note(midiout, key)

                    self.keys_are_suspended = not self.keys_are_suspended

                if event.key in keyboard_layout.LAYOUT:
                    notes.start_midi_note(midiout, event.key)


            elif event.type == pygame.KEYUP:

                if event.key in keyboard_layout.LAYOUT:
                    if self.keys_are_suspended:
                        if not self.suspended_keys_pressed[event.key]:
                            notes.end_midi_note(midiout, event.key)
                    else:
                        notes.end_midi_note(midiout, event.key)


        # active_notes = notes.notes_pressed(keys_pressed)

        if keys_pressed[pygame.K_SPACE]:
            # Suspend
            # Transposition
            for i, key in enumerate(keyboard_layout.ESCAPE_ROW):
                if keys_pressed[key]:
                    constants.ANCHOR_NOTE = i

        # notes.display_notes(screen, font, active_notes)

        # text = font.render(f'{constants.ANCHOR_NOTE}*', True, (255, 255, 255))
        # text_rect = text.get_rect(center=(constants.WIDTH/10, constants.HEIGHT/10))
        # screen.blit(text, text_rect)


        return not user_has_quit

import pygame
import keyboard_layout
import notes
import constants


def process_events(screen, font, midiout, events, keys_pressed):
    """
    process events from the user. Returns if the user has quit the program

    :param midiout:
    :param events:
    :param keys_pressed:
    :return:
    """
    user_has_quit = False
    for event in events:
        match event.type:
            case pygame.QUIT:
                user_has_quit = True
                pygame.quit()
            case pygame.KEYDOWN:
                if event.key in keyboard_layout.LAYOUT:
                    notes.start_midi_note(midiout, event.key)
            case pygame.KEYUP:
                if event.key in keyboard_layout.LAYOUT:
                    notes.end_midi_note(midiout, event.key)

    active_notes = notes.notes_pressed(keys_pressed)

    if keys_pressed[pygame.K_SPACE]:
        for i, key in enumerate(keyboard_layout.ESCAPE_ROW):
            if keys_pressed[key]:
                constants.ANCHOR_NOTE = i

    screen.fill(pygame.Color("black"))
    notes.display_notes(screen, font, active_notes)

    text = font.render(f'{constants.ANCHOR_NOTE}*', True, (255, 255, 255))
    text_rect = text.get_rect(center=(constants.WIDTH/10, constants.HEIGHT/10))
    screen.blit(text, text_rect)


    pygame.display.flip()

    return user_has_quit


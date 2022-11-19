import pygame
import keyboard
import notes
import constants


def process_events(screen, font, midiout, events, keys_pressed):
    """
    process events from the user. Returns True if it has successfully
    processed the events and the user hasn't quit.

    :param midiout:
    :param events:
    :param keys_pressed:
    :return:
    """
    user_has_quit = False
    for event in events:
        if event.type == pygame.QUIT:
            user_has_quit = True
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in keyboard.LAYOUT:
                notes.start_midi_note(midiout, event.key)
        elif event.type == pygame.KEYUP:
            if event.key in keyboard.LAYOUT:
                notes.end_midi_note(midiout, event.key)

    active_notes = notes.notes_pressed(keys_pressed)

    if keys_pressed[pygame.K_SPACE]:
        for i, key in enumerate(keyboard.ESCAPE_ROW):
            if keys_pressed[key]:
                constants.ANCHOR_NOTE = i

    notes.display_notes(screen, font, active_notes)

    # text = font.render(f'{constants.ANCHOR_NOTE}*', True, (255, 255, 255))
    # text_rect = text.get_rect(center=(constants.WIDTH/10, constants.HEIGHT/10))
    # screen.blit(text, text_rect)



    return not user_has_quit


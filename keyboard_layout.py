import pygame
ESCAPE_AND_CAPS_SWAPPED = True
ESCAPE_AND_CAPS_SWAPPED = False

# We want Caps Lock to be our starting point, so we'll map Caps Lock to 0, then we'll use
# distance to caps lock to produce an offset to the note C4.

NOTE_OFFSET = 24 # implies that tab is C4 and tab will map to zero then add 60.

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

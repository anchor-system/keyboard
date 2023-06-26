# keyboard

This program is designed to be a replacement for an instrument, it has the same polyphonic capabilities as a piano.
When paired with an n-key rollover keyboard, then it allows for more complex chords to be played.

The layout is designed to be as easy to learn as possible by simply incrementing semitones as we move from left to right
across the keyboard, moving up a row goes up an octave as well.

## Output

This program opens a midi port and sends out midi commands based on what keys are currently being pressed. Personally 
I connect this to loopmidi and then connect that to pianoteq which gives a nice sound.

## Commands

### Transposing

Transposing on regular instruments is usually not a simple process, in so far that it becomes a recognized
skill amongst musicians. Since this program is not bound too heavily by physical restraints, then we make transposing simple.

To transpose, simply hold `space+t` and then select the root on the number row of the keyboard. With this command it means
that we simply just figure out what the new key is, transpose the instrument and play regularly.

### Changing the octave row

`space+r`

### Sustain mode

enable: `space+s`
disable: `space+m`

### Increase/Decrease midi velocity

`space+v` + `any top row button in increasing velocity`

### Toggle fullscreen

`space+shift+f`

### Quit

`space+shift+q`
# keyboard

At the end of the day this program has to create
actual notes so that they can be output through
midi. 

The way we play notes is through the anchor system
which allows us to refer to notes through representations
which aren't the notes themselves.

We would like to visualize some information as well.

We want to have a visualizer which operates on midi note
out events pretty much so it's decoupled from the instrument.

We want to also have a visualier which operates at 
at the level of the anchor system which will help us
learn from the system.

We would firstly like to visualize the anchor interval
which is being played at any moment in time, therefore
this is not a midi visualizer.

This should be built into the device since it allows 
you to learn from the instrument faster and in a better way.

The anchor system visualizer should operate as follows.

visualize every note that is currently being played

visualize the intervallic structure if more than one note
is being played.

visualize the most recent notes played in the last 30 
seconds or within some interval.

display what the anchor note is.

potentially display chord names in standard so they 
can understand?

AnchorNote should be a class which contains two numbers.

We first start keys_pressed which allows us to query if a 
key is being pressed. 

Given a colleciton of pressed keys, that may be turned 
into anchorIntervals by first knowing what each Note each
key on the keyboard maps to, then converting that note an
anchorInterval using the anchor note.


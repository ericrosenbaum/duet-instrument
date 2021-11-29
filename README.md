# Duet Instrument
A musical instrument built for two. The two sides of the instrument have matching sets of notes in matching colors. They're mirrored, so if we make the same movement, we play the same melody. You can play together in synchrony, have a call-and-response conversation, trade phrases, or play other improvisation games.

It's about a shared experience of musical communication. A flow state, where you're in sync with each other. A non-verbal conversation through musical gestures. 

[![video thumbnail](http://img.youtube.com/vi/LJ8UbLy1rD8/0.jpg)](http://www.youtube.com/watch?v=LJ8UbLy1rD8)

https://www.youtube.com/watch?v=LJ8UbLy1rD8

# Construction
The Duet Instrument is a self-contained instrument that detects touches using capacitive sensing and plays synthesized sounds.

![duet-instrument-interior-sm](https://user-images.githubusercontent.com/567844/143807217-a2977e17-c00c-4b98-a75b-d39fb0f7f6b5.jpg)

On the top panel, I put on a custom sticker I designed in Adobe Illustrator, and created using stickeryou.com. The panel is a piece of 1/8" acrylic, with copper tape patches for capacitive sensing (through the sticker) for each note. I made laser-cut slots for each note, where the copper tape feeds through to the back, soldered to a wire that connects to a capacitive sensing circuit board (Adafruit MPR-121). Two of these sensing boards connect to the microcontroller board (Adafruit RP2040), which is attached to a sound synthesis board (Music Maker Featherwing with amp), with speakers. Two buttons and a potentiometer are also connected to the microcontroller, along with a rechargeable battery. The case is wooden drawer organizer box.

# Parts list
Adafruit Feather RP2040
Music Maker FeatherWing w/ Amp
12-Key Capacitive Touch Sensor Breakout - MPR121 - STEMMA QT x 2
STEMMA QT / Qwiic JST SH 4-Pin Cable - 200mm Long x 2
Stereo Enclosed Speaker Set - 3W 4 Ohm
Lithium Ion Cylindrical Battery - 3.7v 2200mAh
Panel Mount Right Angle 10K Linear Potentiometer w/On-Off Switch
Knob
Buttons x 2
USB A to C 6”
Black 1/8” cast plexiglas 12"x12”
Copper foil tape 1”
Bamboo Wood Stacking Drawer Organizer Box, 6" x 9”
StickerYou.com Custom sticker 5.83" x 8.75”

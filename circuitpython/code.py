import time
import board
import busio
import neopixel

# Import MPR121 module.
import adafruit_mpr121

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 objects.
cap1 = adafruit_mpr121.MPR121(i2c)
cap2 = adafruit_mpr121.MPR121(i2c, address=0x5B)

pixels.fill((20, 20, 20)) # white

# MIDI setup
midi1 = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)
midi2 = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=1
)
midi3 = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=2
)

def playStartupSound():
    midi1.send(NoteOn(60, 120))
    midi1.send(NoteOn(64, 120))
    time.sleep(0.2)
    midi1.send(NoteOff(60))
    midi1.send(NoteOff(64))
    time.sleep(0.2)
    midi2.send(NoteOn(60, 120))
    midi2.send(NoteOn(64, 120))
    time.sleep(0.2)
    midi2.send(NoteOff(60))
    midi2.send(NoteOff(64))

pixels.fill((0, 20, 0)) # green

playStartupSound()

root = 60
scale = [0, 3, 5, 7, 10, 12, 15]
pins = [3, 2, 4, 1, 5, 0, 6]
touch_states1 = [False] * len(scale)
touch_states2 = [False] * len(scale)
loop_toggle = False

def play_touches(cap, midi, touch_states):
    for i in range(len(scale)):
        touched = cap[pins[i]].value
        if (not touch_states[i] and touched):
                midi.send(NoteOn(root + scale[i], 120))
        if (touch_states[i] and not touched):
                midi.send(NoteOff(root + scale[i]))
        touch_states[i] = touched;

def other_buttons():
    global loop_toggle
    if (not loop_toggle and cap1[11].value):
        midi3.send(NoteOn(60))
    loop_toggle = cap1[11].value

while True:
    play_touches(cap1, midi1, touch_states1)
    play_touches(cap2, midi2, touch_states2)
    other_buttons()
    time.sleep(0.001)
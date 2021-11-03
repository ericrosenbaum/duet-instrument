import board
import digitalio
from analogio import AnalogIn
import time
import supervisor
import math
import busio
import adafruit_mpr121
from adafruit_debouncer import Debouncer

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 objects.
cap1 = adafruit_mpr121.MPR121(i2c)
cap2 = adafruit_mpr121.MPR121(i2c, address=0x5B)

# button setup
button1_pin = digitalio.DigitalInOut(board.A1)
button1_pin.direction = digitalio.Direction.INPUT
button1_pin.pull = digitalio.Pull.UP
button1 = Debouncer(button1_pin)

button2_pin = digitalio.DigitalInOut(board.A2)
button2_pin.direction = digitalio.Direction.INPUT
button2_pin.pull = digitalio.Pull.UP
button2 = Debouncer(button2_pin)

# potentiometer setup
potentiometer = AnalogIn(board.A0)

# MIDI setup
VS1053_BANK_DEFAULT = 0x00
VS1053_BANK_DRUMS1 = 0x78
VS1053_BANK_DRUMS2 = 0x7F
VS1053_BANK_MELODY = 0x79
MIDI_NOTE_ON = 0x90
MIDI_NOTE_OFF = 0x80
MIDI_CHAN_MSG = 0xB0
MIDI_CHAN_BANK = 0x00
MIDI_CHAN_VOLUME = 0x07
MIDI_CHAN_PAN = 0x0A
MIDI_CHAN_PROGRAM = 0xC0

uart = busio.UART(board.TX, board.RX, baudrate=31250)

def noteOn(channel, note, vel):
    uart.write(bytearray([MIDI_NOTE_ON | channel, note, vel]))

def noteOff(channel, note):
    uart.write(bytearray([MIDI_NOTE_OFF | channel, note, 0]))

def setChannelBank(channel, bank):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_BANK, bank]))

def setChannelVolume(channel, vol):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_VOLUME, vol]))

def setChannelInstrument(channel, num):
    uart.write(bytearray([MIDI_CHAN_PROGRAM | channel]))
    time.sleep(0.01)
    uart.write(bytearray([num]))
    time.sleep(0.01)

def setChannelPan(channel, pan):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_PAN, pan]))

root = 60

scales = [
    [0, 2, 3, 5, 7, 10, 12], # minor scale: C D Eb F G Bb C
    [0, 3, 5, 7, 10, 12, 15], # minor pentatonic: C Eb F G Bb C Eb
    [0, 2, 4, 5, 7, 9, 12], # major scale: C D E F G A C
    [0, 4, 7, 9, 12, 16, 19], # major 6: C E G A C E G
    [0, 2, 4, 6, 8, 10, 12] # whole tone: C D E F# G# A# C
]

scale_num = 0;
scale = scales[scale_num]

volume = 90

setChannelBank(0, VS1053_BANK_MELODY)
setChannelVolume(0, volume)
setChannelInstrument(0, 27)
setChannelPan(0, 0)

setChannelBank(1, VS1053_BANK_MELODY)
setChannelVolume(1, volume)
setChannelInstrument(1, 11)
setChannelPan(1, 127)

setChannelBank(2, VS1053_BANK_DRUMS1)
setChannelInstrument(2, 0)
setChannelVolume(2, volume)

interval = 150
next_time = supervisor.ticks_ms()
HAT = 42
KICK = 36
SNARE = 38
drum_pattern = [
    [HAT,KICK],[],[HAT],[],[HAT,SNARE],[],[HAT],[KICK],
    [HAT],[KICK],[HAT],[],[HAT,SNARE],[],[HAT],[],
    [HAT,KICK],[],[HAT],[],[HAT,SNARE],[],[HAT],[KICK],
    [],[],[],[],[SNARE],[],[],[]
]
drum_pattern_index = 0
drums_playing = False

pins = [3, 2, 4, 1, 5, 0, 6]
touch_states1 = [False] * len(scale)
touch_states2 = [False] * len(scale)

def play_touches(cap, channel, touch_states):
    for i in range(len(scale)):
        touched = cap[pins[i]].value
        if (not touch_states[i] and touched):
                noteOn(channel, root + scale[i], 127)
#        if (touch_states[i] and not touched):
#                 noteOff(root + scale[i])
        touch_states[i] = touched;

def next_scale():
    global scale_num, scale
    scale_num += 1
    scale_num %= len(scales)
    scale = scales[scale_num]
    play_scale()

def play_scale():
    for note in scale:
        noteOn(0, root + note, 120)
        #time.sleep(0.05)

def knob():
    global volume
    position = 128 - (potentiometer.value / 512)
    position = math.floor(max(0, min(position, 127)))
    if (abs(position - volume) > 2):
        volume = position
        setChannelVolume(0, volume)
        setChannelVolume(1, volume)
        setChannelVolume(2, volume)

def buttons():
    global drums_playing, next_time
    button1.update()
    if button1.fell:
        drums_playing = not drums_playing
        next_time = supervisor.ticks_ms()
    button2.update()
    if button2.fell:
        next_scale()

def playDrums():
    global next_time, drum_pattern_index
    if (drums_playing):
        now = supervisor.ticks_ms()
        if (now > next_time):
            for note in drum_pattern[drum_pattern_index]:
                noteOn(2, note, 120)
            next_time += interval
            drum_pattern_index += 1
            drum_pattern_index %= len(drum_pattern)

"""
# loop timing tester
while True:
    start = supervisor.ticks_ms()
    reps = 100
    for count in range(reps):
        knob()
        buttons()
        play_touches(cap1, 0, touch_states1)
        play_touches(cap2, 1, touch_states2)
        playDrums()
    print((supervisor.ticks_ms() - start) / reps)
"""

# startup sequence
knob()
play_scale()

while True:
    knob()
    buttons()
    play_touches(cap1, 0, touch_states1)
    play_touches(cap2, 1, touch_states2)
    playDrums()



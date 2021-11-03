import board
import time
import busio

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

setChannelBank(0, VS1053_BANK_MELODY)
setChannelVolume(0, 127)

scale = [60, 62, 64, 65, 67, 69, 71, 72]

for instrument in range(127):
    print('instrument: ' + str(instrument))
    setChannelInstrument(0, instrument)
    for note in scale:
        noteOn(0, note, 60)
        time.sleep(0.1)
    time.sleep(1)
    for note in scale:
        noteOff(0, note)
    time.sleep(0.5)

import board

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner
from kmk.modules.midi import MidiKeys

knob = KMKKeyboard()
knob.matrix = KeysScanner([])

media_keys = MediaKeys()
knob.extensions.append(media_keys)

midi_keys = MidiKeys()
knob.extensions.append(midi_keys)

# Rotary encoders that also acts as keys
encoder_handler = EncoderHandler()
encoder_handler.divisor = 4
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D9, board.D10, board.D3),
    (board.D7, board.D8, board.D6),
)

global bkMidiValue
bkMidiValue = [6, 29, 43]

def bkMidiIncrement(thisMidiChannel):
    print("midi CC + " + str(thisMidiChannel) + ":" + str(thisMidiChannel))
    bkMidiValue[thisMidiChannel] = bkMidiValue[thisMidiChannel] + 1
    return bkMidiValue[thisMidiChannel]

def bkMidiDecrement(thisMidiChannel):
    print("midi CC - " + str(thisMidiChannel) + ":" + str(thisMidiChannel))
    bkMidiValue[thisMidiChannel] = bkMidiValue[thisMidiChannel] + 1
#    return bkMidiValue[thisMidiChannel]
    return 8

def bkMidiIncrement(thisMidiChannel):
    print("midi CC + " + str(thisMidiChannel) + ":" + str(bkMidiValue[thisMidiChannel]))
    bkMidiValue[thisMidiChannel] = bkMidiValue[thisMidiChannel] + 1
    return bkMidiValue[thisMidiChannel]

def bkMidiDecrement(thisMidiChannel):
    print("midi CC - " + str(thisMidiChannel) + ":" + str(bkMidiValue[thisMidiChannel]))
    bkMidiValue[thisMidiChannel] = bkMidiValue[thisMidiChannel] - 1
    return bkMidiValue[thisMidiChannel]

encoder_handler.map = (
    ((KC.MIDI_CC(0,bkMidiIncrement(0)), KC.MIDI_CC(0,bkMidiDecrement(0)), KC.N0), (KC.MIDI_CC(1,bkMidiIncrement(1)), KC.MIDI_CC(1,bkMidiDecrement(1)), KC.N0), (KC.MIDI_CC(2,bkMidiIncrement(2)), KC.MIDI_CC(2,bkMidiDecrement(2)), KC.VOLD)),
)

knob.modules.append(encoder_handler)

print('ANAVI Knobs 3')

print(bkMidiValue[0])
print(bkMidiValue[1])
print(bkMidiValue[2])

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb_ext)

knob.keymap = [[KC.MIDI_CC]]

if __name__ == '__main__':
    knob.go()

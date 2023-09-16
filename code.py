import board

# from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner
from kmk.modules.midi import MidiKeys

knob = KMKKeyboard()
knob.matrix = KeysScanner([])

# media_keys = MediaKeys()
# knob.extensions.append(media_keys)

# added midi module
midi_keys = MidiKeys()
knob.modules.append(midi_keys)

# Rotary encoders that also acts as keys
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D9, board.D10, board.D3),
    (board.D7, board.D8, board.D6),
)

# setup array for MIDI Channels
knobsMidi = [1, 1, 1]
print(knobsMidi[0])
print(knobsMidi[1])
print(knobsMidi[2])

encoder_handler.map = (
    (KC.MIDI_CC(0, 1), KC.MIDI_CC(0, 0), KC.MIDI_CC(0, 2)),
    (KC.MIDI_CC(1, 1), KC.MIDI_CC(1, 0), KC.MIDI_CC(1, 2)),
    (KC.MIDI_CC(2, 1), KC.MIDI_CC(2, 0), KC.MIDI_CC(2, 2)),
)

# original encoder handler map
# encoder_handler.map = (
#   ((KC.VOLD, KC.VOLU, KC.MUTE), (KC.UP, KC.DOWN, KC.A), (KC.RIGHT, KC.LEFT, KC.B)),
# )


knob.modules.append(encoder_handler)


print("ANAVI Knobs 3 KMK MIDI")

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb_ext)

knob.keymap = [[KC.MUTE]]

if __name__ == "__main__":
    knob.go()

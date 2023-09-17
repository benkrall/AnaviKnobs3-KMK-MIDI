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

class MidiCcEncoderHandler(EncoderHandler):
    def __init__(self):
        super().__init__()
        self.midiValues = [6, 29, 43]
        print("self.midiValues " + str([6, 29, 43]))

    def on_move_do(self, keyboard, encoder_id, state):
        if state['direction'] == -1:  # left
            incr = -1
        else:
            incr = 1
        self.miniValues[encoder_id] += incr
        print("on_move_do " + str(encoder_id) + " = " + str(self.miniValues[encoder_id]) + " (incr " + str(incr) + ")")
        KC.MIDI_CC(encoder_id, self.miniValues[encoder_id])

    def on_button_do(self, keyboard, encoder_id, state):
        print("on_button_do " + str(encoder_id))
        # do nothing

# Rotary encoders that also acts as keys
encoder_handler = MidiCcEncoderHandler()
encoder_handler.divisor = 4
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D9, board.D10, board.D3),
    (board.D7, board.D8, board.D6),
)

knob.modules.append(encoder_handler)

print('ANAVI Knobs 3')

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

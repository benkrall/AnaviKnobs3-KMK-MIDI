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
knob.modules.append(midi_keys)

class MidiCcEncoderHandler(EncoderHandler):
    def __init__(self):
        super().__init__()
        self.midiValues = [6, 29, 43]
        print("@init self.midiValues " + str([6, 29, 43]))
        # no matter what these self.map is set to, it will not output MIDI_CC but will execute the code below
        """
        self.map = (
            ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        )
        """

        self.map = (
            ((KC.MIDI_CC(0, 0), KC.MIDI_CC(0, 1), KC.MIDI_CC(0, 2)), (KC.MIDI_CC(1, 0), KC.MIDI_CC(1, 1), KC.MIDI_CC(1, 2)), (KC.MIDI_CC(2, 0), KC.MIDI_CC(2, 1), KC.MIDI_CC(2, 2))),
        )


    def on_move_do(self, keyboard, encoder_id, state):
        if state['direction'] == -1:  # left
            incr = -1
            print("moving left")
        else:
            incr = 1
            print("moving right")
        self.midiValues[encoder_id] += incr
        if self.midiValues[encoder_id] < 0:
            self.midiValues[encoder_id] = 0  # limit low value to 0
        if self.midiValues[encoder_id] > 127:
            self.midiValues[encoder_id] = 127  # limit high value to 127
        KC.MIDI_CC(encoder_id, self.midiValues[encoder_id])
        print("@handler self.midiValues " + str(self.midiValues))
        print("on_move_do control " + str(encoder_id) + " value " + str(self.midiValues[encoder_id])
              + " (incr " + str(incr) + ")")

    def on_button_do(self, keyboard, encoder_id, state):
        print("on_button_do " + str(encoder_id))
        # do nothing

# Rotary encoders that also acts as keys
encoder_handler = MidiCcEncoderHandler() #uncomment this line & comment map below to use custom handler
#encoder_handler = EncoderHandler() # uncomment this line and map below to actually send MIDI_CC
encoder_handler.divisor = 4
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D10, board.D9, board.D3),
    (board.D8, board.D7, board.D6),
)

# each encoder needs a map; assign down here if using stock EncoderHandler, does send MIDI_CC
"""
encoder_handler.map = (
    ((KC.MIDI_CC(0, 0), KC.MIDI_CC(0, 1), KC.MIDI_CC(0, 2)), (KC.MIDI_CC(1, 0), KC.MIDI_CC(1, 1), KC.MIDI_CC(1, 2)), (KC.MIDI_CC(2, 0), KC.MIDI_CC(2, 1), KC.MIDI_CC(2, 2))),
)
"""

knob.modules.append(encoder_handler)

print('ANAVI Knobs 3')

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=15,
    val_default=15,
    animation_mode=AnimationModes.RAINBOW,
)
knob.extensions.append(rgb_ext)

knob.keymap = [[KC.N0]]

if __name__ == '__main__':
    knob.go()

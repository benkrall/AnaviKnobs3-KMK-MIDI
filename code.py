import board
import adafruit_midi
import usb_midi

# from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner
from kmk.modules.midi import MidiKeys

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_on import  NoteOn
from adafruit_midi.note_off import  NoteOff

knob = KMKKeyboard()
knob.matrix = KeysScanner([])

# media_keys = MediaKeys()
# knob.extensions.append(media_keys)

midi_keys = MidiKeys()
knob.modules.append(midi_keys)

class MidiCcEncoderHandler(EncoderHandler):
    def __init__(self):
        super().__init__()

        try:
            self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        except IndexError:
            self.midi = None
            # if debug_enabled:
            print('No midi device found.')

        self.midiValues = [127, 127, 127]
        print("@init self.midiValues " + str(self.midiValues))

        self.map = (
            ((KC.N0, KC.N0, KC.N0), (KC.N0, KC.N0, KC.N0), (KC.N0, KC.N0, KC.N0)),
        )

    def on_move_do(self, keyboard, encoder_id, state):
        print("entered on_move_do")
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
        print("@handler self.midiValues " + str(self.midiValues))
        print("on_move_do control " + str(encoder_id) + " value " + str(self.midiValues[encoder_id])
              + " (incr " + str(incr) + ")")

        if self.midi:
            self.midi.send(ControlChange(encoder_id, self.midiValues[encoder_id]))

    def on_button_do(self, keyboard, encoder_id, state):
        print("on_button_do " + str(encoder_id))
        #send midi note 100>102 on and then note off
        if self.midi:
            self.midi.send(NoteOn(encoder_id+100))
            time.sleep(1)
            self.midi.send(NoteOff(encoder_id+100))

# Rotary encoders that also acts as keys
encoder_handler = MidiCcEncoderHandler()
encoder_handler.divisor = 2
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D10, board.D9, board.D3),
    (board.D8, board.D7, board.D6),
)

knob.modules.append(encoder_handler)

print('ANAVI Knobs 3 KMK-MIDI')

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

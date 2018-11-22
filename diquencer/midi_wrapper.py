import logging
from enum import Enum


class Mute(Enum):
    ON = 127
    OFF = 0


class MIDIWrapper:

    BANKS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

    def __init__(self, channel, midi_out):
        self._channel = channel - 1
        self._midi_out = midi_out

    def change_pattern(self, bank, pattern):
        try:
            bank_number = self.BANKS.index(bank)
        except ValueError:
            logging.error(f'Cannot change pattern: bank {bank} is invalid.')
        self._midi_out.send_message([
            0xC0 + self._channel,
            (pattern - 1) + bank_number * 16
        ])

    def start(self):
        self._midi_out.send_message([0xFA])

    def stop(self):
        self._midi_out.send_message([0xFC])

    def clock(self):
        self._midi_out.send_message([0xF8])

    def mute(self, track: int, mute_state: Mute) -> None:
        self._midi_out.send_message((175 + track, 94, mute_state.value))

from enum import Enum

import rtmidi
from rtmidi.midiconstants import PROGRAM_CHANGE, SONG_START, SONG_STOP, TIMING_CLOCK

from .exceptions import MIDIOutputError, InvalidBank


class Mute(Enum):
    ON = 127
    OFF = 0


class MIDIWrapper:

    BANKS = ("A", "B", "C", "D", "E", "F", "G", "H")

    def __init__(self, channel=1):
        self.channel = channel
        self._midi_out = rtmidi.MidiOut()
        self._ports = self._midi_out.get_ports()

    @property
    def output_ports(self):
        return self._ports

    def raise_if_port_closed(self):
        if not self._midi_out.is_port_open():
            raise MIDIOutputError(
                "MIDI output port is closed. Please open the port first."
            )

    def set_output_port(self, port: str) -> None:
        try:
            port_id = self._ports.index(port)
        except ValueError:
            raise MIDIOutputError("Name of selected MIDI output is invalid.")

        self._midi_out.close_port()
        try:
            self._midi_out.open_port(port_id)
        except rtmidi.InvalidPortError:
            raise MIDIOutputError("ID of selected MIDI output is invalid.")

    def change_pattern(self, bank: str, pattern: int):
        try:
            bank_number = self.BANKS.index(bank)
            self._midi_out.send_message(
                [PROGRAM_CHANGE + self.channel - 1, (pattern - 1) + bank_number * 16]
            )
        except ValueError:
            raise InvalidBank(f"Cannot change pattern: bank {bank} is invalid.")

    def start(self):
        self._midi_out.send_message([SONG_START])

    def stop(self):
        self._midi_out.send_message([SONG_STOP])

    def clock(self):
        self._midi_out.send_message([TIMING_CLOCK])

    def mute(self, track: int, mute_state: Mute) -> None:
        self._midi_out.send_message((175 + track, 94, mute_state.value))

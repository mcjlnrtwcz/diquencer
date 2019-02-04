import logging
from typing import Union

from .engine import SequencerEngine
from .midi_wrapper import MIDIWrapper
from .models import Pattern
from .sequence import Sequence


class SequencerException(Exception):
    pass


class Sequencer:

    def __init__(self, sequence=None, midi_channel=1, start_callback=None):
        self._sequence = sequence
        self._midi = MIDIWrapper(midi_channel)
        self._start_callback = start_callback
        self._engine = None

    @property
    def is_playing(self) -> bool:
        if self._engine:
            return self._engine.is_alive()
        return False

    @property
    def current_pattern(self) -> Union[Pattern, None]:
        if self._engine:
            return self._engine.current_pattern

    @property
    def next_pattern(self) -> Union[Pattern, None]:
        if self._engine:
            return self._engine.next_pattern

    def start(self, blocking=False):
        if self._sequence:
            self._engine = SequencerEngine(
                self._sequence,
                self._midi,
                self._start_callback
            )
            self._engine.start()
            if blocking:
                self._engine.join()
        else:
            logging.warning('Cannot start sequencer. Sequence is not set.')

    def stop(self):
        if self._engine.is_alive():
            self._engine.stop()
            self._engine.join()
        else:
            logging.warning('Sequencer has already been stopped.')

    def get_position(self):
        if self._engine and self._engine.is_alive():
            return str(self._engine.get_position())

    def get_output_ports(self):
        return self._midi.get_output_ports()

    def set_output_port(self, port: str) -> bool:
        return self._midi.set_output_port(port)

    def set_sequence(self, sequece):
        if self._engine and self._engine.is_alive():
            raise SequencerException('Cannot set sequence while running.')
        self._sequence = sequece

    def load_sequence(self, sequence_data):
        if self._engine and self._engine.is_alive():
            raise SequencerException('Cannot load sequence while running.')
        self._sequence = Sequence.from_raw_data(sequence_data)

    def set_midi_channel(self, channel: int) -> None:
        self._midi.channel = channel

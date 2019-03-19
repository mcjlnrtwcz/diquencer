import logging
from typing import List, Union

from .engine import SequencerEngine
from .midi_wrapper import MIDIWrapper
from .models import Pattern
from .sequence import Sequence


class SequencerException(Exception):
    pass


class Sequencer:
    def __init__(self, sequence=None, midi_channel=1, start_callback=None):
        self._sequence = sequence
        self._sequence_data = None
        self._midi = MIDIWrapper(midi_channel)
        self._start_callback = start_callback
        self._engine = None

    @property
    def is_playing(self) -> bool:
        if self._engine:
            return self._engine.is_alive()
        return False

    @property
    def patterns(self) -> List[Pattern]:
        if self._sequence:
            return self._sequence.patterns
        return []

    @property
    def current_pattern(self) -> Union[Pattern, None]:
        if self._engine:
            return self._engine.current_pattern
        return None

    @property
    def next_pattern(self) -> Union[Pattern, None]:
        if self._engine:
            return self._engine.next_pattern
        return None

    @property
    def position(self) -> str:
        if self._engine and self._engine.is_alive():
            return str(self._engine.position)
        return ""

    @property
    def output_ports(self):
        return self._midi.output_ports

    def set_output_port(self, port: str):
        self._midi.set_output_port(port)

    def set_midi_channel(self, channel: int):
        self._midi.channel = channel

    def set_sequence(self, sequece: Sequence):
        if self._engine and self._engine.is_alive():
            raise SequencerException("Cannot set sequence while running.")
        self._sequence = sequece

    def load_sequence(self, sequence_data):
        self._sequence_data = sequence_data
        self._initialize_sequence(sequence_data, 0)

    def set_start_pattern(self, start_pattern_idx: int):
        self._initialize_sequence(self._sequence_data, start_pattern_idx)

    def start(self, blocking=False):
        if self._sequence:
            self._engine = SequencerEngine(
                self._sequence, self._midi, self._start_callback
            )
            self._engine.start()
            if blocking:
                self._engine.join()
        else:
            logging.warning("Cannot start sequencer. Sequence is not set.")

    def stop(self):
        if self._engine.is_alive():
            self._engine.stop()
            self._engine.join()
        else:
            logging.warning("Sequencer has already been stopped.")

    def _initialize_sequence(self, sequence, start_pattern_idx):
        """
        Create and store new sequence based on raw data. The sequence begins
        with specified pattern.
        """
        if self._engine and self._engine.is_alive():
            raise SequencerException("Cannot load sequence while running.")
        self._sequence = Sequence.from_raw_data(sequence, start_pattern_idx)

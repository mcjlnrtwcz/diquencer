import logging

from .engine import SequencerEngine
from .midi_wrapper import MIDIWrapper
from .sequence import Sequence


class SequencerException(Exception):
    pass


class Sequencer:

    def __init__(self, sequence=None, midi_channel=1, stop_callback=None):
        self._sequence = sequence
        self._midi = MIDIWrapper(midi_channel)
        self._engine = None
        self._stop_callback = stop_callback

    def start(self):
        if self._sequence:
            self._engine = SequencerEngine(
                self._sequence,
                self._midi,
                self._stop_callback
            )
            self._engine.start()
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

    @property
    def is_playing(self):
        if self._engine:
            return self._engine.is_alive()
        return False

    def set_midi_channel(self, channel: int) -> None:
        self._midi.channel = channel

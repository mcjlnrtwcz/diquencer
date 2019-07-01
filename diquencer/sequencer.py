from typing import List, Union

from .engine import SequencerEngine
from .midi_wrapper import MIDIWrapper
from .models import Pattern
from .sequence import Sequence
from .exceptions import SequencerTransportError, SequenceNotSet


class Sequencer:
    def __init__(
        self, sequence=None, midi_channel=1, start_callback=None, error_callback=None
    ):
        """
        When an error occurs, error_callback function will be execuded and exception
        will be passed as an argument.
        """
        self._sequence = sequence
        self._sequence_data = None
        self._midi = MIDIWrapper(midi_channel)
        self._start_callback = start_callback
        self._error_callback = error_callback
        self._engine = None

    @property
    def is_playing(self) -> bool:
        try:
            return self._engine.is_alive()
        except AttributeError:
            return False

    @property
    def patterns(self) -> List[Pattern]:
        try:
            return self._sequence.patterns
        except AttributeError:
            return []

    @property
    def current_pattern(self) -> Union[Pattern, None]:
        try:
            return self._engine.current_pattern
        except AttributeError:
            return None

    @property
    def next_pattern(self) -> Union[Pattern, None]:
        try:
            return self._engine.next_pattern
        except AttributeError:
            return None

    @property
    def position(self) -> str:
        if self._is_engine_running():
            return str(self._engine.position)
        return ""

    @property
    def output_ports(self):
        return self._midi.output_ports

    def set_output_port(self, port: str):
        """
        Open MIDI output port. Raise MIDIOutputError if port cannot be opened.
        """
        self._midi.set_output_port(port)

    def set_midi_channel(self, channel: int):
        self._midi.channel = channel

    def set_sequence(self, sequece: Sequence):
        if self._is_engine_running():
            raise SequencerTransportError(
                "Cannot set sequence while sequencer is running."
            )
        self._sequence = sequece

    def load_sequence(self, sequence_data):
        """
        Load sequence form raw data (i.e. dict). Raise SequencerTransportError if
        sequencer is working.
        """
        self._sequence_data = sequence_data
        self._initialize_sequence(sequence_data)

    def set_start_pattern(self, start_pattern_idx: int):
        """
        Set start pattern of current sequence. Raise SequencerTransportError if
        sequencer is working.
        """
        self._initialize_sequence(self._sequence_data, start_pattern_idx)

    def start(self, blocking=False):
        """
        Start sequencer. Raise SequenceNotSet if sequence wasn't loaded. Raise
        MIDIOutputError if midi output port wasn't opened.
        """
        self._midi.raise_if_port_closed()

        if not self._sequence:
            raise SequenceNotSet("Cannot start sequencer. Sequence is not set.")

        self._engine = SequencerEngine(
            self._sequence, self._midi, self._start_callback, self._error_callback
        )
        self._engine.start()

        if blocking:
            self._engine.join()

    def stop(self):
        if not self._is_engine_running():
            raise SequencerTransportError("Sequencer has already been stopped.")

        self._engine.stop()
        self._engine.join()

    def _is_engine_running(self):
        try:
            return self._engine.is_alive()
        except AttributeError:
            return False

    def _initialize_sequence(self, sequence, start_pattern_idx=0):
        """
        Create and store new sequence based on raw data. The sequence begins
        with specified pattern.
        """
        if self._is_engine_running():
            raise SequencerTransportError("Cannot load sequence while running.")
        self._sequence = Sequence.from_raw_data(sequence, start_pattern_idx)

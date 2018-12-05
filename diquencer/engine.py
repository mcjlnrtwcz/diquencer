import logging
from threading import Event, Thread
from time import perf_counter, sleep

from .events import MuteEvent, PatternEvent, StopEvent
from .midi_wrapper import Mute
from .models import Position


class SequencerEngine(Thread):

    def __init__(self, sequence, midi_wrapper, stop_callback=None):
        super().__init__()
        self._sequence = sequence
        self._midi = midi_wrapper
        self._stop_callback = stop_callback
        self._pulsestamp = 0
        self._stop_event = Event()
        self._pulse_duration = 60.0 / self._sequence.tempo / 24.0

    def _pulse(self):
        start = perf_counter()
        while perf_counter() < start + self._pulse_duration:
            sleep(0.0001)

    def _mute_tracks(self, mutes):
        for track in range(1, 17):
            state = Mute.ON if track in mutes else Mute.OFF
            self._midi.mute(track, state)

    def run(self):
        if not self._midi.is_port_open():
            logging.warning('Cannot start engine. MIDI port is not open.')
            return

        logging.info(f'[{self.get_position()}] Sequencer started.')
        # Set initial pattern
        pattern_event = self._sequence.get_event(self._pulsestamp)
        pattern = pattern_event.pattern
        self._midi.change_pattern(pattern.bank_id, pattern.pattern_id)
        logging.info(f'[{self.get_position()}] Changing pattern to {pattern}.')
        # Set initial mutes
        mute_event = self._sequence.get_event(self._pulsestamp)
        self._mute_tracks(mute_event.mutes)
        logging.info(
            f'[{self.get_position()}] Muting tracks: {mute_event.mutes}.'
        )

        # Warm-up
        for pulse in range(24 * 4):
            self._midi.clock()
            self._pulse()

        self._midi.start()
        while not self._stop_event.is_set():
            self._pulse()
            self._midi.clock()

            event = self._sequence.get_event(self._pulsestamp)
            if isinstance(event, StopEvent):
                break
            if isinstance(event, PatternEvent):
                pattern = event.pattern
                self._midi.change_pattern(pattern.bank_id, pattern.pattern_id)
                logging.info(
                    f'[{self.get_position()}] Changing pattern to {pattern}.')
            if isinstance(event, MuteEvent):
                self._mute_tracks(event.mutes)
                logging.info(
                    f'[{self.get_position()}] Muting tracks: {event.mutes}.')

            self._pulsestamp += 1

        self._midi.stop()
        logging.info(f'[{self.get_position()}] Sequencer stopped.')

        self._sequence.reset()

        if self._stop_callback:
            self._stop_callback()

    def stop(self):
        self._stop_event.set()

    def get_position(self):
        return Position(self._pulsestamp)

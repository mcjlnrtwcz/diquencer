import logging
from threading import Event, Thread
from time import perf_counter, sleep

from .events import MuteEvent, PatternEvent, StopEvent
from .midi_wrapper import Mute
from .models import Position


class SequencerEngine(Thread):

    def __init__(
            self,
            sequence,
            midi_wrapper,
            start_callback=None
    ):
        super().__init__()
        self._sequence = sequence
        self._midi = midi_wrapper
        self._stat_callback = start_callback
        self._pulsestamp = 0
        self._stop_event = Event()
        self._pulse_duration = 60.0 / self._sequence.tempo / 24.0

    def _pulse(self):
        start = perf_counter()
        while perf_counter() < start + self._pulse_duration:
            sleep(0.0001)

    def _play_tracks(self, playing_tracks):
        for track in range(1, 17):
            state = Mute.OFF if track in playing_tracks else Mute.ON
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
        # Set initial playing tracks
        mute_event = self._sequence.get_event(self._pulsestamp)
        self._play_tracks(mute_event.playing_tracks)
        logging.info(
            f'[{self.get_position()}] Playing tracks: '
            f'{mute_event.playing_tracks}.'
        )

        # Warm-up
        for pulse in range(24 * 4):
            self._midi.clock()
            self._pulse()

        self._stat_callback()
        self._midi.start()
        while not self._stop_event.is_set():
            self._midi.clock()
            self._pulse()

            event = self._sequence.get_event(self._pulsestamp)
            if isinstance(event, StopEvent):
                break
            if isinstance(event, PatternEvent):
                pattern = event.pattern
                self._midi.change_pattern(pattern.bank_id, pattern.pattern_id)
                logging.info(
                    f'[{self.get_position()}] Changing pattern to {pattern}.')
            if isinstance(event, MuteEvent):
                self._play_tracks(event.playing_tracks)
                logging.info(
                    f'[{self.get_position()}] Playing tracks: '
                    f'{event.playing_tracks}.')

            self._pulsestamp += 1

        self._midi.stop()
        logging.info(f'[{self.get_position()}] Sequencer stopped.')

        self._sequence.reset()

    def stop(self):
        self._stop_event.set()

    def get_position(self):
        return Position(self._pulsestamp)

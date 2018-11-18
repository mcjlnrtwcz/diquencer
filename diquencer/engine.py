import logging
from threading import Event, Thread
from time import perf_counter, sleep

from midi_wrapper import MIDIWrapper
from models import Position


class SequencerEngine(Thread):

    def __init__(self, sequence, midi_out):
        super().__init__()
        self._sequence = sequence
        self._midi = MIDIWrapper(1, midi_out)
        self._pulsestamp = 0
        self._stop_event = Event()
        self._pulse_duration = 60.0 / self._sequence.tempo / 24.0

    def _pulse(self):
        start = perf_counter()
        while perf_counter() < start + self._pulse_duration:
            sleep(0.0001)

    def run(self):
        logging.info(f'[{self.get_position()}] Sequencer started.')

        # Set first pattern
        event = self._sequence.get_event(self._pulsestamp)
        self._midi.change_pattern(event.bank_id, event.pattern_id)
        logging.info(f'[{self.get_position()}] Changing pattern to {event}.')

        # Warm-up
        for pulse in range(24 * 4):
            self._midi.clock()
            self._pulse()

        self._midi.start()
        while not self._stop_event.is_set():
            self._pulse()
            self._midi.clock()

            event = self._sequence.get_event(self._pulsestamp)
            if event == 'stop':
                break
            if event:
                self._midi.change_pattern(event.bank_id, event.pattern_id)
                logging.info(
                    f'[{self.get_position()}] Changing pattern to {event}.')

            self._pulsestamp += 1

        self._midi.stop()
        logging.info(f'[{self.get_position()}] Sequencer stopped.')

        self._sequence.reset()

    def stop(self):
        self._stop_event.set()

    def get_position(self):
        return Position(self._pulsestamp)

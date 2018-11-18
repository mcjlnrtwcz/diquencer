import logging

from engine import SequencerEngine


class Sequencer:

    def __init__(self, midi_out, sequence=None):
        self._midi_out = midi_out
        self._sequence = sequence
        self._engine = None

    def start(self):
        # TODO: Is port open?
        if self._sequence:
            self._engine = SequencerEngine(self._sequence, self._midi_out)
            self._engine.start()
        else:
            logging.warning('Cannot start sequencer. Sequence is not set.')

    def stop(self):
        if self._engine.is_alive():
            self._engine.stop()
            self._engine.join()
        else:
            logging.warning('Sequencer has already been stopped')

    def get_position(self):
        if self._engine and self._engine.is_alive():
            return str(self._engine.get_position())

    def get_midi_outs(self):
        return self._midi_out.get_ports()

    def set_midi_out(self, midi_out_id):
        if not self._midi_out.is_port_open():
            self._midi_out.open_port(midi_out_id)
        else:
            logging.debug('Selected MIDI port is already opened.')

    def load_sequence(self, sequence_data):
        self._sequence = Sequence(**sequence_data)

    @property
    def is_playing(self):
        if self._engine:
            return self._engine.is_alive()
        return False
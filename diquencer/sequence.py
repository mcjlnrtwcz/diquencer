from copy import deepcopy

from .models import Pattern, PatternSequence


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternSequence)

    def __init__(self, tempo=120, pattern_seqs=[]):
        self.tempo = tempo
        self._pattern_seqs = pattern_seqs
        self._patterns_blueprint = deepcopy(self._pattern_seqs)  # For reset
        self._stop_event = 0

        # Get pulsestamp of stop event
        if self._pattern_seqs:
            last_pattern_seq = self._pattern_seqs[-1]
            self._stop_event = last_pattern_seq.pulsestamp
            self._stop_event += (
                last_pattern_seq.pattern.length
                * last_pattern_seq.repetitions
                * 24 * 4
            )

    @classmethod
    def from_raw_data(cls, raw_data):
        pattern_seqs = []
        last_event_pulses = 0

        for index, pattern_sequence in enumerate(raw_data['sequence']):
            pattern = Pattern(
                pattern_sequence['pattern'],
                pattern_sequence['bank'],
                pattern_sequence['length']
            )
            if index != 0:
                last_event_pulses += (
                    pattern.length
                    * pattern_sequence['repetitions']
                    * 24 * 4
                )
            pattern_seq = PatternSequence(
                pattern,
                pattern_sequence['repetitions'],
                last_event_pulses
            )
            pattern_seqs.append(pattern_seq)

        return cls(raw_data['tempo'], pattern_seqs)

    def get_event(self, pulsestamp):
        if len(self._pattern_seqs) > 0:
            next_pattern_sequence = self._pattern_seqs[0]
            if next_pattern_sequence.pulsestamp - 24 <= pulsestamp:
                return self._pattern_seqs.pop(0).pattern
        else:
            if pulsestamp == self._stop_event:
                return 'stop'

    def reset(self):
        self._pattern_seqs = deepcopy(self._patterns_blueprint)

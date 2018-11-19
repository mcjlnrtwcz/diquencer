from copy import deepcopy

from .models import Pattern, PatternSequence


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternSequence)

    def __init__(self, tempo, sequence):
        self.tempo = tempo
        self._patterns_blueprint = []
        self._patterns = []

        last_event_pulses = 0

        for index, pattern_sequence in enumerate(sequence):
            pattern = Pattern(
                pattern_sequence['pattern'],
                pattern_sequence['bank'],
                pattern_sequence['length']
            )
            if index != 0:
                last_event_pulses += (pattern_sequence['length']
                                      * pattern_sequence['repetitions']
                                      * 24 * 4)
            pattern_seq = PatternSequence(pattern, last_event_pulses)
            self._patterns_blueprint.append(pattern_seq)

        self._patterns = deepcopy(self._patterns_blueprint)  # For reset

        self._stop_event = last_event_pulses
        self._stop_event += (sequence[-1]['length']
                             * sequence[-1]['repetitions']
                             * 24 * 4)

    def get_event(self, pulsestamp):
        if len(self._patterns) > 0:
            next_pattern_sequence = self._patterns[0]
            if next_pattern_sequence.pulsestamp - 24 <= pulsestamp:
                return self._patterns.pop(0).pattern
        else:
            if pulsestamp == self._stop_event:
                return 'stop'

    def reset(self):
        self._patterns = deepcopy(self._patterns_blueprint)

class Position:

    def __init__(self, pulses):
        self.pulses = pulses % 24
        self.beats = int(pulses / 24) % 4
        self.measures = int(pulses / (24 * 4))

    def __str__(self):
        # This assumes that songs won't be longer than 999 measures
        return '{}.{}.{}'.format(
            str(self.measures).zfill(3),
            self.beats,
            str(self.pulses).zfill(2)
        )


class Pattern:

    def __init__(self, pattern_id, bank_id, length):
        self.pattern_id = pattern_id
        self.bank_id = bank_id
        self.length = length

    def __str__(self):
        return f'{self.bank_id}{self.pattern_id}'


class PatternSequence:

    def __init__(self, pattern, repetitions, pulsestamp=0):
        self.pattern = pattern
        self.repetitions = repetitions
        self.pulsestamp = pulsestamp

    def __str__(self):
        return '{}{} @ {}'.format(
            self.pattern.bank_id,
            self.pattern.pattern_id,
            Position(self.pulsestamp)
        )

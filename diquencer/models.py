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

    def __init__(self, pattern_id, bank_id, length, mutes=[]):
        self.pattern_id = pattern_id
        self.bank_id = bank_id
        self.length = length

    def __str__(self):
        return f'{self.bank_id}{self.pattern_id}'


class Event:

    def __init__(self, pulsestamp):
        self.pulsestamp = pulsestamp

    def __str__(self):
        return f'{self.__class__.__name__} @ {Position(self.pulsestamp)}'


class MuteEvent(Event):

    def __init__(self, pulsestamp, mutes):
        super().__init__(pulsestamp)
        self.mutes = mutes


class PatternEvent(Event):

    def __init__(self, pulsestamp, pattern, repetitions):
        super().__init__(pulsestamp)
        self.pattern = pattern
        self.repetitions = repetitions

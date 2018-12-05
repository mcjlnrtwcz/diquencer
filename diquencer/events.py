from .models import Position


class SequenceEvent:

    def __init__(self, pulsestamp):
        self.pulsestamp = pulsestamp

    def __str__(self):
        return f'{self.__class__.__name__} @ {Position(self.pulsestamp)}'


class MuteEvent(SequenceEvent):

    def __init__(self, pulsestamp, playing_tracks):
        super().__init__(pulsestamp)
        self.playing_tracks = playing_tracks


class PatternEvent(SequenceEvent):

    def __init__(self, pulsestamp, pattern, repetitions):
        super().__init__(pulsestamp)
        self.pattern = pattern
        self.repetitions = repetitions


class StopEvent(SequenceEvent):
    pass

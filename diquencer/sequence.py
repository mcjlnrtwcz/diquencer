from copy import deepcopy
from typing import Union

from .events import MuteEvent, PatternEvent, SequenceEvent, StopEvent
from .models import Pattern, Position


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternEvent)

    def __init__(self, tempo=120, events=[]):
        self.tempo = tempo
        self._events = events

        # Get pulsestamp of stop event
        if self._events:
            last_event = self._events[-2]  # -1 is MuteEvent
            stop_event = StopEvent(
                last_event.pulsestamp
                + last_event.pattern.length
                * last_event.repetitions
                * 24 * 4
            )
            self._events.append(stop_event)

        self._events_blueprint = deepcopy(self._events)  # For reset

    @classmethod
    def from_raw_data(cls, raw_data):
        events = []
        last_event_pulses = 0

        for index, event in enumerate(raw_data['sequence']):
            pattern = Pattern(
                event['name'],
                event['pattern'],
                event['bank'],
                event['length'],
            )
            if index != 0:
                last_event_pulses += (
                    pattern.length
                    * event['repetitions']
                    * 24 * 4
                )

            pattern_event = PatternEvent(
                0 if index == 0 else last_event_pulses - 24,
                pattern,
                event['repetitions'],
            )
            events.append(pattern_event)

            mute_event = MuteEvent(
                0 if index == 0 else last_event_pulses - 1,
                event['playing_tracks']
            )
            events.append(mute_event)

        return cls(raw_data['tempo'], events)

    @property
    def next_pattern(self) -> Union[Pattern, None]:
        pattern_it = filter(
            lambda event: isinstance(event, PatternEvent), self._events
        )
        try :
            pattern_event = next(pattern_it)
            return pattern_event.pattern
        except StopIteration:
            return None


    def get_event(self, pulsestamp: int) -> Union[SequenceEvent, None]:
        if self._events and self._events[0].pulsestamp == pulsestamp:
            return self._events.pop(0)

    def reset(self):
        self._events = deepcopy(self._events_blueprint)

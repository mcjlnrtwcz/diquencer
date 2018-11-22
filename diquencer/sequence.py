from copy import deepcopy

from .models import Pattern, Event, PatternEvent, MuteEvent


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternEvent)

    def __init__(self, tempo=120, events=[]):
        self.tempo = tempo
        self._events = events
        self._events_blueprint = deepcopy(self._events)  # For reset
        self._stop_event = 0

        # Get pulsestamp of stop event
        if self._events:
            last_event = self._events[-1]
            self._stop_event = last_event.pulsestamp
            self._stop_event += (
                last_event.pattern.length
                * last_event.repetitions
                * 24 * 4
            )

    @classmethod
    def from_raw_data(cls, raw_data):
        events = []
        last_event_pulses = 0

        for index, event in enumerate(raw_data['sequence']):
            pattern = Pattern(
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
                pattern,
                event['repetitions'],
                last_event_pulses - 24
            )
            events.append(pattern_event)

            mute_event = MuteEvent(
                last_event_pulses - 1,
                event['mutes']
            )
            events.append(mute_event)

        return cls(raw_data['tempo'], events)

    def get_event(self, pulsestamp: int) -> Event:
        if len(self._events) > 0:
            next_event = self._events[0]
            if next_event.pulsestamp == pulsestamp:
                return self._events.pop(0)
        else:
            if pulsestamp == self._stop_event:
                return 'stop'

    def reset(self):
        self._events = deepcopy(self._events_blueprint)

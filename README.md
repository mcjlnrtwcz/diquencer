# diquencer
Simple MIDI sequencing library for Python designed for [Elektron](https://www.elektron.se/) Digitakt.

## Usage
The main features of diquencer are pattern changes and track mutes.

### Initialization
Start with importing `Sequencer` class (which is the public API of diquencer):
```python
from diquencer import Sequencer
```
then you can initialize it with the following optional arguments:
```python
sequencer = Sequencer(
    midi_channel=1,
    start_callback=lambda: print("Called when the transport starts"),
    error_callback=lambda error: print(f"Something bad happened: {error}")
)
```
- `error` argument of `error_callback` is an exception (it doesn't need to be handled though).
- `midi_channel` value should be in the range from 1 to 16.

After initialization you can get available MIDI output ports and then select one:
```python
>>> sequencer.output_ports
['IAC Driver Bus 1', 'Digitakt Elektron MIDI']
>>> sequencer.set_output_port('Digitakt Elektron MIDI')
```

then you should feed the sequencer with data:
```python
sequence_data = {
    "tempo": 134,
    "sequence": [
        {
            "name": "Intro",
            "pattern": 9,
            "bank": "A",
            "length": 4,  # length of pattern in measures
            "repetitions": 2,
            "playing_tracks": [1, 3, 7]  # tracks that are NOT muted
        },
        {
            "name": "Outro",
            "pattern": 10,
            "bank": "A",
            "length": 4,
            "repetitions": 2,
            "playing_tracks": [2, 4, 8]
        }
    ]
}
sequencer.load_sequence(sequence_data)
```

### Running the sequencer

You can start (and stop) the playback with:
```python
>>> sequencer.start()
>>> sequencer.is_playing
True
>>> sequencer.stop()
```

By default `start` fuction is non-blocking (the actual sequencer runs in a separate thread). You can, however, make it blocking with an optional argument:
```python
>>> sequencer.start(blocking=True)
>>> sequencer.is_playing
False  # already finished
```

During playback (in non-blocking mode) you can enquire the sequencer about its status:
```python
>>> sequencer.position
'001.0.17'  # MEASURE.QUARTER_NOTE.PULSE
>>> sequencer.current_pattern.name
'Intro'
>>> sequencer.next_pattern.name
'Outro'
```

Playback may be started from any pattern you want:
```python
>>> sequencer.set_start_pattern(1)
>>> sequencer.start()
>>> sequencer.current_pattern.name
'Outro'
```
the argument of `set_start_pattern` is the index (starting from 0) of pattern in `sequence` list (see `sequence_data` in previous section).

If you wish, you can change the output MIDI channel and port (changes will have an effect after the playback restarts):
```python
sequencer.set_midi_channel(5)
```

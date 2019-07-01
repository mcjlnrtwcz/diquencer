class DiquencerException(Exception):
    pass


class SequencerTransportError(DiquencerException):
    """
    Error due to incompatible state of squencer transport (e.g. still playing).
    """


class SequenceNotSet(DiquencerException):
    pass


class MIDIOutputError(DiquencerException):
    pass


class InvalidBank(DiquencerException):
    """
    Invalid pattern bank was selected.
    """


class ChangePatternError(DiquencerException):
    """
    Pattern cannot be changed.
    """

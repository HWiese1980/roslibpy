__all__ = ["from_epoch", "to_epoch"]


def to_epoch(header_stamp):
    """
    Converts a Header/stamp dictionary of the shape

    ```
    {
        "stamp": {
            "secs": int,
            "nsecs": int
        }
    }
    ```

    into a Unix Epoch timestamp (seconds since January 1st, 1970)

    Args:
        header_stamp: dict; a dictionary of above described shape

    Returns: float; the corresponding Unix Epoch timestamp since The Epoch
    """
    secs = header_stamp["secs"]
    nsecs = header_stamp["nsecs"]
    stamp = secs + (nsecs * 1e-9)
    return stamp


def from_epoch(stamp):
    """
    Converts a Unix Epoch timestamp into a Header/stamp dictionary of the shape

    ```
    {
        "stamp": {
            "secs": int,
            "nsecs": int
        }
    }
    ```

    Args:
        stamp: float; a Unix Epoch timestamp

    Returns: float; the corresponding Unix Epoch timestamp
    """
    secs = int(stamp)
    nsecs = (stamp - secs) * 1e9
    return {
        "secs": secs,
        "nsecs": nsecs
    }

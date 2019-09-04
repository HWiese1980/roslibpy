__all__ = ["from_epoch", "to_epoch"]


def to_epoch(header_stamp):
    secs = header_stamp["secs"]
    nsecs = header_stamp["nsecs"]
    stamp = secs + (nsecs * 1e-9)
    return stamp


def from_epoch(stamp):
    secs = int(stamp)
    nsecs = (stamp - secs) * 1e9
    return {
        "secs": secs,
        "nsecs": nsecs
    }

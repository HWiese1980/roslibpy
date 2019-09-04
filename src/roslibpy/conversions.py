#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The following code is additional contribution to roslibpy
# Copyrighted Hendrik Wiese with MIT license

# Copyright(c) 2019 Hendrik Wiese

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

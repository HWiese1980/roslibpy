# The following code is additional contribution to roslibpy
# Copyrighted Hendrik Wiese with MIT license

# The MIT License(MIT)

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

"""
This module contains the ApproximateTimeSynchronizer; a message filter that
is supposed to synchronize two or more topics.

It should be considered unstable. The algorithm itself is very basic as it
just stores the latest messages for all registered topics and invokes a
callback function if all latest messages have a header/stamp within a given
interval from each other. All other messages will be dropped.

There is an optional unsynced callback that gets invoked every time that a
message arrives on a given topic. These messages won't get dropped; at least
not by the synchronizer.

This file could use some clean up and streamlining, and maybe a more
sophisticated algorithm.

Author: Hendrik Wiese (hendrik.wiese@dfki.de)
Date of issue: 2019-09-23

"""
import json

from roslibpy.conversions import to_epoch

__all__ = ["ApproximateTimeSynchronizer"]


class ApproximateTimeSynchronizer:
    def __init__(self, callback, slop=0.01):
        """
        Create an instance of the ApproximateTimeSynchronizer.

        Args:
            callback: callable; The callable is invoked if all latest messages
                have arrived within a given time frame according to their header
                stamp. The argument names must match the names given when
                registering a topic. (see `register`)
            slop: the maximum delta between the oldest and the youngest of the
                most recent messages on all registered topics.
        """
        self.callback = callback
        self.slop = slop
        self._last_messages = {}

    def _create_cb(self, name, unsynced_cb):
        def _cb(msg):
            try:
                # Try to parse json message
                msg = json.loads(msg["data"])
            except:
                pass
            self._last_messages[name] = msg
            self._on_new_message()
            if callable(unsynced_cb):
                unsynced_cb(msg)

        return _cb

    def _on_new_message(self):
        stamps = []
        for t, msg in self._last_messages.items():
            stamp = to_epoch(msg["header"]["stamp"])
            stamps.append(stamp)
        delta = (max(stamps) - min(stamps))
        if len(stamps) > 1 and delta < self.slop:
            self.callback(delta=delta, **self._last_messages)

    def register(self, topic, name, unsynced_cb=None):
        """
        Register a topic for synchronization. The optional unsynced callback
        will get called every time that a message arrives on this topic,
        disregard if it's in sync with other messages of this synchronizer.

        Args:
            topic: roslibpy.Topic; The roslibpy.Topic object to register
            name: str; The name of the parameter of the synchronizer callback
                that is filled with messages from this topic
            unsynced_cb: callable (optional); A callback function for the
                unsynchronized message on this topic
        """
        topic.subscribe(self._create_cb(name, unsynced_cb))

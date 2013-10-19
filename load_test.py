#!/usr/bin/env python
#    Copyright 2009 Google Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import httplib2
import random
import socket
import time
from threading import Event
from threading import Thread
from threading import current_thread
from urllib import urlencode

# Modify these values to control how the testing is done

# How many threads should be running at peak load.
NUM_THREADS = 10

TIME_AT_PEAK_QPS = 1 # minutes

DELAY_BETWEEN_THREAD_START = 2 # seconds

quitevent = Event()

def threadproc():
    """This function is executed by each thread."""
    print "Thread started: %s" % current_thread().getName()
    h = httplib2.Http(timeout=30)
    while not quitevent.is_set():
        for url in [
            "http://localhost:8080/",
            "http://localhost:8080/about/",
            "http://localhost:8080/cinemas/stephen-joseph-theatre/",
        ]:
            try:
                resp, content = h.request(url)
                if resp.status != 200:
                    print "Response not OK"
            except socket.timeout:
                pass

    print "Thread finished: %s" % current_thread().getName()


if __name__ == "__main__":
    runtime = (TIME_AT_PEAK_QPS * 60 + DELAY_BETWEEN_THREAD_START * NUM_THREADS)
    print "Total runtime will be: %d seconds" % runtime
    threads = []
    try:
        for i in range(NUM_THREADS):
            t = Thread(target=threadproc)
            t.start()
            threads.append(t)
            time.sleep(DELAY_BETWEEN_THREAD_START)
        print "All threads running"
        time.sleep(TIME_AT_PEAK_QPS*60)
        print "Completed full time at peak qps, shutting down threads"
    except:
        print "Exception raised, shutting down threads"

    quitevent.set()
    time.sleep(3)
    for t in threads:
        t.join(1.0)
    print "Finished"

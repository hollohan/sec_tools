#!/bin/bash

find /proc -type d -name "[0-9]*" -maxdepth 1 -exec bash -c 'echo ---{}---; cat {}/cmdline; echo' \; 2>/dev/null
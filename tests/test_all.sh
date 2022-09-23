#!/bin/bash

# $(which python3) is used to cover the case of Python virtual environments
$(which python3) pt4.py -f test_activate.txt
$(which python3) pt4.py -f test_toggle_trot.txt
$(which python3) pt4.py -f test_walk_square_slow.txt
$(which python3) pt4.py -f test_walk_square_fast.txt
$(which python3) pt4.py -f test_pitch_mid.txt
$(which python3) pt4.py -f test_pitch_max.txt
$(which python3) pt4.py -f test_yaw_mid.txt
$(which python3) pt4.py -f test_jump.txt
#$(which python3) pt4.py -f test_cancel_shutdown.txt
#$(which python3) pt4.py -f test_shutdown.txt

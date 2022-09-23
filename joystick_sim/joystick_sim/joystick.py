import time
import threading
from collections import deque
from enum import Enum
from UDPComms import Publisher


class Commands(Enum):
    L1 = 1
    R1 = 2
    X = 3
    SQUARE = 4
    CIRCLE = 5
    TRIANGLE = 6
    DPADX = 7
    DPADY = 8
    NONE = 99


class Joystick(threading.Thread):

    def __init__(self):
        # used for debugging
        self.write_log = False
        self.publish = True

        MESSAGE_RATE = 20
        self.message_rate = MESSAGE_RATE
        self.is_active = False
        self.terminate = False
        self.min_msg = 5
        self.send_count = 0
        self.lx = 0.0
        self.ly = 0.0
        self.rx = 0.0
        self.ry = 0.0
        self.dpadx = 0
        self.dpady = 0
        self.the_deque = deque()
        self.the_command = None
        if self.publish:
            self.pub = Publisher(8830)
        threading.Thread.__init__(self)

    def push_L1(self):
        self.the_deque.append(Commands.L1)

    def push_R1(self):
        self.the_deque.append(Commands.R1)

    def push_x(self):
        self.the_deque.append(Commands.X)

    def push_circle(self):
        self.the_deque.append(Commands.CIRCLE)

    def push_triange(self):
        self.the_deque.append(Commands.TRIANGLE)

    def set_velocity(self, x, y):
        self.lx = x
        self.ly = y

    def set_yaw(self, yaw):
        with open('/tmp/log.txt', 'a') as f:
            f.write("Yaw %s\n" % yaw)
        self.rx = yaw

    def set_pitch(self, pitch):
        self.ry = pitch

    def adjust_height(self, value):
        self.dpady = value
        self.the_deque.append(Commands.DPADY)

    def adjust_roll(self, value):
        self.dpadx = value
        self.the_deque.append(Commands.DPADX)

    def stop(self):
        self.terminate = True

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def run(self):
        while not self.terminate:

            if len(self.the_deque) and (not self.the_command or self.send_count > self.min_msg):
                self.the_command = self.the_deque.popleft()
                if self.write_log:
                    with open('/tmp/log.txt', 'a') as f:
                        f.write("Got Event %s\n" % self.the_command)
                self.send_count = 0

            if self.the_command:
                msg = {}
                msg["lx"] = self.lx
                msg["ly"] = self.ly
                msg["rx"] = self.rx
                msg["ry"] = self.ry
                msg["x"] = 1 if self.the_command == Commands.X else 0
                msg["square"] = 1 if self.the_command == Commands.SQUARE else 0
                msg["circle"] = 1 if self.the_command == Commands.CIRCLE else 0
                msg["triangle"] = 1 if self.the_command == Commands.TRIANGLE else 0
                msg["dpadx"] = self.dpadx if self.the_command == Commands.DPADX else 0
                msg["dpady"] = self.dpady if self.the_command == Commands.DPADY else 0
                msg["L1"] = 1 if self.the_command == Commands.L1 else 0
                msg["R1"] = 1 if self.the_command == Commands.R1 else 0
                msg["L2"] = 0
                msg["R2"] = 0
                msg["message_rate"] = self.message_rate
                if self.write_log:
                    with open('/tmp/log.txt', 'a') as f:
                        f.write("%s\n" % msg)
                if self.publish:
                    self.pub.send(msg)
                self.send_count += 1
                if self.the_command == Commands.TRIANGLE:
                    continue
                if self.send_count > self.min_msg:
                    if self.the_command == Commands.NONE and not self.is_active:
                        self.the_command = None
                    else:
                        self.the_command = Commands.NONE
            else:
                if self.is_active:
                    self.the_command = Commands.NONE

            time.sleep(1 / self.message_rate)

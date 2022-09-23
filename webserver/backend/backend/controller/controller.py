import json
import time
from joystick_sim.joystick import Joystick


class Controller:

    def __init__(self):
        self.joystick = Joystick()
        self.joystick.start()
        self.params = {}
        self.params['pupper'] = {}
        self.params['dance'] = {}
        self.params['walk'] = {}
        self.params['jump'] = {}
        self._setDefaults(self.params['dance'])
        self._setDefaults(self.params['walk'])
        self.dpadx = 0.0
        self.dpady = 0.0

    def _setDefaults(self, params):
        params['yaw'] = 0.
        params['pitch'] = 0.
        params['roll'] = 0.
        params['height'] = 0.
        params['vel_x'] = 0
        params['vel_y'] = 0

    def setParams(self, gait, command, param):
        if command == 'status':
            if gait == 'pupper' and param == 'start':
                self.joystick.activate()
            if gait == 'pupper' and param == 'stop':
                self.joystick.deactivate()
            if gait == 'pupper' and param == 'toggle':
                self.joystick.push_L1()
            if gait == 'pupper' and param == 'shutdown':
                self.joystick.push_triange()
            if gait == 'walk' and param == 'toggle':
                self.joystick.push_R1()
            if gait == 'dance' and param == 'toggle':
                self.joystick.push_circle()
            if gait == 'dance' and param == 'rollplus':
                self.joystick.adjust_roll(1)
            if gait == 'dance' and param == 'rollminus':
                self.joystick.adjust_roll(-1)
            if gait == 'dance' and param == 'heightplus':
                self.joystick.adjust_height(1)
            if gait == 'dance' and param == 'heightminus':
                self.joystick.adjust_height(-1)
            if gait == 'jump' and param == 'jump':
                self.joystick.push_x()
                time.sleep(.4)
                self.joystick.push_x()
                time.sleep(.4)
                self.joystick.push_x()
            return
        self.params[gait][command] = float(param)
        if gait == 'walk':
            self.joystick.set_velocity(self.params[gait]['vel_x']/100,
                                       self.params[gait]['vel_y']/100)
        if gait == 'dance':
            if command == 'yaw':
                self.joystick.set_yaw(self.params[gait]['yaw']/100)
            if command == 'pitch':
                self.joystick.set_pitch(self.params[gait]['pitch']/100)
            if param == 'rollplus':
                self.joystick.adjust_roll(1)
            if param == 'rollminus':
                self.joystick.adjust_roll(-1)
            if param == 'heightplus':
                self.joystick.adjust_height(1)
            if param == 'heightminus':
                self.joystick.adjust_height(-1)
        return

    def getParams(self, gait, command, param):
        return json.dumps(self.params[gait])

    def getMsg(self):
        return self.msg

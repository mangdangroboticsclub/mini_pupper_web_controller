import time
from mini_pupper import CONF

if CONF.mini_pupper.environment == 'simulator':
    from backend.controller.simulator.hardware_interface import Servo


def main():
    if CONF.mini_pupper.environment == 'simulator':
        servo = Servo(isServer=True)
        while True:
            servo.get_servo_positions()
            time.sleep(1.)


if __name__ == "__main__":
    main()

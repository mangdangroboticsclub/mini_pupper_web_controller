#!/bin/bash

sudo rm -f /etc/supervisor/conf.d/run_webcontroller.conf
sudo rm -f /etc/supervisor/conf.d/run_webcontroller.sh
sudo rm -f /etc/supervisor/conf.d/run_robot.conf
sudo rm -f /etc/supervisor/conf.d/run_robot.sh
sudo systemctl enable joystick
sudo systemctl enable robot

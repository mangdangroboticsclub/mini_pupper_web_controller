# mini_pupper_web_controller

Replaces PS4 joystick by a web GUI that can be run on a smartphone

## Installation

The following describes the steps for an installation from scratch that installs all components required.
It also install a pygame based keyborad controller that you might find usefull in certain circumstances

- flash Ubuntu 22.04.img to SD card
- on mini pupper open a terminal:
- git clone https://github.com/mangdangroboticsclub/mini_pupper_bsp.git
- git clone https://github.com/mangdangroboticsclub/StanfordQuadruped.git
- git clone https://github.com/mangdangroboticsclub/mini_pupper_web_controller.git

- ./mini_pupper_bsp/install.sh; sudo reboot
- ./mini_pupper_bsp/update_kernel_modules.sh; sudo reboot
- cd StanfordQuadruped
- ./install.sh
- ./configure_network.sh &lt;my SSID&gt; &lt;my wifi password&gt;
- cd ~
- ./mini_pupper_web_controller/webserver/install.sh
- sudo apt-get install -y libsdl2-2.0-0
- sudo pip3 install pygame
- git clone https://github.com/stanfordroboticsclub/PupperKeyboardController.git
- sudo reboot

## Run
Point a web browser to http://x.x.x.x:8080 where x.x.x.x is the IP address of your mini_pupper

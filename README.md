# Summary

[![Youtube video](https://img.youtube.com/vi/ubgNV3DJ6JE/0.jpg)](https://youtu.be/ubgNV3DJ6JE)   ![smartphone](imgs/webController.gif)

You can try this application on Mini Pupper and Mini Pupper2. 

Web GUI that can be run on mobile devices, such as smartphones, Pad, and Notebook can run a browser.


## Installation

Step1: install [mini_pupper_bsp](https://github.com/mangdangroboticsclub/mini_pupper_bsp.git)  repo and run the test script to ensure your installation works as expected. Please make sure you install the right branch for your Mini Pupper or Mini Pupper 2.

Step2: install [mini_pupper](https://github.com/mangdangroboticsclub/StanfordQuadruped)  repo.


After the up installation, please follow the below steps.

```
cd ~
git clone https://github.com/mangdangroboticsclub/mini_pupper_web_controller.git
./mini_pupper_web_controller/webserver/install.sh
```

## Run
Point a web browser to http://x.x.x.x:8080 where x.x.x.x is the IP address of your mini_pupper


## Keyboard controller
If you want to use a keyboard to control Mini Pupper, please try the below steps. Be certain to tell ssh to allow X11 forwarding before you run it.

```bash
ssh -o ForwardX11=yes ubuntu@<Your Mini Pupper IP address>
```

```
cd ~
sudo apt-get install -y libsdl2-2.0-0
sudo pip3 install pygame
git clone https://github.com/mangdangroboticsclub/PupperKeyboardController
python keyboard_joystick.py
```

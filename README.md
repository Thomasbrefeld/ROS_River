# ROS_River
ROS River is an application that will display information about the Robot Operating System (ROS) to the user via a LED display. This application displays current tasks, issues, and other debugging information desired by the user. ROS River has uses in autonomous vehicle development where persons outside the vehicle can see and understand the car's current task. The application runs on a Raspberry PI B and is connected via ethernet to the main ROS core. The Raspberry PI subscribes to certain nodes within the main ROS core and displays the information to the LED Display.

## Setup
The only setup required is to set the IP of the ROS Core Computer within the src/remote-master.sh file. Currently this requires the user to SSH into the Raspberry PI and update the file.

## Usage
ROS River when setup correctly takes no interaction and on start-up, ROS River starts in "Auto" mode.
### Auto Mode
When in this mode ROS River will automatically detect what the vehicle is doing at that time.  This mode requires no interaction from the user. This mode will display error and warning messages of level 4 or high from ROSout. 
### Manual Mode
When the user publishes to “display/auto” False the mode is changed to “Manual”. ROS River displays the information provided in “display/text” and “display/status”. ROS River will display this information until new information is published to the topics. 

## ROS Subsribers
### display/auto
Takes a bool, and is used to switch the ROS River mode from/to "Auto Mode". Topic is False the Program will operate in manual mode and will require data to be published to "display/text" and "display/status".
### display/text
Takes a string, when "display/auto" is set to False, the program will display the text verbatim until the topic is updated.
### display/status
Take an Int8, when "display/auto" is set to False, the program will display the integer verbatim until the topic is updated.
### Other topics subscribed to:
* rosout
* joy
* /vehicle/dbw_enabled

## Files being run on ACTor
* src/remote-master.sh
* run/startUp.py
* launch/main.launch
* src/main1.py
* src/show1.py

## Power
Required power is 12v at max 3 amps.

## Parts:
* Raspberry PI 3B or better
* WS2812B LED Display (Display can be any size)
* DC Voltage Regulator 12v to 5v

## Links
* GitHub Page: https://github.com/Thomasbrefeld/ROS_River
* Demo: https://youtu.be/Xvg98JJ5lbI

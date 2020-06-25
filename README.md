# RoboCar

    ### In this Tutorial you will  program a robot to autonomously navigate through a maze. 

# Table of contents
1. [Task Description](#introduction)
2. [Specifikations](#paragraph1)
    1. [Image to the Maze](#subparagraph1)
    2. [Layout of the Maze](#subparagraph1)
    3. [Road Signd](#subparagraph1)
    4. [Program Invocation, time Measurment](#subparagraph1)
    5. [Penalties](#subparagraph1)
3. [Quickstart Guidelines](#paragraph2)
    1. [Working with Raspberry pi](#subparagraph1)
    2. [ Virtual maschine for 3pi and maze processing development ](#subparagraph1)
    3. [ Working with the 3pi Roboter](#subparagraph1)
    4. [Sample maze generator](#subparagraph1)
    5. [Transmission Control Protocol/internet Protocol (TCP/IP)](#subparagraph1)
    6. [Universal Asynchronous Receiver-Transmitter(UART)](#subparagraph1)
3. [off-the-Shelf Modules](#paragraph2)
    1. [Image to Mazr Graph Module](#subparagraph1)
    2. [ Robot Control Module ](#subparagraph1)
    3. [ Road Sign Detection Module](#subparagraph1)

1. Task Description
The Task is to program a 3pi Roboter to drive through a maze from a starting point to a finish point. The maze is represented by black lines and 3pi Robot is never allowed to leave these lines. During the race you are not allowed to interact wth the 3pi Robot, i.e.,it must be able to autonomously navigate the maze. The image of the maze, that can be used as a map to plan a route through the maze. Befor you can sart driving, the maze plan must be processed into a representation your robot can make use of. For this , you must use the Raspberry Pi that sits on top of the 3pi Robot.

In the race, The robot will need to navigate through the maze. To increase the difficulty, road signs wil be added to the maze that need to be detected and reacted upon. For exemple, the robot shall come to a complete stop in front of a stop sign befor it continues.

2. specifiCations
2.1 Image to the Maze
An image of the maze is shown in Figure. the image is a png file that consists a black  pinels to represent the lines on which the 3pi Robot must drive. Other pixels will be white.Back lines have a thickness of 3 pixels. Note that there can be gray pixels at the edge of the black lines crated by anti-aliasing. The starting point is illustrated by a circle filled in red and the finish point by circlefilled in green.

2.2. Layout of the Maze


# BioDesic-Pattern-Fitter

### Introduction

This is the first program I wrote whilst teaching myself python for a short while, before I'd learnt about OOP, OOD, TDD and all the things you're supposed to do to write good code. It came from a desire to learn software development and solve a real world problem related to a clothing design side project of mine known as BioDesic.

The concept for the clothing came from studying Interior and Architectural design back in 2003-05. I wanted to apply the design principles I'd formulated during this time, as well as technology and physics to create something new. Clothing that was less about fashion and trends and more about craftsmanship, contrasting organic forms against geodesic structures, and creating clothes that I wanted to wear.

The problem that this created was that making clothes out of triangles made fitting them perfectly was very laborious. What I needed was a program to automate altering a 3D model of a garment to enable quicker more accurate pattern design.
Wanting to create wearable, architectural clothing using tessellated forms it became apparent that fitting these garments to the curves of the human body required much more precision than traditional clothing construction. This program was born out of a desire to embrace technology and push the boundaries of traditional clothing and create an aesthetic created by the solution to this problem.

The program is by no means finished and there are a few issues with crashing, e.g. if you try to cut part way through geometry and also when using the align command. But this is a work in progress.

### Instructions

The program runs in python 2.7

You also need Pygame. To install it run the command:

**pip install pygame**

### To run the program:

From the command shell (Bash Unix or Mac) enter **python Biodesic\ Fit_Version_1** or type **python** hit enter and then type **exec(open("Biodesic Fit_Version_1.py").read())** from inside the python shell

For Windows you can open the code using the IDLE or double click the .py file and it will run automatically.

Once the program's running you can click two points either side of the part of the model you want to cut through and it will display the measurement. You can then type in the new measurement and hit enter repeatedly until it acheives thee desired result.

![Image of GUI](https://github.com/SimonTanner/BioDesic-Pattern-Fitter/blob/master/images/BioDesic-Pattern-Fitter.jpg)

### Other commands are as follows:

E - Shows or hides polygon edges

CTRL + E - Displays the edges of the pattern before you made any changes allowing you to compare the two

Left & Right Arrow keys rotate the model

F - Front view

L - Left view

R - Right view

B - Back view

C - Clears the cut points

A - Aligns the cutting plane to the average perpendicular plane to the local geometry

SHIFT - Whilst clicking a second point means the line will be drawn along the x or y axis.

V - Displays the number of the face

N - Toggles the display of the average normal at each vertex

ESC - Brings up the quit menu

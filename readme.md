A suite of computer vision utilities
====================================

About
-----

A package of useful utilities for general computer vision tasks written in Python. 

Dependencies
------------

* OpenCV 2.3.1 or greater with Python bindings
* Numpy
* Scipy
* Matplotlib
* FFMpeg

Camera
------

Something something something...

Overlay
-------

About:
Code for overlaying a model on a video feed given pose parameters and a camera 
calibration file.

Usage:
        $python overlay --video SOMEFILE.avi --pose POSES.csv --calib CALIB.xml [--stereo]

* The camera calibration file should be in the OpenCV XML format.
* The poses should be one for each frame on a new line in the format tx,ty,tz,r1,r2,r3 where the rotations are obtained from Rodrigues rotation forumla. Units are mm and radians.
* The stereo flag is optional. This is only used for video splitting and does not make any assumptions about the calibration parameters.

PosePlotter
-----------

A utility for plotting the pose of a tracking algorithm and a ground truth in 3D.

Recolor
-------

Generating interesting colorspaces from an RGB image.

Licence
-------

Copyright (C) 2013  Max Allan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses](http://www.gnu.org/licenses).
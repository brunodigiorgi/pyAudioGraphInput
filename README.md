Description
-----------

Control input nodes for pyAudioGraph (https://github.com/brunodigiorgi/pyAudioGraph)

Requirements
------------

* numpy
* LeapMotionSDK  (only required for LeapMotionNode)

LeapMotionSDK for Python3
-------------------------

Follow the instructions at https://support.leapmotion.com/hc/en-us/articles/223784048

1. install swig-2.0.9 (I used 3.0.3), downloadable at https://sourceforge.net/projects/swig/files/swig/
2. download LeapMotion SDK. I used 2.3.1 from https://developer.leapmotion.com/sdk/v2
3. copy Leap.h, LeapMath.h, Leap.i, and libLeap.dylib in one folder
4. run

	swig -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i

5. compile (this is osx specific, replace [VERSION] with your Python3 version. Tested with 3.5):

	clang++ -arch i386 -arch x86_64 -I/Library/Frameworks/Python.framework/Versions/[VERSION]/include/python[VERSION]m LeapPython.cpp libLeap.dylib /Library/Frameworks/Python.framework/Versions/[VERSION]/lib/libpython[VERSION].dylib -shared -o LeapPython.so

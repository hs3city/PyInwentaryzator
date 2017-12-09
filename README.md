PyInwentaryzator
======

A simple tool in development intended to be used during stocktaking of the hardware available at Hackerspace Trójmiasto.


How to use
------

In order to use the application:
1. Download the app
2. Install required libraries
3. Open `PyInventaryzator.py` file in a text editor, find line `CAMERA = <something>`. This variable controls which camera is to be used. If you have only one, this should be set to `0` otherwise experiment to find your camera. `<something>` variables value must be a positive integer, 
4. Start the application `python PyInventaryzator.py`
5. Read instructions presented in the terminal.
 
Projects technical requirements
------

1. Data should be preserved in csv format.
2. Each photo should have an unique pseudo-random file name.
3. The photos pseudo-random name should be used to reference the photo in the CSV database.
4. Keep It Simple you Stupid.

Requirements
------
1. Ubuntu 16.04.2 LTS
2. CPython 2.7.12
3. python-opencv 2.4.9.1 : `sudo apt-get install python-opencv`

Project stories
------

### Story: Webcam support
**Given** the user has at least one webcam.

**When** the user start the program.

**Then** the user should be able to select webcam to be used.

### Story: Program start
**Given** the user has started the application.

**When** the user select the webcam to be used.

**Then** the user should be presented with the stock add screen.

### Story: Initial stock addition
**Given** the user is on the stock add screen and there is no stock in the database.

**When** the user finish providing the application with the required data and order the application to save the data.

**Then** an initial database containing the provided data should be created.

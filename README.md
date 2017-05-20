PyInwentaryzator
======

A simple tool in development intended to be used during stocktaking of the hardware available at Hackerspace Trójmiasto.

Project stories
------

### Story: Webcam support
Given the user has at least one webcam.
When the user start the program.
Then the user should be able to select webcam to be used.

### Story: Program start
Given the user has started the application.
When the user select the webcam to be used.
Then the user should be presented with the stock add screen.

### Story: Initial stock addition
Given the user is on the stock add screen and there is no stock in the database.
When the user finish providing the application with the required data and order the application to save the data.
Then an initial database containing the provided data should be created.

Projects technical requirements
------

1. Data should be preserved in csv format.
2. Each photo should have an unique pseudo-random file name.
3. The photos pseudo-random name should be used to reference the photo in the CSV database.
4. Keep It Simple you Stupid.

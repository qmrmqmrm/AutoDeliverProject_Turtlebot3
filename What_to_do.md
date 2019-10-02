# What to do

## Part 1. - Code

### 1. Remove redundant

- S.O : Sort out Obsolete nodes and files
  - Necessary node : 1. Aruco marker detecting node, 2. Robot controlling node, 3. Program starting node, 4. Box lifting node



### 2. Make configure

- M.C : Make Configure.py

  - Try not to put coordinates in code. Use configure file.

  - Step 1. Make configure.py in workspace.

  - Step 2. Make a dictionary which stands for goal pose in configure.py.

    Ex) poses = {"home" : (1,2,3), "destination 1" : (3,6,1) ....etc...}

  - Step 3. In robot controlling node, import configure.py and use coordinate data

  - Step 4. Copy configure.py as configure_example.py

  - Step 5. Add configure.py to .gitignore so that the file cannot be committed on git.



### 3. Refactor

- R.M : Refactor main()
  - Bring out mode section from all functions and put them in main().
  - Make sure the algorithm is exposed to main().
  - Make more bases up to 10
  - Try to minimize delay between each function



### 4. Additional function

- 1. If there are more than two boxes which have same destination, (in this case, same marker id) do the delivering function repetitive
  2. If a box is in the way, not in the base, and the robot is not carrying a box, try to pickup the box and deliver to proper destination
  3. Try to face marker on the center of the robot so that the robot can pickup the box easily.



## Part 2. -Hardware Setting

### 1. Get a new motor - for the lift

- XL430-W250-T
  - Either functionally and mechanically similar to XM430(motors for wheels) series.
- Motor cable
  - bought Cable-X3P 180mm.
- Turtlebot Plate
  - For more layer.



### 2. Visit Hardware Store

- Screws - 2.5 * 12mm
  - Get screws for fastening new motor to the robot plate.



### 3. Think about robot cover design

- Make it cool
  - For the robot festival, choose cover design.



# Schedule

### Oct. 2 ~ Oct. 8

- Finish S.O & M.C
- Finish Hardware Setting



### Oct. 9 ~ Oct. 20

- Try to finish refactor main()



### Oct. 21 ~ Nov.20

- Try to finish additional function
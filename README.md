### Summary
**Short breakdown of the code**
- test_camera controls camera to take RGB data (Colour intrinsics...), DEPTH data ... and stores these data into a data folder
- test_cv retrieves data from data folder, determine the x, y, z coordinates of stains based on the data test_camera had collected
### Introduction

**Functionality of realsense camera that we are using**
- Capture RGB or normal coloured images
- Capture depth (distance between the camera and the object in sight)


## Modes
**Mode 1** - perfectly clean toilet

**Mode 2** - toilet before cleaning

**Mode 3** - toilet after cleaning

- Each mode is a state at which the camera can go into
- if the camera is at mode 1, it has to record data of the perfectly clean toilet
- It will record two different data files.
1. RGB_photo.jpeg
2. DEPTH_photo.png

- RGB photo records the color data
- Depth photo records the depth data

**files.py**
- class Files
- needs a home folder that contains a data.json file to initialise
- self.datafilepath outputs all the file path 
**test_camera.py**
- class Camera()
- Set the mode here, self.recording(mode=int..)
- You can press s to take a video, press t to toggle between RGB and depth, and q to quit. Once q is pressed, the camera will record the data from the last frame and write the two files.
- After the user set the images and depth data for these 3 modes, there should be 6 data files in the data folder.
- self.Datatreatment returns all the colour and depth data from the frame
- self.storingoffsets_and_focal_length stores horizontal, vertical offsets and focal length to a data.json file
- self.getframedata expresses the depth and color of the frame in terms of np array
- self.align resolution aligns the resolution (pixel width and length) of the depth and rgb camera image.
- when user presses quit. test camera will update a data.json file
- data.json would possess the horizontal, vertical offsets and focal length of the camera. Such values would only change when switching to a different type of realsense camera. 

After running test camera. the following folders...

**DATA FOLDER** should have ...
- Photo_depth_perfect/_before/_after .png 
- photo_perfect/_before/_after .jpeg

**Robot_computer_vision** should have...
- data.json


**test_cv.py**
- class Analyse()
- you would only need the file path of the image to innitialise the class
- if depth file is not specified, the program would take all the depth value as 0. 
- It will draw a contour around the stain spots
- self.contour_ellipse will express the contours as an ellipse and store the centre and the axes of the ellipse in points_array
- self.find_elipse_coordinate_and_depth returns the contours, the points array and sum_area of the stain
- self.normalized vector returns vectors, which is how the robot arm will tilt to aim at the stain spot. It gets the vector perpendicular to the centre of the stain in the toilet bowl.
- self.visualizevectors allows users to visualise all the vectors
- self.find_ellipsis_coordinates_and_depth has a variable blur_level. Set it according to the level of precision of contours generated you want. Blur level must be a tuple consisting of two odd value and cannot be set as (1,1).


**main.py**
- class Comparison()
- Comparison class requires the repository file path to initialise. Input in "../usr/.../robot_computer_vision" as the directory file path.
- self.return_all_data_path has a argument called default. If default is true, the program will return the default toilet images and analyse them. This is used to test various functions of the stain detection program.
- However if default is set to False, the program will search through the data folder for data and analyse them. The program will crash if all seven files are not included beforehand.
- The program will compare the area of stains between before and after, to find out how many percentage of stains had been cleaned. 
- It was also compare the area of stains between perfect and after to find out how many percentage of stains needs to be removed. 



**Test Camera functions**

![depth_rgb_camera](https://github.com/BluePjCookies/robot_computor_vision/blob/main/screen_shot/Screen%20Recording%202024-01-11%20at%201.11.46%20PM.mov)

**Identifying stains**
- red represents contours
- green represent ellipse
- blue dots are coordinates that would be taken down in the points_array
![image](https://github.com/17688959374/robot_computor_vision/assets/128206550/0208efd7-6b04-4539-b47d-8d090d90770d)

**What is blur_level**
- Images are first treated with a Gaussian blur, before drawing the contours on it. Setting the blur level would impact the precision of the contours drawn.
- Image below depicts the difference between the contours drawn when blur level is set to (3,3) and (5,5) respectfully. 
- User can set blur level in self.find_ellipsis_coordinates_and_depth
![blurlevel](https://github.com/BluePjCookies/robot_computor_vision/blob/main/screen_shot/image.png)

**3D view of Normalized-vectors**
![video](https://github.com/BluePjCookies/robot_computer_vision/blob/main/screen_shot/3dvector.mov)

### What does this updated code eliminate?

- The need to connect to a realsense2 camera for data collection while running test_cv. This allows one to only retrieve data from test_camera py script. Allowing for modularity.
- Heavy debugging, Code has been broken down to simpler and readable chunks, with added comments to enhance readability during debugging
- Repetition in code. Usage of functions in both test_cv and test_camera, reduces the number of lines of code needed, allowing for simplicity and reusability in other areas



   

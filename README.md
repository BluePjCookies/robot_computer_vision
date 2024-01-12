### Allow for Modularity
**Short breakdown of the code**
- test_camera controls camera to take RGB data (Colour intrinsics...), DEPTH data ... and stores these data into a data folder
- test_cv retrieves data from data folder, determine the x, y, z coordinates of stains based on the data test_camera had collected
### Changes

**REAL SENSE FOLDER**
- Data.json file to host offsets and focal length
- Photo_depth_perfect/_before/_after .png
- photo_perfect/_before/_after .jpeg

**main.py**
- class Comparison requires the repository file path to initialise. Input in "../usr/.../robot_computer_vision" as the repository file path. 
- The program will look through the files in the data folder. It will retrieve the file path data after all 3 modes had been collected. You can set whether you want the file path to be default or not if you dont have an actual photo of a toilet.
- The program will compare the area of stains between before and after, to find out how many percentage of stains had been cleaned. 
- It was also compare the area of stains between perfect and after to find out how many percentage of stains needs to be removed. 


**test_camera.py**
- class Camera()
- There are 3 modes. Mode 1 will request the user to take a photo of the perfectly clean toilet, 2 for the toilet before cleaning and 3 for the toilet after cleaning. Select mode in c.recording(mode=int..)
- After the user set the images and depth data for these 3 modes, there should be 6 data files in the data folder.
- The 6 files are 3 images and depth, consisting of the perfectly clean toilet, toilet before cleaning, and toilet after cleaning
- Stores all file path in self.storingfilepath
- self.recording records, added functionality - press t to toggle between RGB and Colourdepth
- self.Datatreatment returns aligned and colour data from frame
- self.storingoffsets_and_focal_length stores horizontal, vertical offsets and focal length to a data.json file
- self.getframedata expresses the depth and color of the frame in terms of np array
- self.align resolution returns the aligned frame, aligned_colour_frame and aligned_depth_frame. It aligns the resolution of the depth and rgb camera.

**test_cv.py**
- class Analyse()
- No changes made to the math
- self.find_elipse_coordinate_and_depth displays contours, the points array and sum_area
- self.normalized vector returns vectors, which is how the robot arm will tilt to aim at the stain spot. It gets the vector perpendicular to the centre of the stain in the toilet bowl.
- self.visualizevectors allows users to visualise all the vectors
- self.retrieve offsets.. retrieve data from data.json file
- self.find_ellipsis_coordinates_and_depth has a variable blur_level. Set it according to the level of precision of contours generated you want. Blur level must be a tuple consisting of two odd value and cannot be set as (1,1). Eg. (3,3)...

**Test Camera functions**
- When t is pressed, the stream can toggle to an RGB mode or a Color_depth mode.
- When q is pressed, the data from the photo of the last frame will be stored in photo_depth.png and photo.jpg. The these can be used in test_cv to analyse the vectors etc...
![depth_rgb_camera](https://github.com/BluePjCookies/robot_computor_vision/blob/main/screen_shot/Screen%20Recording%202024-01-11%20at%201.11.46%20PM.mov)

**Identifying stains**
- red represents contours
- green represent ellipse
- blue dots are coordinates that would be taken down in the points_array. They are points on the ellipse that are of the furthest distance from one another, known as axes..
![image](https://github.com/17688959374/robot_computor_vision/assets/128206550/0208efd7-6b04-4539-b47d-8d090d90770d)

**What is blur_level**
- Image below depicts the difference between the contours drawn when blur level is set to (3,3) and (5,5) respectfully. 
- User can set blur level in self.find_ellipsis_coordinates_and_depth
![blurlevel](https://github.com/BluePjCookies/robot_computor_vision/blob/main/screen_shot/image.png)

**3D view of Normalized-vectors**
![video](https://github.com/BluePjCookies/robot_computer_vision/blob/main/screen_shot/3dvector.mov)

### What does this updated code eliminate?

- The need to connect to a realsense2 camera for data collection while running test_cv. This allows one to only retrieve data from test_camera py script. Allowing for modularity.
- Heavy debugging, Code has been broken down to simpler and readable chunks, with added comments to enhance readability during debugging
- Repetition in code. Usage of functions in both test_cv and test_camera, reduces the number of lines of code needed, allowing for simplicity and reusability in other areas



   

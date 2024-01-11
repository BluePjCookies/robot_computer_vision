### Allow for Modularity
**Short breakdown of the code**
- test_camera controls camera to take RGB data (Colour intrinsics...), DEPTH data ... and stores these data into a RealSense folder
- test_cv retrieves data from RealSense folder, determine the x, y, z coordinates of stains based on the data test_camera had collected
### Changes
**REAL SENSE FOLDER**
- Data.json file to host offsets and focal length
- Photo.jpeg and Photo_depth.png for testing purposes

**test_camera.py**
- class Camera()
- Stores all file path in self.storingfilepath
- self.recording records, added functionality - press t to toggle between RGB and Colourdepth
- self.Datatreatment returns aligned and colour data from frame
- self.storingoffsets_and_focal_length stores horizontal, vertical offsets and focal length to a data.json file
- self.getframedata expresses the depth and color of the frame in terms of np array
- self.align resolution returns the aligned frame, aligned_colour_frame and aligned_depth_frame, (I replaced depthx and depthxy with aligned_depth_frame

**test_cv.py**
- class Analyse()
- No changes made to the math
- self.find_elipse_coordinate_and_depth displays contours, the points array and sum_area
- self.normalized vector returns vectors instead of posture
- self.visualizevectors allows users to visualise all the vectors
- self.retrieve offsets.. retrieve data from data.json file
Changes were only made to the code. The outputs for my code is the same as yours

**3D view of Normalized-vectors**
![image](https://github.com/17688959374/robot_computor_vision/assets/128206550/09c20ca3-9fe5-4b59-907e-d0e39f632ce1)

**Identifying stains**
- red represents contours
- green represent ellipse
- blue dots are coordinates that would be taken down in the points_array. They are points on the ellipse that are of the furthest distance from one another, known as axes..
![image](https://github.com/17688959374/robot_computor_vision/assets/128206550/0208efd7-6b04-4539-b47d-8d090d90770d)

### What does this updated code eliminate?

- The need to connect to a realsense2 camera for data collection while running test_cv. This allows one to only retrieve data from test_camera py script. Allowing for modularity.
- Heavy debugging, Code has been broken down to simpler and readable chunks, with added comments to enhance readability during debugging
- Repetition in code. Usage of functions in both test_cv and test_camera, reduces the number of lines of code needed, allowing for simplicity and reusability in other areas



   

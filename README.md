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

# Files.py

```python

class Files:
   def __init__(self, home_folder):
      ... #define home_folder and path to data.json files
   def datafilepath(self, mode, data_folder):
      return video_path, video_depthcolor_path, video_depth16_path, photo_path, photo_depth_path, self.json_file_path

```

- class Files
- needs a home folder that contains a data.json file to initialise
- self.datafilepath outputs all the file path 

# Test_camera.py

```python
class Camera():
   def __init__(self, width=640, height=480, fps=30, ColorAndDepth = False, home_folder = None, data_folder = None):
      ... #Initialise camera and file paths.

   def getframe(self):
      return frame

   def getframedata(self, frame):
      return depth_image, color_image #Return as an numpy array

   def alignresolution(self, frame):
      return aligned_frame, aligned_depth_frame, aligned_color_frame

   def storing_offsets_and_focal_length(self, frame, mode):
         ... #stores camera information in data.json

   def Datatreatment(self, frame):
      return color_image, aligned_depth_image, aligned_color_image, colorizer_depth

   def release(self):
      ... #stop the camera

   def initialise_recording_function(self, mode):
      return wr, wr_colordepth, wr_depth

   def handling_exception(self, mode):
      ...

   def recording(self, mode:int):
      ...#Opens and runs the camera
      return frame

```

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
> [!NOTE]
> After running test camera. the following folders...

**DATA FOLDER** should have ...
- Photo_depth_perfect/_before/_after .png 
- photo_perfect/_before/_after .jpeg

**Robot_computer_vision** should have...
- data.json

**Test Camera functions**

![depth_rgb_camera](https://github.com/BluePjCookies/robot_computor_vision/blob/main/screen_shot/Screen%20Recording%202024-01-11%20at%201.11.46%20PM.mov)


# Test_cv.py

```python
class Analyse:
    def __init__(self, width=640, height=480, fps=30, img = None, depth_map = None, show_img=False, home_folder=None, perfect_img = None):
      ... #initialise file path. if depth map set to None. Default depth are all set to 0

   def display(self, image):
      #display image

   def enhance_contrast(self, img, blur_level:tuple):
      ... #image processing and remove noise from image
      return thresh

   def contour_ellipse(self, cnt):
      ... #get data from cnt in contours
      return area, center, axes, angle

   def find_ellipse_coordinates_and_depth(self, blur_level = (3,3)):
      ... #search for contours and fit it into an Ellipse
      ... #retrieve points from ellipse (centre and axes) and put it in an array (points_array)
      return contours, points_array, sum_area

   def expressing_vectors(self, vectors, index):
      ... #Express vectors in terms of movement in the x,y and z coordinate
      return x, y, z

   def normalized_vectors(self, points_array, depth_map):
      ... #get the normal vector perpendicular to the centre of the stain in the toilet bowl
      return vectors

   def visualize_all_vectors(self, vectors, points_array, depth_map):
      ... #use matplotlib, 3d plot to plot vectors

   def visualize_depth_map(self, depth_map):
      ... #use matplotlib, 3d plot to plot depth

   def retrieve_offsets_and_focal_length(self):
      ... #retrieve camera systems's data from data.json file
      return data["ppx"], data["ppy"], data["fx"], data["fy"]

   def find_realxyz_coordinate(self, points_array, depth_map):
      #determine the x, y, z coordinate of the stain based on the offsets and focal length data
      return points_array
```
- class Analyse()
- you would only need the file path of the image to innitialise the class
- if depth file is not specified, the program would take all the depth value as 0. 
- It will draw a contour around the stain spots
- self.contour_ellipse will express the contours as an ellipse and store the centre and the axes of the ellipse in points_array
- self.find_elipse_coordinate_and_depth returns the contours, the points array and sum_area of the stain
- self.normalized vector returns vectors, which is how the robot arm will tilt to aim at the stain spot. It gets the vector perpendicular to the centre of the stain in the toilet bowl.
- self.visualizevectors allows users to visualise all the vectors
- self.find_ellipsis_coordinates_and_depth has a variable blur_level. Set it according to the level of precision of contours generated you want. Blur level must be a tuple consisting of two odd value and cannot be set as (1,1).
- addition of visualise depth image, allow you to get a 3d view of the frame
- perfect_img variables allows one to subtract the current image with the perfect one. This however is optional and can be used if perfect image is available


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

**3D view of depth map**

![video](https://github.com/BluePjCookies/robot_computer_vision/blob/main/screen_shot/depth_map.mov)

**3D view of Normalized-vectors**
![video](https://github.com/BluePjCookies/robot_computer_vision/blob/main/screen_shot/3dvector.mov)


# Main.py

```python
class Comparison:
   def __init__(self, data_folder = None, has_depth=False, home_folder=None):
      ... #initialise file path. If data_folder contains depth, change it accordingly
      self.perfect = Analyse(...)
      self.before = Analyse(...)
      self.after = Analyse(...)
   def compare(self, show_img=True):
      ... #print out the results of the comparison
```


- class Comparison()
- Comparison class requires the repository file path to initialise. Input in "../usr/.../robot_computer_vision" as the directory file path.
- It will automatically source for specific files in data_folder, if has_depth is False, it will take depth to be 0
- The program will compare the area of stains between before and after, to find out how many percentage of stains had been cleaned. 
- It was also compare the area of stains between perfect and after to find out how many percentage of stains needs to be removed. 

```python
#Output for testing
ic| perfect_sum_area: 0
    before_sum_area: 5158.0
    after_sum_area: 2600.5
Stain removed from before to after: 49.583171772004654%
Percentage of stains to be removed to be perfect: 100.0%
```


### What does this updated code eliminate?

- The need to connect to a realsense2 camera for data collection while running test_cv. This allows one to only retrieve data from test_camera py script. Allowing for modularity.
- Heavy debugging, Code has been broken down to simpler and readable chunks, with added comments to enhance readability during debugging
- Repetition in code. Usage of functions in both test_cv and test_camera, reduces the number of lines of code needed, allowing for simplicity and reusability in other areas


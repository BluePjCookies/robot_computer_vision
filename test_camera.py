import pyrealsense2 as rs
import numpy as np
import cv2
import h5py
import json
from icecream import ic

class Camera():
    def __init__(self, width=640, height=480, fps=30, ColorAndDepth = False, data_folder = None):
        
        self.width = width
        self.height = height
        self.fps = fps
        self.isrecording = False
        self.ColorAndDepth = ColorAndDepth
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.data_folder = data_folder

        
        
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16,  fps)
        self.data_folder = data_folder
        
        # self.config.enable_stream(rs.stream.infrared, 1, self.width, self.height, rs.format.y8, fps)
        # self.config.enable_stream(rs.stream.infrared, 2, self.width, self.height, rs.format.y8, fps)
        self.pipeline.start(self.config)

        

    def getframe(self):
        # Get the frames from external realsense camera
        frame = self.pipeline.wait_for_frames()
        return frame

    def getframedata(self, frame):
        #Retrieves the Depth and color values from the frames and convert them to a np array
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return depth_image, color_image
    
    def alignresolution(self, frame):
        align_to = rs.stream.color                 
        align = rs.align(align_to)
        aligned_frame = align.process(frame)

        aligned_depth_frame = aligned_frame.get_depth_frame()      
        aligned_color_frame   = aligned_frame.get_color_frame()

        return aligned_frame, aligned_depth_frame, aligned_color_frame 
    
    def storing_offsets_and_focal_length(self, frame, mode):
        _, _, _, _, _, json_file_path = self.storingfilepath(mode)
        _, _, aligned_color_frame  = self.alignresolution(frame)

        #Retrieve the internal parameters of the coloured frame
        color_profile = aligned_color_frame.get_profile()
        cvsprofile = rs.video_stream_profile(color_profile)
        color_intrin = cvsprofile.get_intrinsics()
        color_intrin_part = (color_intrin.ppx, color_intrin.ppy, color_intrin.fx, color_intrin.fy)
        #ppx -  horizontal offset of that central point
        #fx - focal length which will affect the depth map...
        ppx, ppy, fx, fy = color_intrin_part
        
        data = {
            "ppx" : ppx,
            "ppy" : ppy,
            "fx" : fx,
            "fy" : fy
        }
        #Dumping data to a file
        with open(json_file_path, "w") as f:
            json.dump(data, f)
    
    def Datatreatment(self, frame):
        
        
        #Setting colours to different levels of depth
        colorizer = rs.colorizer()

        #Retrieves the Depth and color values from the frames and convert them to a np array
        depth_image, color_image = self.getframedata(frame)
        

        #Align the resolution of the depth and color of the image. 
        aligned_frame, aligned_depth_frame, aligned_color_frame = self.alignresolution(frame)

        #Setting colors to the aligned depth frame
        colorizer_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())

        #Retrieve the depth and color values from the aligned frame and convert it to an array
        aligned_depth_image, aligned_color_image = self.getframedata(aligned_frame)
        

        return color_image, aligned_depth_image, aligned_color_image, colorizer_depth
    
    def release(self):
        self.pipeline.stop()

    
    def storingfilepath(self, mode):

        classify_modes = {1:"_perfect", 2:"_before", 3:"_after"}
        #Stores the RGB video here
        video_path = self.data_folder + "/targetvideo_rgb.mp4"
        #Stores the Color&depth video here
        video_depthcolor_path = self.data_folder + "/targetvideo_depthcolor.mp4"
        #stores the video_depth data here
        video_depth16_path = self.data_folder + "/targetvideo_depth.h5"
        #stores the last frame of the video here
        photo_path = self.data_folder + f"/photo{classify_modes[mode]}.jpeg"
        #stores the depth_data from the last frame of the video here
        photo_depth_path = self.data_folder + f"/photo_depth{classify_modes[mode]}.png"
        #stores the x,y,z offsets here
        json_file_path = self.data_folder.split("robot_computer_vision")[0] + "robot_conputer_vision/data.json"

        return video_path, video_depthcolor_path, video_depth16_path, photo_path, photo_depth_path, json_file_path
    

    def initialise_recording_function(self, mode):

        video_path, video_depthcolor_path, video_depth16_path, _, _, _= self.storingfilepath(mode=mode)
        
        mp4 = cv2.VideoWriter_fourcc(*'mp4v') 

        #Initialising different recording functions. normal rgb, depth and color+depth
        wr = cv2.VideoWriter(video_path, mp4, self.fps, (self.width, self.height), isColor=True)
        wr_colordepth = cv2.VideoWriter(video_depthcolor_path, mp4, self.fps, (self.width, self.height), isColor=True)
        wr_depth = h5py.File(video_depth16_path, 'w')

        return wr, wr_colordepth, wr_depth
    def handling_exception(self, mode):
       #1 - Perfectly clean toilet, 2 - Dirty Toilet, 3 - Toilet after cleaning
        if isinstance(mode, int) is False:
            raise Exception("Input an integer value for mode")
        if mode > 3 and mode < 1:
            raise Exception("There are only three modes")
        if self.data_folder is None:
            raise Exception("Please input in your video folder /Usr.../folder")

    def recording(self, mode:int):

        self.handling_exception(mode)
        
        print("Press s to record, t to toggle and q to quit")

        #Retrieve all the file Path
        video_path, _, _, photo_path, photo_depth_path, _ = self.storingfilepath(mode=mode)

        idx = 0
        
        while True:
            #Retrieve Data
            # Get the frames from external realsense camera
            frame = self.getframe()
            color_image, aligned_depth_image, aligned_color_image, colorizer_depth = self.Datatreatment(frame)

            #Initialise Window
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

            #Shift between Color&depth and RGB
            if self.ColorAndDepth:
                cv2.imshow('RealSense', colorizer_depth)
            else:
                cv2.imshow('RealSense', color_image)

            key = cv2.waitKey(1)

            if key & 0xFF == ord('s') and self.isrecording is False :
                self.isrecording = True
                
                #Initialising different recording functions.
                wr, wr_colordepth, wr_depth = self.initialise_recording_function(mode=mode)

                print('...recording...')

            #Allow to toggle between Colr&Depth and RGB
            if key & 0xFF == ord('t'):
                if self.ColorAndDepth == True:
                    self.ColorAndDepth = False
                else:
                    self.ColorAndDepth = True

            if self.isrecording:
                
                #Writing the color and colorizer depth to the different recording system, wr and wr_colordepth
                wr.write(color_image)                         
                wr_colordepth.write(colorizer_depth)         
                
                #Encodes the depth array into a photo
                depth16_image = cv2.imencode('.png', aligned_depth_image)[1]
                
                #Save the depth16 image to a unique name inside the h5py file
                depth_map_name = str(idx).zfill(5) + '_depth.png'
                        
                wr_depth[depth_map_name] = depth16_image          
                
                idx += 1
                
            if (key & 0xFF == ord('q') or key == 27):

                cv2.imwrite(photo_path, color_image)
                cv2.imwrite(photo_depth_path, aligned_depth_image)
                cv2.destroyAllWindows()
                print('...quit...')
                
                self.storing_offsets_and_focal_length(frame, mode) #storing the focal length for one frame. to be used in test_cv

                break
            
        
        print(f" The video is saved at {video_path} \n The photo is saved at {photo_path} \n The depth is saved at {photo_depth_path}" )
        self.release()
        return frame


if __name__ == "__main__":

    c = Camera(data_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision/data")
    
    c.recording(mode=3)

   
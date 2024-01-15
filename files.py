import os
class Files:
    def __init__(self, home_folder):
        if home_folder is None:
            raise Exception("Home folder must not be None but type string")
        if os.path.isdir(home_folder) is False:
            raise Exception("HOME FOLDER ISNT A DIRECTORY")

        self.home_folder = home_folder
        self.json_file_path = home_folder + "/data.json"
        
        if os.path.isfile(self.json_file_path) is False:
            raise Exception('write this to a data.json file in homefolder \n {"ppx": 328.7347106933594, "ppy": 238.96812438964844, "fx": 607.7224731445312, "fy": 606.7443237304688}')
        
    
    
    def datafilepath(self, mode, data_folder):

        classify_modes = {1:"_perfect", 2:"_before", 3:"_after"}
        #Stores the RGB video here
        video_path = data_folder + "/targetvideo_rgb.mp4"
        #Stores the Color&depth video here
        video_depthcolor_path = data_folder + "/targetvideo_depthcolor.mp4"
        #stores the video_depth data here
        video_depth16_path = data_folder + "/targetvideo_depth.h5"
        #stores the last frame of the video here
        photo_path = data_folder + f"/photo{classify_modes[mode]}.jpeg"
        #stores the depth_data from the last frame of the video here
        photo_depth_path = data_folder + f"/photo_depth{classify_modes[mode]}.png"
        

        return video_path, video_depthcolor_path, video_depth16_path, photo_path, photo_depth_path, self.json_file_path

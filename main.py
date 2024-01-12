#This takes in a folder and assumes you have added your captured jpeg files in /data folder

from test_camera import Camera
from test_cv import Analyse
import cv2
from icecream import ic

class Comparison: #This class assumes you have two folders, /data and /realsense
    def __init__(self, directory_path):
        self.data_folder = directory_path + "/data"
        self.default_folder = directory_path + "/realsense"

    def reset_to_default_image_and_depth(self):
        #Reset all the files in the data_folder with the images and depth data from the default folder

        modes = ["_perfect", "_before", "_after"]
        photo_file_path = (self.data_folder + f"/photo{mode}.jpeg" for mode in modes)
        photo_path_perfect, photo_path_before, photo_path_after = photo_file_path
        photo_depth_file_path = [self.data_folder + f"/photo_depth{mode}.png" for mode in modes]


        default_image_after = cv2.imread(f"{self.default_folder}/after.jpeg") #after
        default_image_perfect = cv2.imread(f"{self.default_folder}/after1.jpeg") #perfect
        default_image_before = cv2.imread(f"{self.default_folder}/before.jpeg") #before
        default_depth_image = cv2.imread(f"{self.default_folder}/1_depth.png") #depth


        cv2.imwrite(photo_path_perfect, default_image_perfect)
        cv2.imwrite(photo_path_before, default_image_before)
        cv2.imwrite(photo_path_after, default_image_after)

        print(f"Resetting photo image: {photo_path_perfect}")
        print(f"Resetting photo image: {photo_path_before}")
        print(f"Resetting photo image: {photo_path_after}")

        for photo_depth in photo_depth_file_path:
            print(f"Resetting depth image: {photo_depth}")
            cv2.imwrite(photo_depth, default_depth_image)
    
    def return_all_data_path(self):
        modes = ["_perfect", "_before", "_after"]
        photo_file_path = (self.data_folder + f"/photo{mode}.jpeg" for mode in modes)
        photo_path_perfect, photo_path_before, photo_path_after = photo_file_path
        photo_depth_file_path = (self.data_folder + f"/photo_depth{mode}.png" for mode in modes)
        photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after = photo_depth_file_path

        return photo_path_perfect, photo_path_before, photo_path_after, photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after

    def compare(self, default = False):

        photo_path_perfect, photo_path_before, photo_path_after, photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after = self.return_all_data_path()
        
        if default:
            self.reset_to_default_image_and_depth()

        perfect = Analyse(data_folder=self.data_folder,
                        img=photo_path_perfect,
                        depth_map=photo_depth_path_perfect)
        
        before = Analyse(data_folder=self.data_folder,
                        img = photo_path_before,
                        depth_map=photo_depth_path_before)
        
        after = Analyse(data_folder=self.data_folder,
                        img = photo_path_after,
                        depth_map=photo_depth_path_after)

        perfect.show_img = True
        before.show_img = True
        after.show_img = True

        perfect_contours, perfect_points_array, perfect_sum_area = perfect.find_ellipsis_coordinates_and_depth()
        before_contours, before_points_array, before_sum_area = before.find_ellipsis_coordinates_and_depth()
        after_contours, after_points_array, after_sum_area = after.find_ellipsis_coordinates_and_depth()

        if before_sum_area != 0:
            percentage_cleaned = (before_sum_area-after_sum_area)*100/before_sum_area
            print(f"Stain removed from before to after: {percentage_cleaned}%")
        else:
            print("Percentage of stains removed is 0%. There were no stains to be removed.")
        if after_sum_area != 0:
            percentage_to_be_cleaned = (after_sum_area-perfect_sum_area)*100/after_sum_area
            print(f"Percentage of stains to be removed to be perfect: {percentage_to_be_cleaned}%")
        else:
            print(f"Percentage of stains to be removed to be perfect: 0%")

        
    

if __name__ == "__main__":

    
    machine = Comparison(directory_path="/Users/joshua/vscode/hivebotics/robot_computer_vision")
    machine.compare(default=True)
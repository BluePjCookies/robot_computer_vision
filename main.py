#This takes in a folder and assumes you have added your captured jpeg files in /data folder

from test_cv import Analyse
from icecream import ic

class Comparison: #This class assumes you have two folders, /data and /realsense
    def __init__(self, data_folder):
        self.data_folder = data_folder

        
    
    def return_all_data_path(self):
        
        modes = ["_perfect", "_before", "_after"]
        photo_file_path = (self.data_folder + f"/photo{mode}.jpeg" for mode in modes)
        photo_path_perfect, photo_path_before, photo_path_after = photo_file_path
        photo_depth_file_path = (self.data_folder + f"/photo_depth{mode}.png" for mode in modes)
        photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after = photo_depth_file_path

        return photo_path_perfect, photo_path_before, photo_path_after, photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after

    def compare(self, show_img=True):

        photo_path_perfect, photo_path_before, photo_path_after, photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after = self.return_all_data_path()
        
       
        self.perfect = Analyse(img = photo_path_perfect)
        
        self.before = Analyse(img = photo_path_before)
        
        self.after = Analyse(img = photo_path_after)

        self.perfect.show_img = show_img
        self.before.show_img = show_img
        self.after.show_img = show_img

        perfect_contours, perfect_points_array, perfect_sum_area = self.perfect.find_ellipsis_coordinates_and_depth()
        before_contours, before_points_array, before_sum_area = self.before.find_ellipsis_coordinates_and_depth()
        after_contours, after_points_array, after_sum_area = self.after.find_ellipsis_coordinates_and_depth()

        ic(perfect_sum_area, before_sum_area, after_sum_area)
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

    machine = Comparison(data_folder=f"/Users/joshua/vscode/hivebotics/robot_computer_vision/testing/TEST SET 7 (Floor)")
    machine.compare(show_img=True)
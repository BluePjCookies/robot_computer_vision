#This takes in a folder and assumes you have added your captured jpeg files in /data folder

from test_cv import Analyse
from icecream import ic
from files import Files

class Comparison: #This class assumes you have two folders, /data and /realsense
    def __init__(self, data_folder = None, has_depth=False, home_folder=None):
        self.data_folder = data_folder
        
        self.f = Files(home_folder=home_folder)

        _,_,_,photo_path_perfect, photo_depth_path_perfect, _  = self.f.datafilepath(data_folder=data_folder, mode=1)
        _,_,_,photo_path_before, photo_depth_path_before, _  = self.f.datafilepath(data_folder=data_folder, mode=2)
        _,_,_,photo_path_after, photo_depth_path_after, _  = self.f.datafilepath(data_folder=data_folder, mode=3)
        
        if has_depth is False:
            photo_depth_path_perfect, photo_depth_path_before, photo_depth_path_after = None, None, None
        
        self.perfect = Analyse(img = photo_path_perfect,
                               depth_map=photo_depth_path_perfect,
                               home_folder=home_folder)
        
        self.before = Analyse(img = photo_path_before,
                              depth_map=photo_depth_path_before,
                              home_folder=home_folder)
        
        self.after = Analyse(img = photo_path_after,
                             depth_map=photo_depth_path_after,
                             home_folder=home_folder)
    
    def compare(self, show_img=True):

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

    machine = Comparison(data_folder=f"/Users/Joshua/Vscode/Python/robot_computer_vision/realsense", 
                         has_depth=False,
                         home_folder="/Users/Joshua/Vscode/Python/robot_computer_vision")
    machine.compare(show_img=True)
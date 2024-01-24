from test_cv import Analyse
import os
import cv2
from icecream import ic
import keyboard
import time
#converting everything to jpeg
directory = "/Users/joshua/Downloads/Toilet Bowl/BAND 5 (Best-case scenairo)"

"""files = os.listdir(directory)

for path in files:
    path = directory + "/" + path
    image = cv2.imread(path)
    expected_path = path.lower().replace(".jpg", ".jpeg")
    print(expected_path)
    cv2.imwrite(expected_path, image)
    os.remove(path)"""

"""a = Analyse(
            img="/Users/joshua/Downloads/Toilet Bowl/BAND 3/img_0032.jpeg",
            show_img=True,
            home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision",
            perfect_img="/Users/joshua/Downloads/Toilet Bowl/BAND 4/img_0029.jpeg"
            )"""


"""a = Analyse(
            img="/Users/joshua/Downloads/Toilet Bowl/photo_before.jpeg",
            show_img=True,
            home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision",
            perfect_img="/Users/joshua/Downloads/Toilet Bowl/photo_after.jpeg"
            )"""

"""directory = "/Users/joshua/Downloads/Toilet Bowl/BAND 4"
path = os.listdir(directory)
for p in path:
    a = Analyse(
                img=directory + "/" + p,
                home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision"
                )

    initial_contours, initial_points_array, initial_sum_area = a.find_ellipse_coordinates_and_depth(blur_level=(3,3))
    print(p, initial_sum_area)"""

files = sorted(os.listdir(directory),key=lambda x : int(x[6:8]))
"""
for path in files:
    path = directory + "/" + path
    print(path)
    a = Analyse(
                img=path,
                home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision"
                )
    
    a.display(a.img)
    initial_contours, initial_points_array, initial_sum_area = a.find_ellipse_coordinates_and_depth(blur_level=(3,3))
    print(initial_sum_area)
    a.display(a.img)
    cv2.imwrite(path.replace(".jpeg", "_after.jpeg"), a.img)

"""
time.sleep(4)
for path in files:
    if "after" not in path:
        print(path)
        number = path[6:8]
        path = directory + "/" + path
        print(number)
        keyboard.write(number)
        keyboard.press_and_release("tab")
        a = Analyse(
                img=path,
                home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision"
                )
        initial_contours, initial_points_array, initial_sum_area = a.find_ellipse_coordinates_and_depth(blur_level=(3,3))
        keyboard.write(str(initial_sum_area))
        keyboard.press_and_release("enter")
        

        
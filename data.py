from test_cv import Analyse
import os
import cv2
from icecream import ic
"""#converting everything to jpeg
directory = "/Users/joshua/Downloads/Toilet Bowl/BAND 1 (Worst-case scenario)"

files = os.listdir(directory)

for path in files:
    path = directory + "/" + path
    image = cv2.imread(path)
    expected_path = path.lower().replace(".jpg", ".jpeg")
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

a = Analyse(
            img="/Users/joshua/Downloads/Toilet Bowl/BAND 3/img_0030.jpeg",
            show_img=True,
            home_folder="/Users/joshua/vscode/hivebotics/robot_computer_vision"
            )

initial_contours, initial_points_array, initial_sum_area = a.find_ellipse_coordinates_and_depth(blur_level=(3,3))

print(initial_sum_area)
from test_camera import Camera
from test_cv import Analyse
import cv2

video_folder = "/Users/joshua/vscode/hivebotics/robot_computer_vision/realsense"
c = Camera(video_folder= video_folder)

mode = input("mode: ")
if mode.isnumeric():
    c.recording(mode=int(mode))
else:
    image_after = cv2.imread(f"{video_folder}/after.jpeg")
    image_perfect = cv2.imread(f"{video_folder}/after1.jpeg")
    image_before = cv2.imread(f"{video_folder}/before.jpeg")
    
    _, _, _, photo_path_perfect, photo_depth_path_perfect, _ = c.storingfilepath(mode=1)

    _, _, _, photo_path_before, photo_depth_path_before, _ = c.storingfilepath(mode=2)

    _, _, _, photo_path_after, photo_depth_path_after, _ = c.storingfilepath(mode=3)

    cv2.imwrite(photo_path_perfect, image_perfect)
    cv2.imwrite(photo_path_after, image_after)
    cv2.imwrite(photo_path_before, image_before)
    data_folder = c.video_folder

    perfect = Analyse(data_folder=data_folder,
                    img=photo_path_perfect,
                    depth_map=photo_depth_path_perfect)
    before = Analyse(data_folder=data_folder,
                    img = photo_path_before,
                    depth_map=photo_depth_path_before)
    after = Analyse(data_folder=data_folder,
                    img = photo_path_after,
                    depth_map=photo_depth_path_after)

    perfect.show_img = True
    before.show_img = True
    after.show_img = True

    perfect_contours, perfect_points_array, perfect_sum_area = perfect.find_ellipsis_coordinates_and_depth()
    before_contours, before_points_array, before_sum_area = before.find_ellipsis_coordinates_and_depth()
    after_contours, after_points_array, after_sum_area = after.find_ellipsis_coordinates_and_depth()

    percentage_cleaned = (before_sum_area-after_sum_area)*100/before_sum_area
    print(f"Stain removed from before to after: {percentage_cleaned}%")
    if after_sum_area != 0:
        percentage_to_be_cleaned = (after_sum_area-perfect_sum_area)*100/after_sum_area
        print(f"Percentage of stains to be removed to be perfect: {percentage_to_be_cleaned}%")
    else:
        print(f"Percentage of stains to be removed to be perfect: 0%")
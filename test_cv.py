
import cv2
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
import json
import os
from files import Files
class Analyse:
    def __init__(self, width=640, height=480, fps=30, img = None, depth_map = None, show_img=False, home_folder=None):
        self.width = width
        self.height = height
        self.fps = fps
        
        self.img = cv2.resize(cv2.imread(img), (width, height), fx=0, fy=0, interpolation=cv2.INTER_AREA)
        self.f = Files(home_folder=home_folder)
        
        if depth_map is not None and os.path.isfile(depth_map): 
            self.depth_map = cv2.imread(depth_map, cv2.IMREAD_UNCHANGED)
        elif depth_map is None:
            self.depth_map = None
        else:
            raise Exception("depth map is not an actual file")
        
            

        self.default_data_json = self.f.json_file_path
        
        self.show_img = show_img

        
    def display(self, image):
        if self.show_img:
            cv2.imshow("Image",image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            pass

    def enhance_contrast(self, img, blur_level:tuple):
        #enhance the contrast between the stains and the background toilet
        #blur level is the level of Gaussian blur applied to the image, a higher Gaussian blur would mean a less detailed contour
        #blur level is a tuple consisting of only odd number. 
        
        self.display(img)
        #L - Lightness/Intensity, A - Green to Purple, B - Blue to yellow
        LabImg = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        L,A,B = cv2.split(LabImg)

        #Blur the Image
        #To get the most detailed contour, a value of (3, 3) for the blur_level would be recommended. (1,1) would cause errors

        blur = cv2.GaussianBlur(B, blur_level, 0)#if the dirty spot is transparent, pls change B into A, add UV light too
        self.display(blur)
        ret,thresh = cv2.threshold(blur,145,255,cv2.THRESH_BINARY)#second value is the treshold value that if you want the code more active pls decrease the value in opposite increase the value. Usually 140-150 is recommended 
        self.display(thresh)
        k1 = np.ones(blur_level, np.uint8)

        #Remove noise from the data
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, k1)

        
        self.display(thresh)

        return thresh
    
    def contour_ellipse(self, cnt):
        #By expressing such contours as an ellipse, we can identify the centre and the extreme leftmost, rightmost side (axes) of the ellipse
        area = cv2.contourArea(cnt)
        ellipse = cv2.fitEllipse(cnt)
        self.img = cv2.ellipse(self.img,ellipse,(0,255,0),2) #draw green elipse
        center, axes, angle = ellipse
        
        return area, center, axes, angle
    
    def find_ellipsis_coordinates_and_depth(self, blur_level = (3,3)) -> (float, float, float):
        
        #Determine the contours in the image
        #By expressing such contours as an ellipse, we can identify the centre and the extreme leftmost, rightmost side (axes) of the ellipse
        #Various points on the eclipse are recorded in points_array

        #Blur level is a tuple that consist of 2 odd numbered values, a lesser odd value would mean a lesser degree of blurring done to process the image.
        #To get the most detailed contour, a value of (3, 3) for the blur_level would be recommended. (1,1) would cause errors
        
        contours,_ = cv2.findContours(self.enhance_contrast(self.img, blur_level=blur_level), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sum_area=0
        points_array = []
        
        for cnt in contours:
        
            area, center, axes, angle = self.contour_ellipse(cnt)
            (h, k) = center
            (a, b) = axes

            #The distance between axes
            c = np.sqrt(abs((0.5*a)**2 - (0.5*b)**2))
            
            theta = np.radians(angle)  
            cos_theta = np.cos(theta)
            sin_theta = np.sin(theta)

            #F1 and 2 holds the coordinates of the points that are at the greatest distance apart within the ellipsis
            #F1 stores the right most coordinate
            if self.depth_map is not None:
                F1 = (int(h + c * sin_theta), int(k - c * cos_theta),self.depth_map[int(k - c * sin_theta), int(h + c * cos_theta)])
                
                #F2 stores the left most coordinate
                F2 = (int(h - c * sin_theta), int(k + c * cos_theta),self.depth_map[int(k + c * sin_theta), int(h - c * cos_theta)])
                center=(int(h),int(k),self.depth_map[int(k),int(h) ])
                
            else: 
                
                F1 = (int(h + c * sin_theta), int(k - c * cos_theta),0)
                
                #F2 stores the left most coordinate
                F2 = (int(h - c * sin_theta), int(k + c * cos_theta),0)
                center=(int(h),int(k),0)
    
            
            # print("F1:", F1)
            # print("F2:", F2)

            sum_area += area
            if area >= 200: #size of the tools.
                
                points_array.append(F1)
                points_array.append(center)
                points_array.append(F2)

                #Drawing circles at the sides of the ellipsis and at the center
                cv2.circle(self.img, (F1[0], F1[1]), 2, (255, 0, 0), -1)
                cv2.circle(self.img, (F2[0], F2[1]), 2, (255, 0, 0), -1)
                cv2.circle(self.img, (center[0], center[1]), 2, (0, 0, 255), -1)        

                cv2.drawContours(self.img,cnt,-1,(0,0,255),2) #Draw red contours
            else:
                
                points_array.append(center) 
                cv2.circle(self.img, (center[0], center[1]), 2, (0, 0, 255), -1)     
                cv2.drawContours(self.img,cnt,-1,(0,0,255),2) #draw red contours
                
        self.display(self.img)
        self.points_array = points_array
        return contours, points_array, sum_area
    
    def expressing_vectors(self, vectors, index):
        #Express vectors in terms of movement in the x,y and z coordinate
        
        return vectors[index,0], vectors[index,1], vectors[index,2]

    def normalized_vectors(self, points_array, depth_map):
       
        #get the normal vector perpendicular to the centre of the stain in the toilet bowl 
        dim1 = len(points_array)
        dim2 = 3
        dim3 = 3
        plane_points = [[[0 for _ in range(dim3)] for _ in range(dim2)] for _ in range(dim1)]

        #giving each points a vector in terms of x, y, z
        vectors=np.zeros((len(points_array), 3))
        

        #number of contour,number of points in the contour,0,x/y
        
        for i in range(len(points_array)):

            x = points_array[i][0]
            y = points_array[i][1]
            
            if self.depth_map is not None:
                plane_points[i][0] = (x + 10, y + 10, depth_map[int(y + 10), int(x+10)] )
                plane_points[i][1] = (x - 10, y + 10, depth_map[int(y - 10), int(x+10)] )
                plane_points[i][2] = (x , y - 10, depth_map[int(y - 8), int(x)] )
            else:
                plane_points[i][0] = (x + 10, y + 10, 0 )
                plane_points[i][1] = (x - 10, y + 10, 0 )
                plane_points[i][2] = (x , y - 10, 0)

            
            v1= [plane_points[i][1][0]-plane_points[i][0][0],-plane_points[i][1][1]+plane_points[i][0][1],-float(plane_points[i][1][2])+float(plane_points[i][0][2])]
            
            v2= [plane_points[i][2][0]-plane_points[i][0][0],-plane_points[i][2][1]+plane_points[i][0][1],-float(plane_points[i][2][2]) + float(plane_points[i][0][2])]

            #cross product of two vectors to determine the normal vector of v1 and v2
            normal_vector = np.cross(v1, v2)
            normal_vector_normalized = normal_vector / np.linalg.norm(normal_vector)
            vectors[i]=normal_vector_normalized

        
        return vectors
    

    def visualize_all_vectors(self, vectors, points_array, depth_map):
        coordinates = self.find_realxyz_coordinate(points_array, depth_map)
        coordinate_vectors = zip(coordinates, vectors)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for coordinate, vector in coordinate_vectors:
            vector_x, vector_y, vector_z = vector
            x, y, z = coordinate

            #simple math here to find final 3d coordinate after applying vector
            start_point = np.array([x, y, z])
            end_point = np.array([x+vector_x, y + vector_y, z + vector_z])

            ax.quiver(start_point[0], start_point[1], start_point[2],
                    end_point[0], end_point[1], end_point[2],
                    color='b', arrow_length_ratio=0.01)
            
        #set limits to the 3d graph
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_zlim([0, 1000])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


    def retrieve_offsets_and_focal_length(self):
        data = {}
        with open(self.default_data_json) as f:
            data = json.load(f)
        
        return data["ppx"], data["ppy"], data["fx"], data["fy"]

    def find_realxyz_coordinate(self, points_array, depth_map):
        #Determine the x, y, z coordinate of each stain

        #ppx -  horizontal offset of that central point
        #fx - focal length which will affect the depth map...
        ppx, ppy, fx, fy = self.retrieve_offsets_and_focal_length()

        #convert pixel coordinate to its actual x, y coordinate by offsetting the offset...
        for i in range(len(points_array)):

            x, y, z = points_array[i]
            target_xy_pixel = [x, y]
            
            if self.depth_map is not None:
                target_depth = depth_map[int(y), int(x)]  
            else:
                target_depth = 0
            
            target_xy_true = [(target_xy_pixel[0] - ppx) * target_depth / fx,
                                (target_xy_pixel[1] - ppy) * target_depth / fy]
            
            
            points_array[i] = (target_xy_true[0], target_xy_true[1], target_depth)       
            #print(target_xy_pixel[0],target_xy_pixel[1],target_xy_true[0]/10,-target_xy_true[1]/10,target_depth)
        
        camera_pos=[0,50,70]
    
        #convert pixel coordinate to a 3d xyz coordinate
        for i in range(len(points_array)):
            points_array[i]=(points_array[i][0]+camera_pos[0],
                                  points_array[i][1]+camera_pos[1],
                                  points_array[i][2]+camera_pos[2]
                                )
            
        return points_array
        

    
    
if __name__ == "__main__":
    data_folder_path = "/Users/Joshua/Vscode/Python/robot_computer_vision/realsense"
    home_folder = "/Users/Joshua/Vscode/Python/robot_computer_vision"
    image_path = data_folder_path + "/photo_before.jpeg"
    depth_path = data_folder_path + "/photo_depth.png"

    
    a = Analyse(
                img=image_path,
                show_img=True,
                depth_map=None,
                home_folder=home_folder
                )
    
    

    initial_contours, initial_points_array, initial_sum_area = a.find_ellipsis_coordinates_and_depth(blur_level=(3,3))

    initial_vectors = a.normalized_vectors(initial_points_array, a.depth_map)

    #ic(initial_vectors)
    a.visualize_all_vectors(initial_vectors, initial_points_array, a.depth_map)

    
    
    


    

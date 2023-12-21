
 
#!/usr/bin/env python
# coding=utf-8
import time
import h5py         
import pyrealsense2 as rs
import numpy as np
import cv2
import os
 
class Camera(object):

    def __init__(self, width=1280, height=720, fps=30):   
 
        self.width = width
        self.height = height
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, fps)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16,  fps)
        # self.config.enable_stream(rs.stream.infrared, 1, self.width, self.height, rs.format.y8, fps)
        # self.config.enable_stream(rs.stream.infrared, 2, self.width, self.height, rs.format.y8, fps)
        self.pipeline.start(self.config)      
 
 
    def get_frame(self):
        frames = self.pipeline.wait_for_frames()   
        colorizer = rs.colorizer()               
        depth_to_disparity = rs.disparity_transform(True)
        disparity_to_depth = rs.disparity_transform(False)
 
        # 创建对齐对象
        align_to = rs.stream.color                 
        align = rs.align(align_to)               
        aligned_frames = align.process(frames)
        # 获取对齐的帧
        aligned_depth_frame = aligned_frames.get_depth_frame()      
        color_frame   = aligned_frames.get_color_frame()
        # left_frame  = frames.get_infrared_frame(1)
        # right_frame = frames.get_infrared_frame(2)
        color_image     = np.asanyarray(color_frame.get_data())
        colorizer_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())
        depthx_image    = np.asanyarray(aligned_depth_frame.get_data())  
        # left_frame   = np.asanyarray(left_frame.get_data())
        # right_frame  = np.asanyarray(right_frame.get_data())
 
        return color_image, depthx_image, colorizer_depth
        # left_frame, right_frame
 
    def release(self):
        self.pipeline.stop()
 
 
if __name__ == '__main__':
 

    video_path         = f'/home/pthahnil/Desktop/realsense/targetvideo_rgb.mp4'
    video_depthc_path  = f'/home/pthahnil/Desktop/realsense/targetvideo_depthcolor.mp4'
    video_depth16_path = f'/home/pthahnil/Desktop/realsense/targetvideo_depth.h5'
    # video_left_path    = f'D://Realsense//Video//Stereo_left//{int(time.time())}_left.mp4'
    # video_right_path   = f'D://Realsense//Video//Stereo_right//{int(time.time())}_right.mp4'
 

    # fps, w, h = 90, 1920, 1080
    fps, w, h = 30, 640, 480
    mp4        = cv2.VideoWriter_fourcc(*'mp4v')  
            
    # wr_left    = cv2.VideoWriter(video_left_path, mp4, fps, (w, h),      isColor=False)
    # wr_right   = cv2.VideoWriter(video_right_path, mp4, fps, (w, h),     isColor=False)
 
 

 
    cam = Camera(w, h, fps)
    flag_V = 0
    idx = 0
    id  = 0
    print('Take a vedio: s, Shot and quit：q')
 
 
    while True:
     
            color_image, depthxy_image, colorizer_depth = cam.get_frame()
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)
            key = cv2.waitKey(1)
 
            if key & 0xFF == ord('s') :
                flag_V = 1
  
                wr = cv2.VideoWriter(video_path, mp4, fps, (w, h), isColor=True)
                wr_colordepth = cv2.VideoWriter(video_depthc_path, mp4, fps, (w, h), isColor=True)
                wr_depth = h5py.File(video_depth16_path, 'w')
                print('...录制视频中...')
            if flag_V == 1:

                wr.write(color_image)                          # 保存RGB图像帧
                wr_colordepth.write(colorizer_depth)           # 保存相机自身着色深度图
                # wr_left.write(left_image)                      # 保存左帧深度图
                # wr_right.write(right_image)                    # 保存右帧深度图
                # res, depth16_image = cv2.imencode('.png', depthxy_image)  # 深度图解码方式一：点云小，但是出错
                depth16_image = cv2.imencode('.png', depthxy_image)[1]      # 深度图解码方式二：文件较大，测试稳定
                depth_map_name = str(id).zfill(5) + '_depth.png'
                # wr_depth[str(idx).zfill(5)] = depth16_image          #  储存方法：1 前3帧和没11帧出现高质量点云，其他错误
                wr_depth[depth_map_name] = depth16_image           #  储存方法：2 所有点云准确，但是点云质量不高
                idx += 1
                id = id + 1
            if key & 0xFF == ord('q') or key == 27:
                cv2.imwrite('/home/pthahnil/Desktop/realsense/1.jpg',color_image)
                cv2.imwrite('/home/pthahnil/Desktop/realsense/1_depth.png',depthxy_image)
                cv2.destroyAllWindows()
                print('...录制结束/直接退出...')
                break

    wr.release()
    wr_colordepth.release()
    # wr_left.release()
    # wr_right.release()
    wr_depth.close()
    cam.release()
    print(f'If you save the vedio，vedio is at：{video_path}')


import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

# device is Intel RealSense D435 (S/N: 213622070558  FW: 05.12.07.150
# device = pipeline_profile.get_device()

# device_product_line is D400
# device_product_line = str(device.get_info(rs.camera_info.product_line))

# Depth Camera Configuration
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Color Camera Configuration
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow('color_depth', color_image)
        print("h, w : ", color_frame.height, color_frame.width)
        # print(type(color_image))
        # print(len(color_image))
        # print(type(color_image.tobytes()))
        # print(len(color_image.tobytes()))

        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()

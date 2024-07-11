# bag2_image
ros2 bag files image topic to images
This Python script subscribes to a ROS 2 topic (/camera/image) and saves incoming images at a rate of 1 frame per second (FPS) using a specified Quality of Service (QoS) profile. The script utilizes the rclpy library for ROS 2 communication and cv_bridge to convert ROS image messages to OpenCV images.

Key Features:
QoS Settings: Configures the subscriber with BEST_EFFORT reliability, VOLATILE durability, and KEEP_LAST history with a depth of 10.
Image Saving: Saves images to an output_images directory, creating the directory if it does not exist.
Timestamped Filenames: Each image is saved with a filename containing the current timestamp to ensure unique filenames.
Rate Control: Ensures images are saved at a rate of 1 FPS by checking the time elapsed since the last saved image.

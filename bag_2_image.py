import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, LivelinessPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from datetime import datetime

class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('image_subscriber')
        self.qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            lifespan=rclpy.duration.Duration(),
            deadline=rclpy.duration.Duration(),
            liveliness=LivelinessPolicy.AUTOMATIC,
            liveliness_lease_duration=rclpy.duration.Duration()
        )
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/ouster/signal_image',
            self.listener_callback,
            self.qos_profile)
        self.last_saved_time = None
        self.output_directory = "output_images"
        os.makedirs(self.output_directory, exist_ok=True)

    def listener_callback(self, msg):
        current_time = self.get_clock().now().to_msg()
        if self.last_saved_time is None or (current_time.sec - self.last_saved_time.sec >= 1):
            self.last_saved_time = current_time
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = os.path.join(self.output_directory, f"image_{timestamp_str}.png")
            cv2.imwrite(image_filename, cv_image)
            self.get_logger().info(f'Image saved: {image_filename}')

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


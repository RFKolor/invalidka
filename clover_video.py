import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from clover import long_callback

rospy.init_node('cv')
bridge = CvBridge()

@long_callback
def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image


image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

rospy.spin()
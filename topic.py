import rospy
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

#инициализация ноды (программы)
rospy.init_node('topic')

#инициализация используемых сервисов 
bridge = CvBridge()

#создание пустого топика 
camera = rospy.Publisher("/color_debug", Image, queue_size=10)

def callback(msg):
    #frame - каждый кадр видео взятого из топика 'main_camera/image_raw'
    frame = bridge.imgmsg_to_cv2(msg, 'bgr8')
    #публикация изображения 
    camera.publish(bridge.cv2_to_imgmsg(frame, 'bgr8'))

rospy.Subscriber('main_camera/image_raw', Image, callback)
    
rospy.sleep(10)
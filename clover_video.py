import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from clover import long_callback
import numpy as np

rospy.init_node('cv')
bridge = CvBridge()

def color(frame, lower, upper):
    # перевод изображения в формат hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # ищем нужные цвета в диапазоне от нижнего предела до верхнего
    mask = cv2.inRange(hsv, lower, upper)
    # находим контуры
    cont, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # CHAIN_APPROX_SIMPLE - контуры сохраняются в 1 кортеже
    return cont


@long_callback
def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')
    
    # задаются нижние пределы. ВСЕ В HSV
    #надо понять как найти нижний и верхний предел опредленного цвета
    # щас здесь пределы из кода дипсика
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    #желтый цвет
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    #обращаемся к функции и она находит нужные цвета на картинке
    #все черное,ток красный видно(как мы проверяли)
    red = color(img, lower_red, upper_red)
    #точно также желтый
    yellow = color(img, lower_red, upper_red)
    # функция возращает кортеж и там хранятся точки красного на картинке
    #скорее всего точки крайние
    red_cont, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #рисует прямоугольникам по точкам из кортежа для красного
    for contour in red_cont:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #такая же хуйня для желтого цвета
    yellow = color(img, lower_red, upper_red)
    for contour in red_cont:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(yellow, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #изображение выводится в топик
    img.publish(bridge.cv2_to_imgmsg(img, "bgr8"))


image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

rospy.spin()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from abc import ABCMeta, abstractmethod
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2


class AbstractBurger(object):
    __metaclass__ = ABCMeta
    def __init__(self, use_lidar=False ,use_camera=False, camera_preview=False):
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        # lidar scan subscriber
        if use_lidar:
            self.scan = None
            self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

        # camera subscribver
        # please uncoment out if you use camera
        if use_camera:
            # for convert image topic to opencv obj
            self.img = None
            self.camera_preview = camera_preview
            self.bridge = CvBridge()
            self.image_sub = rospy.Subscriber('image_raw', Image, self.imageCallback)

    # lidar scan topic call back sample
    # update lidar scan state
    def lidarCallback(self, data):
        self.scan = data.ranges

    # camera image call back sample
    # comvert image topic to opencv object and show
    def imageCallback(self, data):
        try:
            self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        if self.camera_preview:
          cv2.imshow("Image window", self.img)
          cv2.waitKey(1)

    @abstractmethod
    def strategy(self):
        pass


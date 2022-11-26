import os
import re
import time
import xml.etree.cElementTree as ET


def run_without_output(cmd):
    os.popen(cmd)


def run_with_output(cmd):
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode()
    except UnicodeDecodeError:
        return bf.decode('gbk')

class Element:

    ADB_UI_TREE_DUMP_CMD = "adb shell uiautomator dump /data/local/tmp/uidump.xml"
    ADB_GET_UI_TREE_CMD = "adb shell cat /data/local/tmp/uidump.xml"

    def __init__(self):
        self.pattern = re.compile(r"\d+")
        self.ui_tree = ""

    def __uidump(self):
        """
        获取当前Activity控件树
        """
        run_with_output(self.ADB_UI_TREE_DUMP_CMD)
        self.ui_tree = run_with_output(self.ADB_GET_UI_TREE_CMD)

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组
        """
        
        self.__uidump()
        tree = ET.ElementTree(ET.fromstring(self.ui_tree))

        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                return Xpoint, Ypoint

    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表
        """
        self.__uidump()
        tree = ET.ElementTree(ET.fromstring(self.ui_tree))
        
        l = []
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                l.append((Xpoint, Ypoint))
        return l

    def findElementByName(self, name):
        """
        通过元素名称定位
        usage: findElementByName(u"相机")
        """
        return self.__element("text", name)

    def findElementsByName(self, name):
        return self.__elements("text", name)

    def findElementByClass(self, className):
        """
        通过元素类名定位
        usage: findElementByClass("android.widget.TextView")
        """
        return self.__element("class", className)

    def findElementsByClass(self, className):
        return self.__elements("class", className)

    def findElementById(self, id):
        """
        通过元素的resource-id定位
        usage: findElementsById("com.android.deskclock:id/imageview")
        """
        return self.__element("resource-id",id)

    def findElementsById(self, id):
        return self.__elements("resource-id",id)


class Event:

    ADB_WAIT_DEVICE_CMD = "adb wait-for-device "
    ADB_TOUCH_CMD = "adb shell input tap {} {}"

    def __init__(self):
        run_with_output(self.ADB_WAIT_DEVICE_CMD)

    def touch(self, dx, dy):
        """
        触摸事件
        usage: touch(500, 500)
        """
        run_with_output(self.ADB_TOUCH_CMD.format(dx, dy))


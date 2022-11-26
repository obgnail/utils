from adb import Element, Event
import time

def test():
    element = Element()
    evevt = Event()
    
    e1 = element.findElementByName(u"企业微信")
    evevt.touch(e1[0], e1[1])

    e2 = element.findElementByName(u"研发沟通")
    evevt.touch(e2[0], e2[1])

if __name__ == "__main__":
    test()

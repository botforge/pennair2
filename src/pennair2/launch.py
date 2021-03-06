# Copyright (C) 2018  Penn Aerial Robotics
# Fill copyright notice at github.com/pennaerial/pennair2/NOTICE

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import rospkg
import os
import roslaunch
import rospy

active_launches = []


def _shutdown_handler():
    for launch in active_launches:
        launch.shutdown()


def launch(package, name):
    """API call to roslaunch. Same as command line.

    :param package: The package name.
    :param name: The name of the launch file
    :param kwargs: Not implemented in Kinetic. TODO: Implement in Lunar
    """
    rospack = rospkg.RosPack()
    path = rospack.get_path(package) + "/launch"
    path += "/" + name

    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [path])

    active_launches.append(launch)
    rospy.on_shutdown(_shutdown_handler)
    launch.start()


class Node:
    def __init__(self, name, params):
        # type: (str, dict) -> None
        self.name = name  # type: str
        self.element = Element("node")  # type: xml.Element
        for name, value in params.iteritems():
            self.add_param(name, value)

    def add_param(self, name, value):
        SubElement(self.element, "param", {"name": name, "value": value})

    def add_remap(self, old, new):
        SubElement(self.element, "remap", {"from": old, "to": new})

    def add_rosparam(self, name, text):
        rosparam = SubElement(self.element, "rosparam", {"param": name})
        rosparam.text = text

    def add_attribute(self, name, value):
        self.element.set(name, value)


class LaunchFile:
    def __init__(self):
        self.element = Element("launch")
        self.nodes = {}

    def add_node(self, node):
        # type: (xml.Element) -> None
        self.element.append(node.element)
        self.nodes[node.name] = node

    def generate(self):
        reparsed = minidom.parseString(tostring(self.element))
        return reparsed.toprettyxml(indent="    ")

    def write(self, package, name):
        rospack = rospkg.RosPack()
        path = rospack.get_path(package) + "/launch"
        if not os.path.exists(path):
            os.makedirs(path)
        path += "/" + name
        with open(path, "w") as f:
            f.write(self.generate())

import os
p = os.path.realpath(__file__)
p = os.path.dirname(p) + "/../"
import sys
sys.path.append(p)
from davinci.transforms import DaVinciClassicRobot

r = DaVinciClassicRobot()
r.viz_robot()
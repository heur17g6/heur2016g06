

import sys
from time import sleep

from algos.TightFit_B import TightFit_B
from bases.base_a import base_a
from bases.base_b import base_b
from bases.base_dynamic import base_dynamic
from param_searchers.sa_2 import sa_2
from src.Groundplan import Groundplan
from src.GroundplanFrame import GroundplanFrame
from test_config import test_config

f = GroundplanFrame(Groundplan())
f.repaint(Groundplan())

b = base_a(40,True,200,170).deepCopy()

#sleep(4)

"""gif 1 : base a , grid placer a (i=1,j=2,k=3)"""
# shows grid placer a putting residences on base a, with params i=1,j=2,k=3
from algos.TightFit_A import TightFit_A
from algos.TightFitWB import TightFitWB




while True:

    TightFit_A(b.deepCopy(),1.0,2.0,3.0,frame=f,slow=True)
    #TightFitWB(Groundplan(enable_playground=False),1.0, 2.0, 3.0, frame=f, slow=True)



    """gif 2 : sa finding parameters for gif 1"""
    condig = {
        "variables": {
            "Bases": [base_b]
        },
        "constants": {
            "max_iterations": 25,
            'min': 1.0,
            'max': 15.0
        }
    }

    #sa_2(b,condig,TightFit_A,frame=f,slow=True)



"""gif 3 : zoom finding parameters for gif 1"""


"""gif 4 : uniform distributed waterbodies"""

"""gif 5: other_approach , showing functions"""
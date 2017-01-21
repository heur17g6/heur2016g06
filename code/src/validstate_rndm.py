from random import random

import time

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody

# a modified evolver, returns first valid solution it finds
from src.GroundplanFrame import GroundplanFrame


class validstate_rndm(object):
    ITERATIONS_BEFORE_RESET = 4

    @staticmethod
    def findValidHouse(plan, type_to_place, pre,timeout,t):

        h = None


        while True:
            if timeout < time.time()-t:
                #print time.time()-t
                return h

            if pre is None or random() < 0.5:
                x = int(random() * plan.WIDTH)
                y = int(random() * plan.HEIGHT)
            else:
                x = int(pre.getX() - 5 + 10 * random())
                y = int(pre.getY() - 5 + 10 * random())

            if type_to_place is "FamilyHome":
                # skip flipping because FamilyHome has w==h
                h = FamilyHome(x, y)
                if plan.correctlyPlaced(h): return h

            elif type_to_place is "Bungalow":
                h = Bungalow(x, y)
            elif type_to_place is "Mansion":
                h = Mansion(x, y)

            if random() < 0.5: h = h.flip()
            if plan.correctlyPlaced(h): break
            h = h.flip()
            if plan.correctlyPlaced(h): break

        return h

    @staticmethod
    def mutateWater(plan,timeout,t):

        # get number of water bodies
        num_wbs = len(plan.getWaterbodies())

        # remove a random water body
        if num_wbs > 0:
            plan.removeWaterbody(plan.getWaterbodies()[int(random() * num_wbs)])
            num_wbs -= 1

        # dimensions of water bodies
        v1 = int(plan.WIDTH / 4)
        v2 = int(plan.HEIGHT / 5)

        # try many times to place wbs until 4 have been placed
        while True:

            if timeout < time.time()-t:
                return plan

            if num_wbs >= 4: break

            x = int(random() * plan.WIDTH)
            y = int(random() * plan.HEIGHT)

            # randomly decide rotation
            if random() < 0.5:
                wb = Waterbody(x, y, v1, v2)
            else:
                wb = Waterbody(x, y, v2, v1)

            if plan.correctlyPlaced(wb):
                plan.addWaterbody(wb)
                num_wbs += 1

        return plan

    def mutateAHouse(self, plan, i,timeout,t):

        toberemoved = None

        if plan.getNumberOfHouses() is plan.NUMBER_OF_HOUSES:
            ind = int(random() * plan.NUMBER_OF_HOUSES)
            toberemoved = plan.getResidence(ind)

            type_to_place = toberemoved.getType()
            plan.removeResidence(toberemoved)

        else:
            if i % 10 < 5:
                type_to_place = "FamilyHome"
            elif i % 10 < 8:
                type_to_place = "Bungalow"
            else:
                type_to_place = "Mansion"

        h = self.findValidHouse(plan, type_to_place, toberemoved,timeout,t)

        if h is not None: plan.addResidence(h)

        return [plan, h is not None]

    def getPlan(self):
        return self.plan

    # input key to continue existing thread of evolution
    def __init__(self, plan,timeout):

        self.plan = plan

        i = 0

        t = time.time()

        while True:


            if timeout < time.time() - t:
                # print time.time() - t
                break

            # plan = self.mutateWater(plan)
            #print "ok"
            res = self.mutateAHouse(plan, i,timeout,t)



            if res[1]:  # if succeeded in house mutation
                self.plan = res[0]
                i += 1

            if self.plan.isValid():
                break

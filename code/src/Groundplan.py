import math

from districtobjects.Residence import Residence
from districtobjects.Waterbody import Waterbody

from districtobjects.Ground import Ground


class Groundplan(object):
    
    WIDTH = 200
    HEIGHT = 170
    AREA = WIDTH * HEIGHT
    MINIMUM_WATER_PERCENTAGE = 0.2
    MAXIMUM_WATER_BODIES = 4
    MINIMUM_FAMILYHOMES_PERCENTAGE = 0.50
    MINIMUM_BUNGALOW_PERCENTAGE = 0.30
    MINIMUM_MANSION_PERCENTAGE = 0.20
    MAXIMUM_PLAYGROUND_DISTANCE = 50

    def __init__(self, number_of_houses, playground):
        self.PLAYGROUND = playground

        self.ground = Ground(0, 0, self.WIDTH, self.HEIGHT)
        self.number_of_houses = number_of_houses

        self.number_of_familyhomes = 0
        self.number_of_bungalows = 0
        self.number_of_mansions = 0

        self.residences = []
        self.waterbodies = []
        self.playgrounds = []

    def getNumberOfHouses(self):
        return self.number_of_familyhomes + self.number_of_bungalows + self.number_of_mansions

    def __copy__(self):
        return type(self)

    def getWidth(self):
        return self.WIDTH

    def getHeight(self):
        return self.HEIGHT

    def getResidences(self):
        return self.residences

    def getResidence(self, index):
        return self.residences[index]

    def getWaterbodies(self):
        return self.waterbodies

    def getPlaygrounds(self):
        return self.playgrounds

    def numberOfHouses(self):
        return self.number_of_houses

    def addResidence(self, residence):
        if residence.getType() == "FamilyHome":
            self.number_of_familyhomes += 1
        elif residence.getType() == "Bungalow":
            self.number_of_bungalows += 1
        elif residence.getType() == "Mansion":
            self.number_of_mansions += 1
        self.residences.append(residence)

    def removeResidence(self, residence):

        if residence.getType() == "FamilyHome":
            self.number_of_familyhomes -= 1
        elif residence.getType() == "Bungalow":
            self.number_of_bungalows -= 1
        elif residence.getType() == "Mansion":
            self.number_of_mansions -= 1
        self.residences.remove(residence)

    def addWaterbody(self, waterbody):
        self.waterbodies.append(waterbody)

    def removeWaterbody(self, waterbody):
        self.waterbodies.remove(waterbody)

    def addPlayground(self, playground):
        self.playgrounds.append(playground)

    def removePlayground(self, playground):
        self.playgrounds.remove(playground)

    def isValid(self):
        if (len(self.waterbodies) > self.MAXIMUM_WATER_BODIES or
                    (float(self.number_of_familyhomes) / self.number_of_houses) < self.MINIMUM_FAMILYHOMES_PERCENTAGE or
                    (float(self.number_of_bungalows) / self.number_of_houses) < self.MINIMUM_BUNGALOW_PERCENTAGE or
                    (float(self.number_of_mansions) / self.number_of_houses) < self.MINIMUM_MANSION_PERCENTAGE):
            print "problem: incorrect ratio / number of elements"
            return False
        else:
            waterbody_surface = 0
            for waterbody in self.waterbodies:
                if not self.correctlyPlaced(waterbody):
                    print "problem: incorrectly placed water"
                    return False
                else:
                    waterbody_surface += waterbody.getSurface()

            if (float(waterbody_surface) / self.AREA) < self.MINIMUM_WATER_PERCENTAGE:
                print "problem: water percent " , float(waterbody_surface)/self.AREA
                return False
            for residence in self.residences:
                if not self.correctlyPlaced(residence):
                    print "problem: residence incorrectly placed"
                    return False

            return True

    def correctlyPlaced(self, placeable):

        def overlap(o1, o2):
            if o1 is o2: return False
            if o1.topEdge() > o2.bottomEdge() \
                    or o2.topEdge() > o1.bottomEdge() \
                    or o1.rightEdge() < o2.leftEdge() \
                    or o2.rightEdge() < o1.leftEdge():
                return False
            else:
                return True

        if (placeable.topEdge() < self.ground.topEdge() or
                    placeable.rightEdge() > self.ground.rightEdge() or
                    placeable.bottomEdge() > self.ground.bottomEdge() or
                    placeable.leftEdge() < self.ground.leftEdge()):
            return False

        if isinstance(placeable, Residence):

            if (placeable.topEdge() < placeable.getminimumClearance() or
                        placeable.rightEdge() > self.ground.rightEdge() - placeable.getminimumClearance() or
                        placeable.bottomEdge() > self.ground.bottomEdge() - placeable.getminimumClearance() or
                        placeable.leftEdge() < placeable.getminimumClearance()):
                return False

        for waterbody in self.waterbodies:

            if waterbody is not placeable and overlap(waterbody, placeable):
                return False

        self_clearance = 0

        if isinstance(placeable, Residence):
            self_clearance = placeable.getminimumClearance()

        for residence in self.residences:
            if residence is placeable: continue
            if overlap(residence, placeable): return False
            if not isinstance(placeable,Waterbody):
                if self.getDistance(residence, placeable) < max(self_clearance,residence.getminimumClearance()):

                    return False

        if self.PLAYGROUND:

            if len(self.playgrounds) is 0:
                return False
            ok = False
            for playground in self.playgrounds:
                #print "pg",playground
                if overlap(placeable, playground): return False
                if isinstance(placeable, Residence):
                    min_ok = placeable.getminimumClearance()
                    max_ok = self.MAXIMUM_PLAYGROUND_DISTANCE
                    distance = self.getDistance(playground, placeable)
                    #print min_ok,distance,max_ok
                    if distance < min_ok or max_ok < distance:
                        #print "was bad distance from playground :("
                        pass # return False
                    else:
                        ok = True
                        break
                    #print "ok"
                    #print "was ok distance from playground :)"
            if not ok: return False
        return True

    def getDistance(self, residence, other):
        if (residence.topEdge() <= other.bottomEdge() and
                    residence.rightEdge() >= other.leftEdge() and
                    residence.bottomEdge() >= other.topEdge() and
                    residence.leftEdge() <= other.rightEdge()):
            return 0
        elif (residence.topEdge() < other.bottomEdge() and
                      residence.rightEdge() < other.leftEdge() and
                      residence.bottomEdge() > other.topEdge()):
            return other.leftEdge() - residence.rightEdge()
        elif (residence.topEdge() < other.bottomEdge() and
                      residence.bottomEdge() > other.topEdge() and
                      residence.leftEdge() > other.rightEdge()):
            return residence.leftEdge() - other.rightEdge()
        elif (residence.topEdge() > other.bottomEdge() and
                      residence.rightEdge() > other.leftEdge() and
                      residence.leftEdge() < other.rightEdge()):
            return residence.topEdge() - other.bottomEdge()
        elif (residence.rightEdge() > other.leftEdge() and
                      residence.bottomEdge() - other.topEdge() and
                      residence.leftEdge() < other.rightEdge()):
            return other.topEdge() - residence.bottomEdge()
        elif (residence.topEdge() < other.bottomEdge() and
                      residence.rightEdge() > other.leftEdge()):
            return math.sqrt(math.pow(residence.leftEdge() - other.rightEdge(), 2) +
                             math.pow(other.topEdge() - residence.bottomEdge(), 2))
        elif (residence.topEdge() < other.bottomEdge() and
                      residence.leftEdge() < other.rightEdge()):
            return math.sqrt(math.pow(other.leftEdge() - residence.rightEdge(), 2) +
                             math.pow(other.topEdge() - residence.bottomEdge(), 2))
        elif (residence.rightEdge() > other.leftEdge() and
                      residence.bottomEdge() > other.topEdge()):
            return math.sqrt(math.pow(residence.leftEdge() - other.rightEdge(), 2) +
                             math.pow(residence.topEdge() - other.bottomEdge(), 2))
        elif (residence.bottomEdge() > other.topEdge() and
                      residence.leftEdge() < other.rightEdge()):
            return math.sqrt(math.pow(other.leftEdge() - residence.rightEdge(), 2) +
                             math.pow(residence.topEdge() - other.bottomEdge(), 2))

    def getPlanValue(self):
        planValue = 0
        for residence in self.residences:
            planValue += self.getResidenceValue(residence)
        if self.PLAYGROUND:
            for playground in self.playgrounds:
                planValue -= playground.getPrice()
        return planValue

    def getResidenceValue(self, residence):
        value_residence = residence.getValue()
        distance = self.getMinimumDistance(residence)
        value_increase = residence.getAddedValuePercentage() * value_residence
        return value_residence + (max(distance - residence.getminimumClearance(), 0)) * value_increase

    def getMinimumDistance(self, residence):
        minimum = residence.leftEdge()
        if residence.topEdge() < minimum:
            minimum = residence.topEdge()
        if self.ground.rightEdge() - residence.rightEdge() < minimum:
            minimum = self.ground.rightEdge() - residence.rightEdge()
        if self.ground.bottomEdge() - residence.bottomEdge() < minimum:
            minimum = self.ground.bottomEdge() - residence.bottomEdge()
        for other in self.residences:
            if residence != other:
                distance = int(self.getDistance(residence, other))
                if distance < minimum:
                    minimum = distance
        return minimum
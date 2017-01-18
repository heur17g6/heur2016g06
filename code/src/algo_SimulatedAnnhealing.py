from random import random

from src.GroundplanFrame import GroundplanFrame


def simulated_annealing(init_state, max_iterations, generateNeighbor):
    state = init_state.deepCopy()
    best_state = init_state.deepCopy()

    frame = GroundplanFrame(state)
    bframe = GroundplanFrame(best_state)

    for i in range(max_iterations):

        frame.repaint(state)
        bframe.repaint(best_state)

        neighbor = generateNeighbor(state.deepCopy())
        temperature = float(i + 1) / max_iterations

        print state.getPlanValue(), neighbor.getPlanValue(), best_state.getPlanValue()

        print "t =", temperature, ", i =", i
        if neighbor.getPlanValue() > state.getPlanValue():
            state = neighbor.deepCopy()
            if state.getPlanValue() > best_state.getPlanValue():
                best_state = state.deepCopy()
        elif (state.getPlanValue() - neighbor.getPlanValue()) / temperature > random():
            state = neighbor.deepCopy()

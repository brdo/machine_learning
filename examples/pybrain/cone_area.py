#!/usr/bin/python

"""
Cone surface area optimization using NSGA-II multi-objective optimization algorithm
"""

from pybrain.optimization import ConstMultiObjectiveGA
from pybrain.rl.environments.functions.multiobjective import MultiObjectiveFunction
from scipy import array, sqrt, pi, zeros
import pylab

class ConeArea(MultiObjectiveFunction):

    def __init__(self, minVolume=200, radiusBounds=(0, 10), heightBounds=(0, 20)):
        self.minVolume = minVolume

        # contraint on radius and height of cone
        xbound = []
        xbound.append(radiusBounds)
        xbound.append(heightBounds)

        self.xbound = xbound

        # 2 dimensions, radius and height
        self.xdim = 2
        self.constrained = True
        self.feasible = True

    def g(self, x):
        r, h = x[0], x[1]

        # calculate the volume
        g1 = 1.0 / 3 * h * pi * r * r

        if g1 < self.minVolume:
            # minimum volume constraint failed
            # solution not feasible
            return False, array([g1])

        return True, array([g1])

    def f(self, x):
        # minimize both side and total surface area
        feasible, violation = self.g(x)

        # major hack to fix issue with MultiObjectiveFunction properties
        # see https://github.com/pybrain/pybrain/issues/167
        MultiObjectiveFunction.outfeasible = feasible
        MultiObjectiveFunction.outviolation = violation

        r, h = x[0], x[1]

        # side surface area
        f1 = pi * r * sqrt(r * r + h * h)

        # total surface area
        f2 = pi * (r * r) + f1

        return -array([f1, f2])

def dbg(alg):
    """
    debug output of solution
    """
    print 'Population size ',alg.populationSize
    print 'Objective Evaluation number ',alg.numEvaluations
    print 'last generation Length of bestEvaluation ',len(alg.bestEvaluation)
    print 'Best Evaluable : Best Evaluation'
    for i in range(len(alg.bestEvaluation)):
        assert len(alg.bestEvaluation) == len(alg.bestEvaluable)
        print alg.bestEvaluable[i],':',alg.bestEvaluation[i]

    print 'Plotting the results (blue = all evaluated points, red = resulting pareto front)'
    for x in alg._allEvaluations:
        if x[1]:
            pylab.plot([x[0][0]], [x[0][1]], 'b.')
        else:
            pylab.plot([x[0][0]], [x[0][1]], 'r.')

    for x in alg.bestEvaluation:
        pylab.plot([x[0][0]], [x[0][1]], 'go')
    pylab.show()

    print 'Pareto Front'
    for x in alg.bestEvaluation:
        pylab.plot([x[0][0]], [x[0][1]], 'go')
    pylab.show()

def main():

    f = ConeArea(200, (0, 10), (0, 20))

    x0 = zeros(f.indim)

    alg = ConstMultiObjectiveGA(f, x0,
        storeAllEvaluations=True,
        populationSize=100, eliteProportion=1.0,
        topProportion=1.0, mutationProb=1.0,
        mutationStdDev=0.3, storeAllPopulations=True,
        allowEquality=False)

    print 'Start Learning'
    alg.learn(40)
    print 'End Learning'

    dbg(alg)

if __name__ == '__main__':

    main()

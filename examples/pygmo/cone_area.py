#!/usr/bin/python

"""
Cone surface area optimization using NSGA-II multi-objective optimization algorithm
Problem: http://www.math.unipd.it/~marcuzzi/DIDATTICA/LEZ&ESE_PIAI_Matematica/3_cones.pdf
"""

import PyGMO
from math import sqrt, pi
from PyGMO.problem import base, zdt

class ConeArea(base):

    def __init__(self, minVolume=200, radiusBounds=(0, 10), heightBounds=(0, 20)):
        self.minVolume = minVolume

        super(ConeArea, self).__init__(2, 0, 2, 1, 0);

        # sets the problem bounds
        self.set_bounds((radiusBounds[0],heightBounds[0]),
                        (radiusBounds[1],heightBounds[1]))

    def _compute_constraints_impl(self, x):
        r, h = x[0], x[1]

        # calculate the volume
        v = 1.0 / 3 * h * pi * r * r

        return (0,) if (v > self.minVolume) else (1,)

    def _objfun_impl(self, x):
        """
        reimplement the virtual method that defines the obf function
        """
        r, h = x[0], x[1]

        # calculate the volume
        v = 1.0 / 3 * h * pi * r * r

       ## nsga2 doesn't support constraints so artificially make them
       #if (v < self.minVolume):
       #    return (1000000, 1000000)

        # side surface area
        f1 = pi * r * sqrt(r * r + h * h)

        # total surface area
        f2 = pi * (r * r) + f1
        return (f1, f2)

    def human_readable_extra(self):
        return "Cone Area minimization problem"


def main():

    prob = ConeArea(200, (0, 10), (0, 20))
    alg = PyGMO.algorithm.ihs(100)
    pop = PyGMO.population(prob, 200)

    print prob
    #print alg
    print 'Start Learning'
    for i in range(100):
        pop = alg.evolve(pop)
    print 'End Learning'

    import pylab
    pop.plot_pareto_fronts()
    pylab.show()

if __name__ == '__main__':

    main()

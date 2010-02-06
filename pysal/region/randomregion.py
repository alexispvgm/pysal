"""
Generate random regions

Randomly form regions given various types of constraints on cardinality and
composition.

Author(s):
    David Folch dfolch@asu.edu
    Serge Rey srey@asu.edu

    
"""
import pysal
from pysal.common import *

class Random_Regions:
    """Generate a list of Random_Region instances.
    

    Parameters
    ----------

    area_ids        : list
                      IDs indexing the areas to be grouped into regions (must
                      be in the same order as spatial weights matrix if this
                      is provided)
                    
    num_regions     : integer
                      number of regions to generate (if None then this is 
                      chosen randomly from 2 to n where n is the number of 
                      areas)

    cardinality     : list
                      list containing the number of areas to assign to regions
                      (if num_regions is also provided then len(cardinality)
                      must equal num_regions; if cardinality=None then a list 
                      of length num_regions will be generated randomly)

    contiguity      : W
                      spatial weights object (if None then contiguity will be 
                      ignored)

    maxiter         : int
                      maximum number attempts at finding a feasible solution
                      (only affects contiguity constrained regions) 

    permutations    : int
                      number Random_Region instances to generate
                      

    Attributes
    ----------

    solutions       : list
                      list of length permutations containing all Random_Region 
                      instances generated

    solutions_feas  : list
                      list of the Random_Region instances that resulted in
                      feasible solutions

    Examples
    --------

    >>> import random
    >>> import numpy as np
    >>> nregs = 13
    >>> cards = range(2,14) + [10]
    >>> w = pysal.weights.weights.lat2gal(10,10,rook=False)
    >>> ids = w.id_order
    >>>
    >>> # unconstrained
    >>> random.seed(10)
    >>> np.random.seed(10)
    >>> t0 = Random_Regions(ids, permutations=2)
    >>> t0.solutions[0].regions[0]
    [19, 14, 43, 37, 66, 3, 79, 41, 38, 68, 2, 1, 60]
    >>> # cardinality and contiguity constrained (num_regions implied)
    >>> random.seed(60)
    >>> np.random.seed(60)
    >>> t1 = Random_Regions(ids, num_regions=nregs, cardinality=cards, contiguity=w, permutations=2)
    >>> t1.solutions[0].regions[0]
    [7, 18, 29, 17, 38, 48, 19, 28, 39, 37, 47, 36, 57]
    >>> # cardinality constrained (num_regions implied)
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t2 = Random_Regions(ids, num_regions=nregs, cardinality=cards, permutations=2)
    >>> t2.solutions[0].regions[0]
    [37, 62]
    >>> # number of regions and contiguity constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t3 = Random_Regions(ids, num_regions=nregs, contiguity=w, permutations=2)
    >>> t3.solutions[0].regions[1]
    [79, 68, 57, 89, 47, 98, 36, 56, 69, 58, 78, 26, 48]
    >>> # cardinality and contiguity constrained
    >>> random.seed(60)
    >>> np.random.seed(60)
    >>> t4 = Random_Regions(ids, cardinality=cards, contiguity=w, permutations=2)
    >>> t4.solutions[0].regions[0]
    [7, 18, 29, 17, 38, 48, 19, 28, 39, 37, 47, 36, 57]
    >>> # number of regions constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t5 = Random_Regions(ids, num_regions=nregs, permutations=2)
    >>> t5.solutions[0].regions[0]
    [37, 62, 26, 41, 35, 25, 36]
    >>> # cardinality constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t6 = Random_Regions(ids, cardinality=cards, permutations=2)
    >>> t6.solutions[0].regions[0]
    [37, 62]
    >>> # contiguity constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t7 = Random_Regions(ids, contiguity=w, permutations=2)
    >>> t7.solutions[0].regions[1]
    [62, 63, 54, 71]
    >>>

    """
    def __init__(self, area_ids, num_regions=None, cardinality=None, 
                    contiguity=None, maxiter=100, permutations=99):
        
        solutions = []
        for i in range(permutations):
            solutions.append(Random_Region(area_ids, num_regions, \
                    cardinality, contiguity, maxiter))
    
        self.solutions = solutions
        self.solutions_feas = []
        for i in solutions:
            if i.feasible == True:
                self.solutions_feas.append(i)


class Random_Region:
    """Randomly combine a given set of areas into two or more regions based 
    on various constraints.


    Parameters
    ----------

    area_ids        : list
                      IDs indexing the areas to be grouped into regions (must
                      be in the same order as spatial weights matrix if this
                      is provided)
                    
    num_regions     : integer
                      number of regions to generate (if None then this is 
                      chosen randomly from 2 to n where n is the number of 
                      areas)

    cardinality     : list
                      list containing the number of areas to assign to regions
                      (if num_regions is also provided then len(cardinality)
                      must equal num_regions; if cardinality=None then a list 
                      of length num_regions will be generated randomly)

    contiguity      : W
                      spatial weights object (if None then contiguity will be 
                      ignored)

    maxiter         : int
                      maximum number attempts at finding a feasible solution
                      (only affects contiguity constrained regions) 

    Attributes
    ----------
            
    feasible        : boolean
                      if True then solution was found
            
    regions         : list: 
                      list of lists of regions (each list has the ids of areas
                      in that region)

    Examples
    --------

    >>> import random
    >>> import numpy as np
    >>> nregs = 13
    >>> cards = range(2,14) + [10]
    >>> w = pysal.weights.weights.lat2gal(10,10,rook=False)
    >>> ids = w.id_order
    >>>
    >>> # unconstrained
    >>> random.seed(10)
    >>> np.random.seed(10)
    >>> t0 = Random_Region(ids)
    >>> t0.regions[0]
    [19, 14, 43, 37, 66, 3, 79, 41, 38, 68, 2, 1, 60]
    >>> # cardinality and contiguity constrained (num_regions implied)
    >>> random.seed(60)
    >>> np.random.seed(60)
    >>> t1 = Random_Region(ids, num_regions=nregs, cardinality=cards, contiguity=w)
    >>> t1.regions[0]
    [7, 18, 29, 17, 38, 48, 19, 28, 39, 37, 47, 36, 57]
    >>> # cardinality constrained (num_regions implied)
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t2 = Random_Region(ids, num_regions=nregs, cardinality=cards)
    >>> t2.regions[0]
    [37, 62]
    >>> # number of regions and contiguity constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t3 = Random_Region(ids, num_regions=nregs, contiguity=w)
    >>> t3.regions[1]
    [79, 68, 57, 89, 47, 98, 36, 56, 69, 58, 78, 26, 48]
    >>> # cardinality and contiguity constrained
    >>> random.seed(60)
    >>> np.random.seed(60)
    >>> t4 = Random_Region(ids, cardinality=cards, contiguity=w)
    >>> t4.regions[0]
    [7, 18, 29, 17, 38, 48, 19, 28, 39, 37, 47, 36, 57]
    >>> # number of regions constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t5 = Random_Region(ids, num_regions=nregs)
    >>> t5.regions[0]
    [37, 62, 26, 41, 35, 25, 36]
    >>> # cardinality constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t6 = Random_Region(ids, cardinality=cards)
    >>> t6.regions[0]
    [37, 62]
    >>> # contiguity constrained
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> t7 = Random_Region(ids, contiguity=w)
    >>> t7.regions[0]
    [37, 27, 38, 29]
    >>>

    """
    def __init__(self, area_ids, num_regions=None, cardinality=None, 
                    contiguity=None, maxiter=1000):
        
        self.n = len(area_ids)
        ids = copy.copy(area_ids)
        self.ids = list(np.random.permutation(ids))
        self.area_ids = area_ids
        self.regions = []
        self.feasible = True

        # tests for input argument consistency
        if cardinality:
            if self.n != sum(cardinality):
                self.feasible = False
                raise Exception, 'number of areas does not match cardinality'
        if contiguity:
            if area_ids != contiguity.id_order:
                self.feasible = False
                raise Exception, 'order of area_ids must match order in contiguity'
        if num_regions and cardinality:
            if num_regions != len(cardinality):
                self.feasible = False
                raise Exception, 'number of regions does not match cardinality'

        # dispatches the appropriate algorithm
        if num_regions and cardinality and contiguity:
            # conditioning on cardinality and contiguity (number of regions implied)
            self.build_contig_regions(num_regions, cardinality, contiguity, maxiter)
        elif num_regions and cardinality:
            # conditioning on cardinality (number of regions implied)
            region_breaks = self.cards2breaks(cardinality)
            self.build_noncontig_regions(num_regions, region_breaks)
        elif num_regions and contiguity:
            # conditioning on number of regions and contiguity
            cards = self.get_cards(num_regions)
            self.build_contig_regions(num_regions, cards, contiguity, maxiter)
        elif cardinality and contiguity:
            # conditioning on cardinality and contiguity
            num_regions = len(cardinality)
            self.build_contig_regions(num_regions, cardinality, contiguity, maxiter)
        elif num_regions:
            # conditioning on number of regions only
            region_breaks = self.get_region_breaks(num_regions)
            self.build_noncontig_regions(num_regions, region_breaks)
        elif cardinality:
            # conditioning on number of cardinality only
            num_regions = len(cardinality)
            region_breaks = self.cards2breaks(cardinality)
            self.build_noncontig_regions(num_regions, region_breaks)
        elif contiguity:
            # conditioning on number of contiguity only
            num_regions = self.get_num_regions()
            cards = self.get_cards(num_regions)
            self.build_contig_regions(num_regions, cards, contiguity, maxiter)
        else:
            # unconditioned
            num_regions = self.get_num_regions()
            region_breaks = self.get_region_breaks(num_regions)
            self.build_noncontig_regions(num_regions, region_breaks)

    def get_num_regions(self):
        return np.random.random_integers(2, self.n)

    def get_region_breaks(self, num_regions):
        region_breaks = set([])
        while len(region_breaks) < num_regions-1:
            region_breaks.add(np.random.random_integers(1, self.n-1))
        region_breaks = list(region_breaks)
        region_breaks.sort()
        return region_breaks

    def get_cards(self, num_regions):
        region_breaks = self.get_region_breaks(num_regions)
        cards = []
        start = 0
        for i in region_breaks:
            cards.append(i - start)
            start = i
        cards.append(self.n - start)
        return cards

    def cards2breaks(self, cards):
        region_breaks = []
        break_point = 0
        for i in cards:
            break_point += i
            region_breaks.append(break_point)
        region_breaks.pop()
        return region_breaks

    def build_noncontig_regions(self, num_regions, region_breaks):
        start = 0
        for i in region_breaks:
            self.regions.append(self.ids[start:i])
            start = i
        self.regions.append(self.ids[start:])

    def build_contig_regions(self, num_regions, cardinality, w, maxiter):
        iter = 0
        regions = []
        self.feasible = False
        while iter < maxiter:
            cards = copy.copy(cardinality)
            cards.sort()
            candidates = copy.copy(self.ids)
            seed_test = 0  # identifies when no feasible solution is possible
            while candidates and seed_test<num_regions-len(regions):
                # draw a seed and begin building a new region around it
                building = True
                seed = candidates.pop(0)
                region = [seed]
                potential = [i for i in w.neighbors[seed] if i in candidates]
                test_card = cards.pop()
                while building and len(region)<test_card:
                    # find neighbors for seed; try to build largest region first
                    if potential:
                        # keep trying to find potential neighbors
                        neigID = random.randint(0,len(potential)-1)
                        neigAdd = potential.pop(neigID)
                        region.append(neigAdd)
                        potential.extend([i for i in w.neighbors[neigAdd] \
                                            if i not in potential and \
                                               i not in region and \
                                               i in candidates])
                    else:
                        # not enough potential neighbors to reach test_card size
                        building = False
                        cards.append(test_card)
                        if len(region) in cards:
                            # constructed region matches another candidate region size
                            cards.remove(len(region))
                        else:
                            # constructed region doesn't match a candidate region size
                            # put seed back in the queue
                            candidates.append(seed)
                            region = []
                            seed_test += 1
                if region:
                    for i in region:
                        if i in candidates:
                            candidates.remove(i)
                    regions.append(region)
                    seed_test = 0
            if len(regions) < num_regions:
                # shuffle the ids and try again for a feasible solution
                self.ids = list(np.random.permutation(self.ids))
                regions = []
                iter += 1
            else:
                self.feasible = True
                iter = maxiter
        self.regions = regions

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

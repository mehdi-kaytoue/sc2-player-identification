
import time

from parser import replays2traces
from features import traces2features
from models import learn
import matplotlib.pyplot as plt

import numpy as np
import numpy.random

def main():

    #replays2traces("replay-data/Whitera_replay_pack/", 1000, 100, 5, "replay-traces.txt")

    maxseconds = [i for i in range(0, 101, 2)]
    minlabels = [j for j in range(0, 101, 2)]
    scores = []

    for i in maxseconds:
        traces2features("replay-traces.txt", "features-train.txt", i)
        row = []
        for j in minlabels:
            score = learn("features-train.txt", j)
            row += [score]
        scores.append(row)

    print(scores)

        #plt.clf()
        #plt.xlabel('Minimum number of games per player')
        #plt.ylabel('Classifier score ')
        #plt.ylim([0.0, 1.05])
        #plt.xlim([0.0, 100])
        #plt.title('Classifier score w.r.t. label count')
        #plt.legend(loc="lower left")
        #plt.plot(minlabels, scores, '-')
        #plt.show()


    plt.contourf(minlabels, maxseconds, scores) # Dim: i, j, ixj
    plt.colorbar()
    plt.xlabel('Minimum number of games per player')
    plt.ylabel('Max seconds taken into account')
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- Finished in " + str(int(time.time() - start_time)) + " seconds ---")

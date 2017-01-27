import time

from algos.TightFitWB import TightFitWB
from src.Groundplan import Groundplan


def best_res(res):
    bestone = None
    for r in res:
        if bestone is None or r[7] > bestone[7]:
            bestone = r
    return bestone


def perform_experiment(variables, frame):
    print "Performing all zoom tight experiments"

    MIN = 1.0
    MAX = 10.0
    INTERVAL = 0.5

    def find_best_params(num_houses, enable_playground, base, f, frame):

        if base == "gp": bas = Groundplan(num_houses, enable_playground).deepCopy()
        else: bas = base(num_houses=num_houses,enable_playground=enable_playground).develop_ground_plan().deepCopy()

        interval = INTERVAL
        i_min = MIN
        i_max = MAX
        j_min = MIN
        j_max = MAX
        k_min = MIN
        k_max = MAX

        res = []

        while True:
            results = res + []
            i = i_min
            while i_min <= i < i_max:
                j = j_min
                while j_min <= j < j_max:
                    k = k_min
                    while k_min <= k < k_max:
                        ti = time.time()
                        r = f(bas.deepCopy(), i, j, k, frame).getPlan().deepCopy()
                        print round((time.time() - ti) * 1000), 'plans per second'
                        v = r.getPlanValue() if r.isValid() else -1
                        results.append([num_houses, enable_pg, base, i, j, k, r, v])
                        k += interval
                    j += interval
                i += interval

            best = best_res(results)

            res.append(best)

            frame.repaint(best[6])

            i_ = best[3]
            j_ = best[4]
            k_ = best[5]

            i_min = max(MIN, i_ - interval * 2)
            i_max = min(MAX, i_ + interval * 2)
            j_min = max(MIN, j_ - interval * 2)
            j_max = min(MAX, j_ + interval * 2)
            k_min = max(MIN, k_ - interval * 2)
            k_max = min(MAX, k_ + interval * 2)
            interval *= 0.5
            if interval < 0.25:
                break

        overall_best = best_res(res)
        frame.repaint(overall_best[6])
        return overall_best

    allresults = []
    for num_houses in variables[0]:
        for enable_pg in variables[1]:
            for base in variables[2]:
                for f in variables[3]:
                    allresults.append(find_best_params(num_houses, enable_pg, base, f, frame))

    best = best_res(allresults)

    frame.repaint(best[6])

    return allresults


def construct_report(experiment):
    return experiment


def report(frame):
    experiment_variables = [
        [
            #40  # , #70,
            #70
         100
        ],
        [False],
        [  # base_dynamic.base_dynamic,#,
            # base_a.base_a#,
            # base_b.base_b#, base_c.base_c
            "gp"
        ],
        [  # validstate_tight
            #  ,
            # validstate_tight2
            TightFitWB
        ]
    ]
    return construct_report(perform_experiment(experiment_variables, frame))

import time

from src.Groundplan import Groundplan


def zoom(base, experiment, f, frame=None):
    # print 'zoom' , base.puts

    def best_res(res):
        bestone = None
        for r in res:
            if bestone is None or r[5] > bestone[5]: bestone = r
        return bestone

    def getmin(v):
        return max(p['min'], v - interval * 2)

    def getmax(v):
        return min(p['max'], v + interval * 2)

    t = time.time()

    p = experiment['constants']

    i_min = p['min']
    i_max = p['max']
    j_min = p['min']
    j_max = p['max']
    k_min = p['min']
    k_max = p['max']

    interval = p['interval']

    results = []

    while interval > p['min_interval']:
        i = i_min
        while i_min <= i < i_max:
            j = j_min
            while j_min <= j < j_max:
                k = k_min
                while k_min <= k < k_max:
                    r = f(base.deepCopy(), i, j, k, frame).getPlan()
                    v = 0
                    if isinstance(r, Groundplan):
                        r = r.deepCopy()
                        if r.isValid():
                            if frame is not None: frame.repaint(r)
                            v = r.getPlanValue()
                    results.append([base, i, j, k, r, v])
                    k += interval
                j += interval
            i += interval

        best = best_res(results)

        i_min = getmin(best[1])
        i_max = getmax(best[1])
        j_min = getmin(best[2])
        j_max = getmax(best[2])
        k_min = getmin(best[3])
        k_max = getmax(best[3])

        interval *= p['interval_shrink_factor']

    best = best_res(results)
    pt = time.time() - t

    if best is None:
        o = {'Plan': None, 'Value': 0, 'Processing time': pt, 'Params': {'base': base.name, 'algorithm': f}}
    else:
        o = {
            'Plan': best[4].serialize() if best[4] is not None else None,
            'Value': best[5],
            'Processing time': pt,
            'Parameters': {
                'familyhome_min_clearance': best[1],
                'bungalow_min_clearance': best[2],
                'mansion_min_clearance': best[3]
            }
        }

    return o

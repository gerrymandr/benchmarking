import numpy as np

#%% canonical form helper function
def canonical_form(plan_tuple):
    wrong = list(plan_tuple)
    seen = set()
    wrong_order = [d for d in wrong if not (d in seen or seen.add(d))]
    correct_order = list(range(1, len(wrong_order) + 1))
    correction_table = dict(zip(wrong_order, correct_order))
    right = [correction_table[d] for d in wrong]
    return tuple(right)

#%% parameter functions
# each parameter must take input of this form
def get_dem_seat_share(plan, dem_populations, rep_populations):
    plan = np.array(plan)
    num_districts = int(max(plan))
    seats = 0
    for d in range(1, num_districts + 1):
        dem_count = np.sum(dem_populations[plan == d])
        rep_count = np.sum(rep_populations[plan == d])
        if dem_count > rep_count:
            seats += 1
        # add half a seat in the case of a tie
        elif dem_count == 0 and rep_count == 0:
            seats += 0.5
    return seats

def entropy(plan, reps, dems):
    plan = np.array(plan)
    num_districts = int(max(plan))
    curr_entropy = 0
    for d in range(1, num_districts + 1):
        size = np.sum(plan == d)
        if size > 0:
            curr_entropy -= size * np.log(size)
    return curr_entropy
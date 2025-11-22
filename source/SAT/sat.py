from z3 import *
import json
import sys
import time
from pathlib import Path
import math
from itertools import combinations

def at_least_one_seq(bool_vars):
    return Or(bool_vars)

def at_most_one_seq(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    s = [Bool(f"s_{name}_{i}") for i in range(n - 1)]
    constraints.append(Or(Not(bool_vars[0]), s[0]))
    constraints.append(Or(Not(bool_vars[n-1]), Not(s[n-2])))
    for i in range(1, n - 1):
        constraints.append(Or(Not(bool_vars[i]), s[i]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i-1])))
        constraints.append(Or(Not(s[i-1]), s[i]))
    return And(constraints)

def exactly_one_seq(bool_vars, name):
    return And(at_least_one_seq(bool_vars), at_most_one_seq(bool_vars, name))

def at_least_k_seq(bool_vars, k, name):
    return at_most_k_seq([Not(var) for var in bool_vars], len(bool_vars)-k, name)

def at_most_k_seq(bool_vars, k, name):
    constraints = []
    n = len(bool_vars)
    s = [[Bool(f"s_{name}_{i}_{j}") for j in range(k)] for i in range(n - 1)]
    constraints.append(Or(Not(bool_vars[0]), s[0][0]))
    constraints += [Not(s[0][j]) for j in range(1, k)]
    for i in range(1, n-1):
        constraints.append(Or(Not(bool_vars[i]), s[i][0]))
        constraints.append(Or(Not(s[i-1][0]), s[i][0]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i-1][k-1])))
        for j in range(1, k):
            constraints.append(Or(Not(bool_vars[i]), Not(s[i-1][j-1]), s[i][j]))
            constraints.append(Or(Not(s[i-1][j]), s[i][j]))
    constraints.append(Or(Not(bool_vars[n-1]), Not(s[n-2][k-1])))
    return And(constraints)

def exactly_k_seq(bool_vars, k, name):
    return And(at_most_k_seq(bool_vars, k, name), at_least_k_seq(bool_vars, k, name))

def sports_tournament_schedule(n=6, timeout=300):
    
    # initialize variable from the data
    week = n - 1
    period = math.ceil(n / 2)
    slots = 2
    lower_bound = math.floor(week / 2)
    upper_bound = math.ceil((week / 2) + 1)

    total_games = week * period

    # creating 3d array for scedhule
    schedule = [[[Int(f's_{p}_{w}_{s}') for s in range(slots)] for w in range(week)] for p in range(period)]

    # creating z3 solver instance
    solver = Solver()
    solver.set("timeout", timeout * 1000)  # timeout in milliseconds

    # adding constraints
    for p in range(period):
        for w in range(week):
            # each slot should have one team assigned to it
            for s in range(slots):
                solver.add(And(schedule[p][w][s] >= 1, schedule[p][w][s] <= n))

            # no team plays against itself
            solver.add(schedule[p][w][0] != schedule[p][w][1])
                
                
    # each team play only once in a week
    for t in range(1, n + 1):
        for w in range(week):
            bool_vars = []
            for p in range(period):
                for s in range(slots):
                    bool_vars.append(schedule[p][w][s] == t)
            solver.add(exactly_one_seq(bool_vars, f"team_{t}_week_{w}"))

    # each team play each other only once in the tournament
    for t1 in range(1, n+1):
        for t2 in range(t1 + 1, n + 1):
            bool_vars = []
            for p in range(period):
                for w in range(week):
                    bool_vars.append(Or(And(schedule[p][w][0] == t1, schedule[p][w][1] == t2),
                                        And(schedule[p][w][0] == t2, schedule[p][w][1] == t1)))
            solver.add(exactly_one_seq(bool_vars, f"pair_{t1}_{t2}"))

    # no team play more than twice in the same period
    for t in range(1, n + 1):
        for p in range(period):
            bool_vars = []
            for w in range(week):
                for s in range(slots):
                    bool_vars.append(schedule[p][w][s] == t)
            solver.add(at_most_k_seq(bool_vars, 2, f"team_{t}_period_{p}"))
    
    # balance the number of home and away games for each team
    for t in range(1, n + 1):
        bool_vars = []
        for p in range(period):
            for w in range(week):
                bool_vars.append(schedule[p][w][0] == t)
        solver.add(at_least_k_seq(bool_vars, lower_bound, f"home_lower_team_{t}"))
        solver.add(at_most_k_seq(bool_vars, upper_bound, f"home_upper_team_{t}"))
    
    for t in range(1, n + 1):
        bool_vars = []
        for p in range(period):
            for w in range(week):
                bool_vars.append(schedule[p][w][1] == t)
        solver.add(at_least_k_seq(bool_vars, lower_bound, f"away_lower_team_{t}"))
        solver.add(at_most_k_seq(bool_vars, upper_bound, f"away_upper_team_{t}"))


    #  reduce symmetries
    for p in range(period):
        for w in range(1, 1):
            solver.add(schedule[p][w][0] < schedule[p][w][1])

    # solving the model

    start = time.time()
    result = solver.check()
    end = time.time() - start

    if result == sat:
        model = solver.model()
        
        # Extract solution in [periods][weeks][slots] format
        sol = []
        for p in range(period):
            period_data = []
            for w in range(week):
                game = [model.evaluate(schedule[p][w][s]).as_long() for s in range(2)]
                period_data.append(game)
            sol.append(period_data)
        
        return {
            'time': int(end),
            'optimal': True,
            'obj': None,
            'sol': sol
        }
    else:
        return {
            'time': 300,
            'optimal': False,
            'obj': None,
            'sol': []
        }
        


if __name__ == '__main__':
    n = int(sys.argv[1])
    
    print(f"Solving with SAT for n={n}...")
    result = sports_tournament_schedule(n)
    
    # Save
    output_dir = Path('../../res/SAT')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / f'{n}.json', 'w') as f:
        json.dump({'z3': result}, f, indent=2)
    
    print(f"Done: Solution found: {result['optimal']}, Time: {result['time']}s")
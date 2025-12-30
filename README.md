# CDMO Project - Sports Tournament Scheduling
The Sports tournament scheduling problem requires arranging n even teams so that each team plays every other team exactly once over W = n − 1 weeks. Each week contains P = n/2 periods. The challenge is to compute a feasible schedule satisfying structural fairness and operational constraints.

Practical constraints imposed include:
• every team plays exactly once per week;
• no team plays itself;
• every unordered pair of teams meets exactly once in the tournament;
• a team appears in a given period at most twice during the tournament;
• home/away games for each team are balanced.

The Sports tournament scheduling problem is combinatorial and known to be computationally challenging as n grows. Different modelling paradigms exploit different reasoning techniques:

Constraint Programming (CP): relies on finite-domain integer variables, global constraints (e.g. alldifferent), and propagation with search heuristics.
SMT encoding: The SMT encoding represents assignments using integer variables and enforces cardinality and structural constraints directly through the solver’s arithmetic and logical theories, avoiding the need for additional Boolean variables.
Mixed Integer Programming (MIP): models the problem with binary variables and linear constraints, often requiring auxiliary variables to linearise non linear constructs (e.g., pairwise match detection).

## Local Usage

### Requirements
- Python 3.8+
- MiniZinc
- Z3 (`pip install z3-solver`)
- PuLP (`pip install pulp`)

### Run All Experiments
```bash
python run_all.py
```

### Run Individual
```bash
python source/CP/run_cp.py
python source/SMT/smt.py {number_of_teams}
python source/MIP/mip.py {number_of_teams}
```

### Validate Results
```bash
python solution_checker.py res/CP
python solution_checker.py res/SMT
python solution_checker.py res/MIP
```

## Docker Usage

### Build
```bash
docker build -t cdmo-project .
```

### Run All

**Linux/macOS:**
```bash
docker run --rm -v $(pwd)/res:/app/res cdmo-project
```

**Windows (PowerShell):**
```powershell
docker run --rm -v ${PWD}/res:/app/res cdmo-project
```

### Run Individual
```bash
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/CP/run_cp.py
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/SMT/smt.py {number_of_teams}
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/MIP/mip.py {number_of_teams}
```

### Check Solutions

**Linux/macOS:**
```bash
docker run --rm -v $(pwd)/res:/app/res cdmo-project python3 solution_checker.py res/CP
docker run --rm -v $(pwd)/res:/app/res cdmo-project python3 solution_checker.py res/SMT
docker run --rm -v $(pwd)/res:/app/res cdmo-project python3 solution_checker.py res/MIP
```

**Windows (PowerShell):**
```powershell
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 solution_checker.py res/CP
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 solution_checker.py res/SMT
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 solution_checker.py res/MIP
```

## Results Format
- `res/CP/6.json`, `res/CP/8.json`, `res/CP/10.json`
- `res/SMT/6.json`, `res/SMT/8.json`, `res/SMT/10.json`
- `res/MIP/6.json`, `res/MIP/8.json`, `res/MIP/10.json`

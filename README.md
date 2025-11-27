# CDMO Project - Sports Tournament Scheduling

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
python source/SMT/smt.py
python source/MIP/mip.py
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

**Windows (CMD):**
```cmd
docker run --rm -v %cd%/res:/app/res cdmo-project
```

### Run Individual
```bash
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/CP/run_cp.py
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/SMT/smt.py
docker run --rm -v ${PWD}/res:/app/res cdmo-project python3 source/MIP/mip.py
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

**Windows (CMD):**
```cmd
docker run --rm -v %cd%/res:/app/res cdmo-project python3 solution_checker.py res/CP
docker run --rm -v %cd%/res:/app/res cdmo-project python3 solution_checker.py res/SMT
docker run --rm -v %cd%/res:/app/res cdmo-project python3 solution_checker.py res/MIP
```

## Results Format
- `res/CP/6.json`, `res/CP/8.json`, `res/CP/10.json`
- `res/SMT/6.json`, `res/SMT/8.json`, `res/SMT/10.json`
- `res/MIP/6.json`, `res/MIP/8.json`, `res/MIP/10.json`
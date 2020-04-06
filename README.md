# CS3243 Project 2
Ivan, Jun Wei, Ze Chu, Larry
## CSP and Reinforcement Learning
### Problem Specification
1. Variable: Every cell in 9x9 matrix.
2. Domain: Every cell, 1-9
3. Constraint
   1. For each col and row, Alldif must be satisfied
   2. (KIV) Unary constraint for starting puzzle

### Variant
1. Variable ordering
   1. Most Constrained Variable
   2. Most Constraining Variable
2. Value Ordering
   1. Least Constraining Value
3. Inference Mechanism
   1. AC3
   2. Forward Checking

TODO:
1. Experiment
    - Plot time taken against number of empty cells (for randomly generated puzzles)
    - Histogram (frequency against time)
2. Variants
    - at least 2 variants that has justifications
    - Shift AC3 forward
    - Clarify most constraining value
3. Justification for variant
4. Beat benchmark 

## Pacman
TODO
1. Bug for 1 test case
2. Feature extractor

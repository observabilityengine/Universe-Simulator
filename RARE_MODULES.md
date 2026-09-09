# Rare Complex Modules (20)

## quantum/ (5)
- qubit.py – Multi-qubit state vector, measurement, Z expectation
- gates.py – H/X/Z/S/T single-qubit gates + CNOT
- circuit.py – Circuit builder; Bell-state demo
- qft.py – Quantum Fourier Transform
- vqe.py – Variational Quantum Eigensolver

## formal/ (5)
- sat_solver.py – DPLL SAT with unit propagation
- model_checker.py – CTL EF/AG model checking
- temporal_logic.py – LTL on finite traces (X/F/G/U)
- smt_simple.py – Linear integer arithmetic bound propagation
- hoare_logic.py – Hoare triple weakest-precondition checker

## compress/ (4)
- huffman.py – Huffman coding encode/decode
- lz77.py – LZ77 sliding-window compression
- arithmetic_coding.py – Arithmetic coding core
- ans.py – Asymmetric Numeral Systems (rANS)

## consensus/ (3)
- raft.py – Raft leader election + log replication
- paxos.py – Single-decree Paxos
- byzantine.py – Oral messages Byzantine broadcast

## symbolic/ (3)
- expression.py – Symbolic expression trees + evaluation
- differentiate.py – Symbolic differentiation
- simplify.py – Algebraic simplification rules

All modules are pure Python, self-testing, and production-structured.

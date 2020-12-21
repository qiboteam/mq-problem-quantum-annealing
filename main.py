#!/usr/bin/env python
from sympy import symbols
import numpy as np
import functions
import argparse


def main(bits, T, chainstrength, numruns, dwave, greedy, inspect, repeat, iterations):
    """Adiabatic evolution for nonlinear functions.

    Args:
        bits (int): Number of bits of the example.
        T (float): Total annealing time.
        chainstrength (float): Chainstrangth for device. Leave None if calculated automatically.
        numruns (int): Number of samples to take from quantum computer.
        dwave (Bool): run everything on dwave.
        greedy (Bool): process results using the greedy algorithm.
        inspect (Bool): Open the dwave inspector.
        repeat (Bool): Fix ancillas using repetition.
        iterations (int): number of repetitions for the ancilla fixing.

    -------------- if minimization is run via dwave -------------------
    Returns:
        best_sample (list): bit positions of the best found solution.
        best_energy (float): energy value associated to the found minimum.
        
    """
    x = symbols(' '.join((f'x{i}' for i in range(1, bits+1))))
    if bits == 3:
        ancillas = (symbols(' '.join((f'xa{i}' for i in range(1, 2)))), )
        f = functions.f_3(*x)
        r = functions.r_3()
    elif bits == 8:
        ancillas = symbols(' '.join((f'xa{i}' for i in range(1, 23))))
        f = functions.f_8(*x)
        r = functions.r_8()
    else:
        raise ValueError('Only instances for 3 and 8 bits are supported.\n')
        
    sym = x+ancillas
    symbol_num = {}
    for i in range(len(sym)):
        symbol_num[sym[i]] = i
    print(f'Solving a {bits} bit instance of a nonlinear function using Adiabatic Evolution.\n')
    print('Creating problem Hamiltonian.\n')
    h = functions.to_hamiltonian(f, r, sym)
    terms = functions.check_interactions(h)
    print('Number of terms for each k-body interactions.\n')
    print(terms, '\n')
    print('Reducing the k-body interactions using ancillas.\n')
    h2, anc = functions.to_gadget_ruge2(h, sym, ancillas, bits, control)
    terms = functions.check_interactions(h2, high=False)
    print(f'Total number of qubits needed for the 2-local hamiltonian encoding {bits} bits: {anc+bits}.\n')
    print('Number of terms for each k-body interactions after gadget aplication.\n')
    print(terms, '\n')
    
    if dwave:
        best_sample, best_energy = dwave(h2, symbol_num, bits, T, chainstrength, numruns, greedy, inspect, repeat, iterations)
        return best_sample, best_energy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", default=3, type=int)
    parser.add_argument("--T", default=20, type=float)
    parser.add_argument("--chainstrength", default=None, type=float)
    parser.add_argument("--numruns", default=500, type=int)
    parser.add_argument("--dwave", action="store_true")
    parser.add_argument("--greedy", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--repeat", action="store_true")
    parser.add_argument("--iterations", default=5, type=int)
    args = vars(parser.parse_args())
    main(**args)

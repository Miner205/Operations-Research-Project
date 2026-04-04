# Operations Research Project
Solving transportation problems

# int2 - Our Team - Group 1 :
Arthur Donnat
Arthur Delannoy
Raphaël Lesterlin
Jude Guehl
Indiko

# GitHub link :
https://github.com/Miner205/Operations-Research-Project

# Project specification :
- Transportation Problems: only balanced case.
- txt format : ...
- ...

# ToDo :
- Transportation Problem: Display tables (..., Potential costs table, Marginal costs table) ,...
- Solve TP : find the best way of transporting objects from suppliers to customers that minimizes
the total cost of transport. /!\ Only balanced case.
    - Algorithm for setting the initial proposal : North-West.
    - Algorithm for setting the initial proposal : Balas-Hammer.
        - Calculation of penalties.
        - Display of row(s) (or columns) with the maximum penalty.
        - Choice of edge to fill.
    - Solving algorithm : the stepping-stone method with potential.
        - Test whether the proposition is acyclic : we’ll use a Breadth-first algorithm.
        - etc. -> cf pdf consignes.
- Main while loop -> cf "Overall structure" Part in pdf consignes.
- pseudo-code of functions & slides (for Oral presentation of 10min).
- Report 'on complexity' // "Study of complexity" -> cf pdf consignes.
- Execution traces -> cf "Execution traces" Part in pdf consignes.

# Functionalities done :
- Transportation Problem: load TP (Read data), save TP, display matrix/tables(Cost matrix, Transportation proposal, ...)
    - Total cost calculation for a given transport proposal. 
- ...

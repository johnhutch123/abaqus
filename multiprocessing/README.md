This script shows how the multiprocessing module within python can be used to parallise FEA jobs within Abaqus.

The script takes sequentially numbered abaqus input files and creates a pool. New jobs from the pool are run as CPUs are made avaialbe.

# Quadratic Assignment Problem

author: George Nunes de Moura Filho, 

Computer Engineering Student at Federal University of Paraiba (UFPB), João Pessoa, Brazil.

e-mail: georgenmoura@gmail.com

This code contains a GRASP solution with VND implementation of the Quadratic Assignment Problem [NP-Hard], made just for fun. The input is given by 2 text files, each one contains an adjacency matrix, wich correspond to the locations and facilities. The files should be in the following format:

```
(number_of_nodes)
0 0 0 0 0...
0 0 0 0 0...
0 0 0 0 0...
0 0 0 0 0...
....
```

### exemple:
```
3
0 4 7
4 0 5
7 5 0
```

The program output is a good solution, with no guarantee of being optmal.

# instance Generator

This code generates new random graph instances for multiple problems, based on magic values 

Defines the range of the matrix values
```
init_matrix_element_range
final_matrix_element_range
```

Defines the start size of the graphs
```
matrix_size_initializer
```

Defines the number of groups of instances who's going to be generated, each group contains one or more instances
```
number_of_groups
```

The number os instances per group
```
number_of_instances
```

Make the graphs undirected
```
undirected
```

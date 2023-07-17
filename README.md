# PedigreeProfiler

**Pedigree Profiler**
- This project presents an object-oriented approach to pedigree analysis in Python. The code implements two classes, Individual and Pedigree, which are used to represent a pedigree (a family tree) and perform various analyses.

**Key Features**
- Individuals: Individuals are the basic building blocks of the pedigree, represented by an Individual object. Each individual can have a mother, father, and list of children. They also have an affected status, which can be used to track whether the individual has a specific trait or condition.
- Pedigrees: The Pedigree object represents a family tree, consisting of a list of Individual objects. It provides functionality to find affected and unaffected individuals, determine possible modes of inheritance, and visualize the pedigree.

**Analyses**
- The Pedigree class provides three main analysis methods:
  - find_affected(): Returns a list of all affected individuals in the pedigree.
  - find_unaffected(): Returns a list of all unaffected individuals in the pedigree.
  - find_mode_of_inheritance(): Determines the potential mode of inheritance for a trait within the pedigree. It evaluates four possible modes of    inheritance: 'Autosomal Dominant', 'Autosomal Recessive', 'X-Linked Dominant', and 'X-Linked Recessive'.

**Visualization**
- The Pedigree class also provides a method to visualize the pedigree with Matplotlib. Each individual in the pedigree is represented as a shape: males are represented by circles and females by squares. Affected individuals are colored black, while unaffected individuals are white.

**Usage**
- The project provides example usages of the classes with a set of test pedigrees. These tests demonstrate the construction of Individual and Pedigree objects, as well as the execution of the analysis and visualization methods.
- This project can serve as a starting point for more complex pedigree analysis tasks or as an educational tool for learning about inheritance patterns in genetics.

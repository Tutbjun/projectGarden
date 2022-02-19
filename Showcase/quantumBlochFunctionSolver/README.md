# quantumBlochFunctionSolver

This is a project for solving 1D bloch functions in crystal lattices so that a coloumb-based potential model can be evaluated against the kronig-penney squarewave model. This was made as a tool to solve the main problem in my high school thesis. For the same reason, it was developed with a tight deadline, and the code is therefor not that "pretty". It has been quickly put into seperate classes for the sake of structuring, but there are still many functions that are far longer than they need to be, and in general, this project has a lot of potential for improvement and generalization.

From the definition of bloch functions, there can be derived a crystal cell wave of an electron. This wave are made with two parts that are scaled by A and B (complex constants), and the main contraint on this wave is that the function and its derivate is equivalent in the start and end of the unit cell. The wave frequency is also dependant on the energy and momentum of the electron. The aproach therefore is to first set an E (energy). Then there will be performed a sweep across k values with A and B equal to 1, where the cell border function values will be stored. Then, by scaling A and B in a linear equation system, there will be found all posible k values that make the function and derivate contraint be withheld. This will result in all values of k in the given energy that makes a true result. Lastly, the E/k values will be exported for plotting in fx Excel.

There are though some issues with unit scaling, and all method should be critically asseses before using this project for anything more important. Especially the regression across the k sweep i suspected to have precission issues.

To run script:
run main.py from any directory. Result will get stored as a csv file in the directory of choice. 
The Python version used is 3.9.7 through a miniconda virtual environment
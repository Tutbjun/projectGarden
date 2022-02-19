# contourRenderer

This project is a method for generating a point inside of a mesh of sorts. The motives where as follows:
* To try and solve an algorithmic/mathematical problem without any outside help
* To get experienced in programming modern c++

In the current state, the program will generate a (simplified) random 2D mesh, and then mark a couple of thousands of points inside it. The concept is that it does this by slicing the mesh into triangles, where it then produces transformations to unit squares. Then an inverse transformation of this kind can be used to go from a cartesian coordinate inside the unit square, into the sliced triangle. By a area-wieghted average there can be choose between the sliced triangles to truly produce a random point. It utilizes a simplified mesh, as it is generated in a way where there will never apear more than one face in a line from origo. The plan was to make this simplification unnecessary by implementing a more sofisticated slicing algorithm, but that hasn't yet been completed. These concepts are also generalizable to 3D, but that too hasn't been completed yet.

Also, since this was my first "proper" programming experience in c++, the code probably does not follow certain conventions

To compile code:
./compile.bat

To run code:
start pointInMesh.exe

pointInMesh.exe will the generate the result in plot1.png
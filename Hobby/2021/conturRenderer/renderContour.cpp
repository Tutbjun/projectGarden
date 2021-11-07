#include <vector>
#include "pointInMesh_Lib/pointInMesh.h"
using namespace std;

const int itterations = 5;

class Grid : vector<vector<vector<float>>>{
    public:
        Grid(){}
        Grid(float divission){
            vector<vector<float>> gridCell = {{0,0},{1,0},{0,1},{1,1}};
            //gridCell *= divission
            //grid out the grid
            //for gridCount self.pushback(gridCell)
        }
};

class RenderGrid{
    public:
        Grid innerGrid;
        Grid outerGrid;
        Grid edgeGrid;

        void categorize_grid(Grid grid, smartMesh mesh){
            //edgeGrid = emtpy
            // for e in grid
                //is all of e in mesh
                //if yes
                    //pushback on innerGrid
                //if no
                    //pushback on outerGrid
                //if not all of e in mesh
                    //pushback on edgeGrid
            return;
        }
        Grid subdivide_grid(Grid grid){
            Grid newgrid;
            // for e in grid
                //pushback four corners of e to newgrid
            return newgrid;
        }
};



Grid get_edgeGrid(){
    return;
}

int main(){
    const int verticieCount = 5;
    smartMesh m = rawMesh(2,verticieCount);
    float divission = 1/10;
    Grid grid(divission);
    RenderGrid rGrid;
    rGrid.categorize_grid(grid, m);
    for (int i = 0; i < itterations; i++){
        rGrid.edgeGrid = rGrid.subdivide_grid(rGrid.edgeGrid);
        rGrid.categorize_grid(rGrid.edgeGrid, m);
    }


    return 0;
}
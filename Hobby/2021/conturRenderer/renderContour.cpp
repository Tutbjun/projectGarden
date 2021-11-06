#include <vector>
using namespace std;

const int itterations = 5;

class Grid : vector<vector<vector<float>>>{

};

class RenderGrid{
    public:
        Grid innerGrid;
        Grid outerGrid;
        Grid edgeGrid;

        void categorize_grid(Grid grid){
            return;
        }
        Grid subdivide_grid(Grid grid){
            return;
        }
};

Grid get_startingGridSet(){
    return;
}

Grid get_edgeGrid(){
    return;
}

int main(){
    Grid grid = get_startingGridSet();
    RenderGrid rGrid;
    rGrid.categorize_grid(grid);
    for (int i = 0; i < itterations; i++){
        rGrid.edgeGrid = rGrid.subdivide_grid(rGrid.edgeGrid);
        rGrid.categorize_grid(rGrid.edgeGrid);
    }


    return 0;
}
//TODO: ensure libraries are correctly formatted

#include  <vector>
#include "pointInMesh_Lib/pointInMesh.h"
#include "pointInMesh_Lib/plottin/meshPlotter.h"

using namespace std;

int main() {
    srand(randSeed);
    const int verticieCount = 5;
    smartMesh m = rawMesh(dims,verticieCount);
    plotMesh(m, "plot1.png");
    vector<vector<float>> points;
    for (int i = 0; i < 10000; i++){
        vector<float> point = m.pickRandomPoint();
        points.push_back(point);
        //print(m.isPointInMesh(point));
    }
    plotMesh(m, points, "plot1.png");
    return 0;
}
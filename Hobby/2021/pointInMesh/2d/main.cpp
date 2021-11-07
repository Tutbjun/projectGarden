#include  <vector>
#include "thirdPartyLibs/pbPlots.hpp"
#include "thirdPartyLibs/supportLib.hpp"
#include "pointInMesh_Lib/pointInMesh.h"
//#include "pointInMesh_Lib/utils.h"

using namespace std;

void plotMesh(vector<vector<float>> verts, vector<vector<int>> faces, vector<vector<int>> triangles, double minx, double miny, double maxx, double maxy, vector<vector<float>> points, string file){
    RGBABitmapImageReference *imageRef = CreateRGBABitmapImageReference();
    vector<double> xs;
    vector<double> ys;
    for (int i = 0; i < verts.size(); i++){
        xs.push_back(verts[i][0]);
        ys.push_back(verts[i][1]);
    }
    xs.push_back(minx);
    ys.push_back(miny);
    xs.push_back(maxx);
    ys.push_back(maxy);

    ScatterPlotSeries *serVerts = GetDefaultScatterPlotSeriesSettings();
	serVerts->xs = &xs;
	serVerts->ys = &ys;
	serVerts->linearInterpolation = false;
	serVerts->pointType = toVector(L"dots");
	serVerts->color = CreateRGBColor(1, 0, 0);

    ScatterPlotSeries *serPoint = GetDefaultScatterPlotSeriesSettings();
    vector<vector<double>> pxs;
    vector<vector<double>> pys;
    vector<double> x;
    vector<double> y;
    for (int i = 0; i < points.size(); i++){
        x.push_back(points[i][0]);
        y.push_back(points[i][1]);
    }
    pxs.push_back(x);
    pys.push_back(y);
	serPoint->xs = &x;
	serPoint->ys = &y;
	serPoint->linearInterpolation = false;
	serPoint->pointType = toVector(L"crosses");
	serPoint->color = CreateRGBColor(0, 0, 0);

    ScatterPlotSettings *settings = GetDefaultScatterPlotSettings();
	settings->width = 1200;
	settings->height = 800;
	settings->autoBoundaries = true;
	settings->autoPadding = true;
	settings->title = toVector(L"");
	settings->xLabel = toVector(L"");
	settings->yLabel = toVector(L"");
	settings->scatterPlotSeries->push_back(serVerts);
    settings->scatterPlotSeries->push_back(serPoint);

    DrawScatterPlotFromSettings(imageRef,settings);

    for (int i = 0; i < triangles.size(); i++){
        for (int j = 0; j < 3; j++){
            int jp = j + 1;
            if (jp >= 3)
                jp -= 3;
            double x1 = MapXCoordinateAutoSettings(verts[triangles[i][j]][0], imageRef->image, &xs);
            double y1 = MapYCoordinateAutoSettings(verts[triangles[i][j]][1], imageRef->image, &ys);
            double x2 = MapXCoordinateAutoSettings(verts[triangles[i][jp]][0], imageRef->image, &xs);
            double y2 = MapYCoordinateAutoSettings(verts[triangles[i][jp]][1], imageRef->image, &ys);
            DrawLine(imageRef->image,x1,y1,x2,y2,1,CreateRGBColor(0,1,0));
        }
    }

    for (int i = 0; i < faces.size(); i++){
        double x1 = MapXCoordinateAutoSettings(verts[faces[i][0]][0], imageRef->image, &xs);
        double y1 = MapYCoordinateAutoSettings(verts[faces[i][0]][1], imageRef->image, &ys);
        double x2 = MapXCoordinateAutoSettings(verts[faces[i][1]][0], imageRef->image, &xs);
        double y2 = MapYCoordinateAutoSettings(verts[faces[i][1]][1], imageRef->image, &ys);
        DrawLine(imageRef->image,x1,y1,x2,y2,1.5,CreateRGBAColor(1,0,0,0.3));
    }

    vector<double> *pngData = ConvertToPNG(imageRef->image);
    WriteToFile(pngData,file);
    DeleteImage(imageRef->image);
}

void plotMesh(rawMesh mesh, vector<vector<float>> points, string file){
    vector<vector<int>> triangles;
    return plotMesh(mesh.verts, mesh.faces, triangles, 0, 0, 1, 1, points, file);
}

void plotMesh(rawMesh mesh, vector<float> point, string file){
    vector<vector<float>> points;
    points.push_back(point);
    return plotMesh(mesh, points, file);
}
void plotMesh(meshPointRandomizer mesh, vector<float> point, string file){
    vector<vector<float>> points;
    points.push_back(point);
    return plotMesh(mesh, points, file);
}
void plotMesh(meshPointRandomizer mesh, vector<vector<float>> points, string file){
    return plotMesh(mesh.verts, mesh.faces, mesh.triangles, 0, 0, 1, 1, points, file);
}
void plotMesh(meshPointRandomizer mesh, string file){
    vector<vector<float>> points = {{0,0}};
    return plotMesh(mesh.verts, mesh.faces, mesh.triangles, 0, 0, 1, 1, points, file);
}

int main() {
    srand(randSeed);
    const int verticieCount = 5;
    meshPointRandomizer m = rawMesh(dims,verticieCount);
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
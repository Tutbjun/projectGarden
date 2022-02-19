#include "pbPlots.hpp"
#include "supportLib.hpp"
#include <vector>

void plotMesh(std::vector<std::vector<float>> verts, std::vector<std::vector<int>> faces, std::vector<std::vector<int>> triangles, double minx, double miny, double maxx, double maxy, std::vector<std::vector<float>> points, std::string file){
    RGBABitmapImageReference *imageRef = CreateRGBABitmapImageReference();
    std::vector<double> xs;
    std::vector<double> ys;
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
    std::vector<std::vector<double>> pxs;
    std::vector<std::vector<double>> pys;
    std::vector<double> x;
    std::vector<double> y;
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

    std::vector<double> *pngData = ConvertToPNG(imageRef->image);
    WriteToFile(pngData,file);
    DeleteImage(imageRef->image);
}

void plotMesh(rawMesh mesh, std::vector<std::vector<float>> points, std::string file){
    std::vector<std::vector<int>> triangles;
    return plotMesh(mesh.verts, mesh.faces, triangles, 0, 0, 1, 1, points, file);
}

void plotMesh(rawMesh mesh, std::vector<float> point, std::string file){
    std::vector<std::vector<float>> points;
    points.push_back(point);
    return plotMesh(mesh, points, file);
}
void plotMesh(smartMesh mesh, std::vector<float> point, std::string file){
    std::vector<std::vector<float>> points;
    points.push_back(point);
    return plotMesh(mesh, points, file);
}
void plotMesh(smartMesh mesh, std::vector<std::vector<float>> points, std::string file){
    return plotMesh(mesh.verts, mesh.faces, mesh.triangles, 0, 0, 1, 1, points, file);
}
void plotMesh(smartMesh mesh, std::string file){
    std::vector<std::vector<float>> points = {{0,0}};
    return plotMesh(mesh.verts, mesh.faces, mesh.triangles, 0, 0, 1, 1, points, file);
}
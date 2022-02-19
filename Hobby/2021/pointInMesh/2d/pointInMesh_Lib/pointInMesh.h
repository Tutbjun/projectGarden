#include "utils.h"
#include <vector>

int dims = 2;

class rawMesh{
    public:
        std::vector<std::vector<float>> verts;
        std::vector<std::vector<int>> faces;
        rawMesh(){}
        rawMesh(std::vector<std::vector<float>> vertexList, std::vector<std::vector<int>> faceList)//imports mesh
        {
            verts = vertexList;
            faces = faceList;
        }
        rawMesh(int dimensions, int vertCount)//generates randomized circular mesh
        {
            float angleSpacing = twoPi/vertCount;
            for (int i = 0; i < vertCount; i++){
                std::vector<float> emptyF;
                std::vector<int> emptyI;
                verts.push_back(emptyF);
                faces.push_back(emptyI);
                float theta = i * angleSpacing + randF(-angleSpacing/2,angleSpacing/2);
                float r = 0.25 + randF(-0.2,0.2);
                verts[i].push_back(cos(theta)*r);
                verts[i][0] += 0.5;
                verts[i].push_back(sin(theta)*r);
                verts[i][1] += 0.5;
                for (int j = 0; j < dimensions; j++){
                    int index = i+j;
                    if (index >= vertCount)
                        index -= vertCount;
                    faces[i].push_back(index);
                }
            }
        }
};

class smartMesh : public rawMesh{
    private:
        bool transformsGenerated = false;
        bool divsGenerated = false;
        std::vector<float> triangleAreas;
        float triangleAreasSum;
        std::vector<std::vector<float>> triShifts;
        std::vector<std::vector<std::vector<float>>> triangleNRotMatricies;
        std::vector<std::vector<std::vector<float>>> invTriangleNRotMatricies;
        void genTransforms(){
            for (int i = 0; i < triangles.size(); i++){
                //shift transform
                triShifts.push_back(verts[triangles[i][0]]);

                //squeue transform
                std::vector<std::vector<float>> targetVecs;
                targetVecs.push_back(subtractVectors(verts[triangles[i][1]],verts[triangles[i][0]]));
                targetVecs.push_back(subtractVectors(verts[triangles[i][2]],verts[triangles[i][0]]));
                std::vector<std::vector<float>> matrix = matMatMul(transpose(targetVecs),{{1,0},{-1,1}});
                triangleNRotMatricies.push_back(matrix);
                invTriangleNRotMatricies.push_back(invMatrix(matrix));

                //triangle area weight finder
                float a = vectorLength(targetVecs[0]);
                float b = vectorLength(targetVecs[1]);
                float triAngle = vectorAngle(targetVecs[0],targetVecs[1]);
                float A = 0.5f*a*b*sin(triAngle);
                triangleAreas.push_back(A);
            }
            triangleAreasSum = sum(triangleAreas);
            transformsGenerated = true;
        }
        void dividePolygon(std::vector<std::vector<float>> lverts, std::vector<std::vector<int>> lfaces){
            bool divisionSucces = false;
            for (int cornerToStart = 0; cornerToStart < lverts.size(); cornerToStart++){
                for (int otherCorner = (cornerToStart + lverts.size()/2) % lverts.size(); otherCorner != cornerToStart; otherCorner = (otherCorner+1)%lverts.size()){
                    std::vector<std::vector<float>> splitverts1;
                    std::vector<std::vector<int>> splitfaces1;
                    std::vector<std::vector<float>> splitverts2;
                    std::vector<std::vector<int>> splitfaces2;
                    ///define splitverts
                    //check if any of the faces er facing wrong way
                    //if not, divisionSucces = True, double break
                }
            }
            if (divisionSucces){
                //if len of faces are over 3, use dividePolygon()
                
            }
        }

        void genDivs(){
            std::vector<float> origin;
            //origin.push_back(0.5);origin.push_back(0.5);
            //verts.push_back(origin);

            //divide figure up into smaller figures until sidecount is 3
            //meanwhile discard figures where any faces are outside faces
            



            origin = verts[0];
            for (int i = 0; i < faces.size(); i++){
                std::vector<int> emptyI;
                triangles.push_back(emptyI);
                triangles[i].push_back(faces[i][0]);
                triangles[i].push_back(faces[i][1]);
                triangles[i].push_back(verts.size()-1);
            }
            divsGenerated = true;
        }
        std::vector<float> cart2Triangle(std::vector<float> inPoint, int transformSet){
            if (inPoint[0] > inPoint[1])
                std::swap(inPoint[0],inPoint[1]);
            inPoint = vecMatMul(triangleNRotMatricies[transformSet],inPoint);//rotate and scale to desired spot
            inPoint = addVectors(inPoint,triShifts[transformSet]);
            return inPoint;
        }
        std::vector<float> triangle2cart(std::vector<float> inPoint, int transformSet){
            inPoint = subtractVectors(inPoint,triShifts[transformSet]);
            inPoint = vecMatMul(invTriangleNRotMatricies[transformSet],inPoint);//de-rotate and de-scale to desired spot
            return inPoint;
        }
        void checkPreps(){
            if (divsGenerated == false)
                genDivs();
            if (transformsGenerated == false)
                genTransforms();
        }
    public:
        std::vector<std::vector<int>> triangles;
        smartMesh(rawMesh mesh){
            verts = mesh.verts;
            faces = mesh.faces;
        }
        bool isPointInMesh(std::vector<float> inPoint){
            checkPreps();
            for (int i = 0; i < triangles.size(); i++){
                std::vector<float> cartPoint = triangle2cart(inPoint,i);
                if ((cartPoint[0] <= 1 && cartPoint[0] >= 0) && (cartPoint[1] <= 1 && cartPoint[1] >= 0)){
                    return true;
                }
            }
            return false;
        }
        std::vector<float> pickRandomPoint(){
            checkPreps();
            
            std::vector<float> randCartPoint;
            randCartPoint.push_back(randF());randCartPoint.push_back(randF());

            int pickedTriangle = randIFromWeightedList(triangleAreas,triangleAreasSum);
            std::vector<float> point = cart2Triangle(randCartPoint,pickedTriangle);
            return point;
        }
};
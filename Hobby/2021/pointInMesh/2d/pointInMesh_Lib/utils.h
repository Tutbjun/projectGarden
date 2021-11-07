#include <iostream>
#include <vector>
#include <chrono>
#include <string>
#include <random>
#include <numbers>

const float Pi = std::numbers::pi;
const float halfPi = Pi/2;
const float twoPi = Pi*2;
std::chrono::system_clock::time_point tp = std::chrono::system_clock::now();
const long long int randSeed = tp.time_since_epoch().count();
std::random_device rd;

int randI(int min,int max){
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> uni(min,max);
    return (int)uni(rng);
}
float randF(float start, float stop){
    return start + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(stop-start)));
}
float randF(float stop){
    return static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/stop));
}
float randF(){
    return static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
}
int randIFromWeightedList(std::vector<float> weightedList, float sumOfList){
    float val = randF(sumOfList);
    int index = 0;
    for (int i = 0; i < weightedList.size(); i++){
        val -= weightedList[i];
        if (val <= 0){
            index = i;
            break;
        }
    }
    return index;
}
float cosTaylor(float x,int n){
    switch(n){
        case 0:
            return 1;
        case 1:
            return -pow(x,2)/2;
        case 2:
            return pow(x,4)/24;
        case 3:
            return -pow(x,6)/720;
        case 4:
            return pow(x,8)/40320;
        case 5:
            return -pow(x,10)/3628800;
        case 6:
            return pow(x,12)/479001600;
        default:
            return 0;
    }
}

float abs(float x){
    long I = * ( long * ) &x;
    I &= ~(1UL << 31);//abs(x)
    x = * ( float * ) &I;
    return x;
}

float cos(float x, int accuracy){
    x = abs(x);

    float cycles = x/(halfPi);
    double dummy;
    float cycleDec = modf(cycles,&dummy);
    x = halfPi*cycleDec;

    int cycle = int(cycles)+1;
    if (cycle % 2 == 0)
        x-=halfPi;
    
    float val = 0;
    for (int i = 0; i < accuracy; i++)
        val += cosTaylor(x,i);

    int wholeCycles = (cycle+2) >> 1;
    if (wholeCycles % 2 == 0)
        val = -val;
    return val;
}
float cos(float in){
    return cos(in, 6);
}
float sin(float in, int accuracy){
    return cos(in-halfPi,accuracy);
}
float sin(float in){
    return cos(in-halfPi);
}
float tan(float in, int accuracy){
    return sin(in, accuracy)/cos(in, accuracy);
}
float tan(float in){
    return sin(in)/cos(in);
}
std::vector<float> addVectors(std::vector<float> v1,std::vector<float> v2){
    std::vector<float> result;
    for (int i = 0; i < v1.size(); i++){
        result.push_back(v1[i]+v2[i]);
    }
    return result;
}
std::vector<float> subtractVectors(std::vector<float> v1,std::vector<float> v2){
    for (int i = 0; i < v2.size(); i++){
        v2[i] = -v2[i];
    }
    return addVectors(v1,v2);
}
std::vector<float> subtractVectors(float val1,std::vector<float> v2){
    std::vector<float> v1;
    for (int i = 0; i < v2.size(); i++)
        v1.push_back(val1);
    return subtractVectors(v1,v2);
}
std::vector<float> multiplyVector(std::vector<float> v1,float val){
    std::vector<float> res;
    for (int i = 0; i < v1.size(); i++){
        res.push_back(v1[i]*val);
    }
    return res;
}
std::vector<std::vector<float>> multiplyVector(std::vector<std::vector<float>> m1,float val){
    std::vector<std::vector<float>> res = m1;
    for (int i = 0; i < m1.size(); i++){
        res[i] = multiplyVector(m1[i],val);
    }
    return res;
}
std::vector<float> divideVector(std::vector<float> v1,float val){
    return multiplyVector(v1,1/val);
}
float sum(std::vector<float> v){
    while (v.size() > 1){
        v[1] += v[0];
        std::vector<float> newV;
        for (int i = 1; i < v.size(); i++){
            newV.push_back(v[i]);
        }
        v = newV;
    }
    return v[0];
}
float dotProduct(std::vector<float> v1, std::vector<float> v2){
    float val = 0;
    for (int i = 0; i < v1.size(); i++)
        val += v1[i]*v2[i];
    return val;
}
std::vector<float> vecMatMul(std::vector<std::vector<float>> m, std::vector<float> v){
    std::vector<float> result = v;
    for (int i = 0; i < result.size(); i++)
        result[i] = dotProduct(v,m[i]);
    return result;
}
std::vector<std::vector<float>> vecMatMul(std::vector<std::vector<float>> m, std::vector<std::vector<float>> vs){
    std::vector<std::vector<float>> results = vs;
    for (int i = 0; i < results.size(); i++)
        results[i] = vecMatMul(m,vs[i]);
    return results;
}
std::vector<std::vector<float>> getGausJordanInvMatrix(std::vector<std::vector<float>> m){
    std::vector<std::vector<float>> im(m.size());
    std::vector<float> emptyRow(m[0].size());
    for (int i = 0; i < im.size(); i++){
        im[i] = emptyRow;
        im[i][i] = 1;
    }
    for (int step = 0; step < m[0].size(); step++){
        float val = m[step][step];
        m[step] = divideVector(m[step],val);
        im[step] = divideVector(im[step],val);
        for (int row = 0; row < m.size(); row++){
            if (row != step){
                std::vector<float> mVecToRem = multiplyVector(m[step],m[row][step]);
                std::vector<float> imVecToRem = multiplyVector(im[step],m[row][step]);
                m[row] = subtractVectors(m[row],mVecToRem);
                im[row] = subtractVectors(im[row],imVecToRem);
            }
        }
    }
    return im;
}
std::vector<std::vector<float>> invMatrix(std::vector<std::vector<float>> m){
    return getGausJordanInvMatrix(m);
}
float vectorLength(std::vector<float> v){
    return sqrtf(powf(v[0],2)+powf(v[1],2));
}
float vectorAngle(std::vector<float> v1, std::vector<float> v2){
    return acosf(dotProduct(v1,v2)/(vectorLength(v1)*vectorLength(v2)));
}
std::vector<std::vector<float>> transpose(std::vector<std::vector<float>> m){
    std::vector<std::vector<float>> result;
    std::vector<float> empty;
    for (int i = 0; i < m[0].size(); i++){
        result.push_back(empty);
        for (int j = 0; j < m.size(); j++){
            result[i].push_back(m[j][i]);
        }
    }
    return result;
}

std::vector<std::vector<float>> matMatMul(std::vector<std::vector<float>> m1, std::vector<std::vector<float>> m2){
    std::vector<std::vector<float>> result;
    std::vector<std::vector<float>> m2T = transpose(m2);
    std::vector<float> empty;
    for (int i = 0; i < m1.size(); i++){
        result.push_back(empty);
        for (int j = 0; j < m2T.size(); j++){
            result[i].push_back(dotProduct(m1[i],m2T[j]));
        }
    }
    return result;
}

void print(std::string in){
    std::cout << '\n';
    std::cout << in << ' ';
}
void print(float in){
    print(std::to_string(in));
}
void print(std::vector<float> in){
    for (float e : in)
        print(e);
}
void print(std::vector<std::vector<float>> in){
    in = transpose(in);
    for (std::vector<float> v : in)
        print(v);
}

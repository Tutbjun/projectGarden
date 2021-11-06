#include <vector>
#include <random>
#include <iostream>
#include <string>
using namespace std;


void print(string in){
    std::cout << in << ' ';
}
void print(float in){
    print(to_string(in));
}
void print(vector<float> in){
    print("\n");
    for (float e : in)
        print(e);
}
void print(vector<vector<float>> in){
    for (vector<float> v : in)
        print(v);
}

float randF(){
    return static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
}

float dotProduct(vector<float> v1, vector<float> v2){
    float val = 0;
    for (int i = 0; i < v1.size(); i++)
        val += v1[i]*v2[i];
    return val;
}

vector<vector<float>> transpose(vector<vector<float>> m){
    vector<vector<float>> result;
    vector<float> empty;
    for (int i = 0; i < m[0].size(); i++){
        result.push_back(empty);
        for (int j = 0; j < m.size(); j++){
            result[i].push_back(m[j][i]);
        }
    }
    return result;
}

vector<vector<float>> matMatMul(vector<vector<float>> m1, vector<vector<float>> m2){
    vector<vector<float>> result;
    vector<vector<float>> m1T = transpose(m1);
    vector<vector<float>> m2T = transpose(m2);
    vector<float> empty;
    for (int i = 0; i < m1.size(); i++){
        result.push_back(empty);
        for (int j = 0; j < m2T.size(); j++){
            result[i].push_back(dotProduct(m1[i],m2T[j]));
        }
    }
    return result;
}

int main(){
    vector<vector<float>> m;
    vector<float> empty;
    for (int i = 0; i < 2; i++){
        m.push_back(empty);
        for (int j = 0; j < 2; j++){
            m[i].push_back(randF());
        }
    }
    vector<vector<float>> mT = transpose(m);
    print(m);
    print(mT);
    print(matMatMul(mT,m));

    return 0;
}
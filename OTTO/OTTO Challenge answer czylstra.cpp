//Clearpath Robotics OTTO Challenge
//Written by Chris Zylstra. September 2021
//https://clearpathrobotics.com/blog/2020/01/humans-of-clearpath-co-op-edition/


#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

//calculates the distance between two points. returns seconds because OTTO moves at 2m/s
double pythag(double a, double b, double c, double d){
    return sqrt(abs((a-b)*(a-b))+abs((c-d)*(c-d)))/2;
}

vector <double> time_arr;

int main(){
    int s;
    cin >> s;

    if (s == 0){
        for (int i = 0; i < time_arr.size(); i++) cout << time_arr[i] << endl;
        return 0;
    }
    
    double time, x[s+2], y[s+2], penalty[s+2], last_len;

    //initialize the x/y of the endpoints.
    x[0] = 0;
    x[s+1] = 100;
    y[0] = 0;
    y[s+1] = 100;

    //take in the data
    for (int i = 1; i < s+1; i++) cin >> x[i] >> y[i] >> penalty[i]; 

    //logic to calculate if skipping the point and incurring the penalty is better than routing to it.
    for (int i = 0; i < s; i++){
        double var1 = pythag(x[i],x[i+2],y[i],y[i+2]); //length if skip the next point
        double var2 = pythag(x[i],x[i+1],y[i],y[i+1]); //length a
        double var3 = pythag(x[i+1],x[i+2],y[i+1],y[i+2]); //length b

        if ((var1 + penalty[i+1]) < (var2 + var3 + 10)){
            time+=var1+penalty[i+1];
            last_len = 0;
            i++; //extra loop iteration to skip the next point.
        }
        else{
            time += var2+10;
            last_len = var3;
        }
    }
    
    time += last_len+10;
    time = round (time * 1000.0) / 1000.0;
    time_arr.push_back(time);
    main();
}        


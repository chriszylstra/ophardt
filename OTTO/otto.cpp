//Hello World cpp

#include <iostream>
#include <math.h>

using namespace std;

double calculate(double a, double b, double c, double d){
    double ans = 0;
    ans = abs((a-b)*(a-b))+abs((c-d)*(c-d));
    return sqrt(ans);
}

void print(int x[], int size){
    for (int i = 0; i < size+2; i++){
        cout << x[i] << " ";
    }
    cout << endl;
}

double sum(double x[], int size){
    double a = 0;
    for (int i = 0; i <size+1; i++){
        a+= x[i];
    }
    return a/2;
 }

double results[] = {0};

int main(){
    int s;
    double time = 0;
    cin >> s;
    if (s == 0){
        return 0;
    }

    double x[s+2] = {};
    double y[s+2] = {};
    double penalty[s+2] = {};
    x[0] = 0;
    x[s+1] = 100;
    y[0] = 0;
    y[s+1] = 100;
    penalty[0] = 0;
    penalty[s+1] = 10;

    for (int i = 1; i < s+1; i++){
        cin >> x[i] >> y[i] >> penalty[i]; 
    }
    for (int i = 0; i < s+1; i++){

        //special case - skip the point and incur the penalty. 
        if (true){
            cout << x[i] << " " << x[i+2] << " " << y[i] << " " << y[i+2] << endl;
            results[i] = calculate(x[i-1],x[i+1],y[i-1],y[i+1]);
            time += penalty[i];
        }
        //normal case - hit each point
        else{
            results[i] = calculate(x[i],x[i+1],y[i],y[i+1]);
            time += 10;
        }
    }
    time += sum(results, s);
    cout << "Time: " << time << endl;
    
    main();
    

}        


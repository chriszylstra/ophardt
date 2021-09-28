#include <iostream>
#include <math.h>
using namespace std;

double calculate(double a, double b, double c, double d){
    double ans = abs((a-b)*(a-b))+abs((c-d)*(c-d));
    return (sqrt(ans))/2;
}

int main(){
    int s;
    cin >> s;
    if (s == 0) return 0;
    double time = 0;
    double x[s+2] = {};
    double y[s+2] = {};
    double penalty[s+2] = {};
    x[0] = 0;
    x[s+1] = 100;
    y[0] = 0;
    y[s+1] = 100;
    for (int i = 1; i < s+1; i++){
        cin >> x[i] >> y[i] >> penalty[i]; 
    }
    double last_len = 0;
    for (int i = 0; i < s; i++){
        double var1 = calculate(x[i],x[i+2],y[i],y[i+2]); //full length skipping
        double var2 = calculate(x[i],x[i+1],y[i],y[i+1]); //length a
        double var3 = calculate(x[i+1],x[i+2],y[i+1],y[i+2]); //length b
        if ((var1 + penalty[i+1]) < (var2 + var3 + 10)){
            time+=var1+penalty[i+1];
            last_len = 0;
            i++;
        }
        else{
            time += var2+10;
            last_len = var3;
        }
    }
    time+=last_len+10;
    time = round (time * 1000.0) / 1000.0;
    cout << time << endl;
    main();
}        


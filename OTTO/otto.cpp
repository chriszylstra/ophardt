//Hello World cpp

#include <iostream>
#include <math.h>

using namespace std;

double calculate(double a, double b, double c, double d){
    double ans = 0;
    ans = abs((a-c)*(a-c))+abs((b-d)*(b-d));
    return sqrt(ans);
}

int main(){
    int s;
    double len[s+1] = {0};
    double result = 0;
    do
    {
        cin >> s;
        //cout << "s: " << s << endl;
        double datapoints[s+2][3] = {0};
        datapoints[0][0] = 0;
        datapoints[0][1] = 0;
        datapoints[0][2] = 0;
        datapoints[s+1][0] = 100;
        datapoints[s+1][1] = 100;
        datapoints[s+1][2] = 10;

        for (int i = 1; i<s+1; i++){
            cin >> datapoints[i][0] >> datapoints[i][1] >> datapoints[i][2]; 
            len[i-1] = calculate(datapoints[i-1][0], datapoints[i-1][1], datapoints[i][0], datapoints[i][1]);
            cout << "Length: " << len[i-1] << endl;
        }
       len[s] = calculate(datapoints[s][0], datapoints[s][1], datapoints[s+1][0], datapoints[s+1][1]);
       for (int i = 0; i < sizeof(len); i++){
            result += len[i];
            len[i] = 0;
       }
       cout << "Total length: " << result << endl; 
        result = 0;

       

    } while (s != 0);

}        


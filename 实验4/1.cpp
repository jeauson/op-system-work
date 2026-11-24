#include<iostream>
using namespace std;
int page_size,v_max,phz,ins;
int t=0;
int main(){
cin>>v_max>>page_size>>phz>>ins;
int v_size=v_max/page_size;
int v_table[50];
int table[50][3];
for(int i=0;i<50;i++){
    table[i][0]=v_table[i]=-1;
    table[i][1]=table[i][2]=0;
}
}

void create(int *p){
    int a=0;
    *p=a;


}


int fifo(int v_table[],int table[][3],int *p,int *t){
    int m=0;
    bool load=false;
    m=*p/page_size;
    ++*t;
    if(v_table[m]==-1){
        for(int i=0;i<phz;i++){
            if(table[i][0]==-1){
                table[i][0]=m;
                v_table[m]=i;
                table[i][1]=table[i][2]=*t;
                load=true;
                break;
            }
        }
        if(!load){
            int min=table[0][1];
            int index=0;
            for(int i=1;i<phz;i++){
                if(table[i][1]<min){
                    min=table[i][1];
                    index=i;
                }
            }
            v_table[table[index][0]]=-1;
            table[index][0]=m;
            v_table[m]=index;
            table[index][1]=table[index][2]=*t;
            load=true;
        }
    }
    else{
        return 0;
    }
    return 1;
}




//void lre(){}



//void opt(){}




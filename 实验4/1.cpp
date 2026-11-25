#include<iostream>
using namespace std;
int page_size//页面大小
,v_max//虚拟地址空间大小
,phz//物理页框数量
,ins;//指令数量

int t=0;//全局时间
//声明
void create(int *p);
int fifo(int v_table[], int table[][3], int n, int *ref, int *t);
int lru (int v_table[], int table[][3], int n, int *ref, int *t);
int opt (int v_table[], int table[][3], int n, int *ref, int *t);
int main(){
cout<<"虚拟地址空间大小："<<endl;
cin>>v_max;
cout<<"页面大小："<<endl;
cin>>page_size;
cout<<"物理页帧数："<<endl;
cin>>phz;
cout<<"指令数量："<<endl;
cin>>ins;
int v_size=v_max/page_size;//虚拟页表数
int v_table[50];
int table[50][3];
for(int i=0;i<50;i++){
    table[i][0]=v_table[i]=-1;
    table[i][1]=table[i][2]=0;
}
int p[800];
int fault=0;
int sign=0;//算法选择标志
create(p);
while(true){
cout<<"选择一个算法：0-FIFO;1-LRU;2-OPT"<<endl;
cin>>sign;
switch(sign)
{
    case 0:
    for(int i=0;i<ins;i++){
        fault+=fifo(v_table,table,i,p,&t);
    }
    break;
    case 1:
    for(int i=0;i<ins;i++){
        fault+=lru(v_table,table,i,p,&t);
    }
    break;
    case 2:
    for(int i=0;i<ins;i++){
        fault+=opt(v_table,table,i,p,&t);
    }
    break;
    default:
    cout<<"非法输入,请重新输入"<<endl;
    continue;

}
break;
}
float ret=(float)fault/ins;
cout<<"缺页率为："<<ret<<endl;
}





void create(int *p){
   int first=rand()%v_max;
    for(int i=0;i<ins;i++){
        int s=rand()%100;
        p[i]=first;
        if(s<50){
            first=(first+1)%v_max;
        }
        else if(s<75){
            first=rand()%v_max/2;
        }
        else{
            first=rand()%v_max/2+v_max/2;
        }
    }
}


int fifo(int v_table[],int table[][3],int n,int *ref,int *t){
    //p:虚拟地址查找
    int m=0;
    bool load=false;
    m=ref[n]/page_size;//虚拟地址页号
    ++*t;
    if(v_table[m]==-1){//未命中物理地址空缺
        for(int i=0;i<phz;i++){
            if(table[i][0]==-1){
                table[i][0]=m;
                v_table[m]=i;
                table[i][1]=table[i][2]=*t;
                load=true;
                break;
            }
        }
        if(!load){//未命中物理地址满载
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
    else{//命中
        table[v_table[m]][2]=*t;
        return 0;
    }
    return 1;
}




int lru(int v_table[],int table[][3],int n,int *ref,int *t){
    int m=0;
    bool load=false;
    m=ref[n]/page_size;//虚拟地址页号
    ++*t;
    if(v_table[m]==-1){//未命中物理地址空缺
        for(int i=0;i<phz;i++){
            if(table[i][0]==-1){
                table[i][0]=m;
                v_table[m]=i;
                table[i][1]=table[i][2]=*t;
                load=true;
                break;
            }
        }
        if(!load){//未命中物理地址满载
            int min=table[0][1];
            int index=0;
            for(int i=1;i<phz;i++){
                if(table[i][2]<min){
                    min=table[i][2];
                    index=i;
                }
            }
            //表格更新
            v_table[table[index][0]]=-1;
            table[index][0]=m;
            v_table[m]=index;
            table[index][1]=table[index][2]=*t;
            load=true;
        }
    }
    else{//命中
        table[v_table[m]][2]=*t;
        return 0;
    }
    return 1;
}
    
//ref：指令序列表
//n:当前指令序列号
int opt(int v_table[],int table[][3],int n,int *ref,int*t){
    int m=0;
    bool load=false;
    m=ref[n]/page_size;//虚拟地址页号
    ++*t;
    int index=0;//置换页号索引
    if(v_table[m]==-1){//未命中物理地址空缺
        for(int i=0;i<phz;i++){
            if(table[i][0]==-1){
                table[i][0]=m;
                v_table[m]=i;
                table[i][1]=table[i][2]=*t;
                load=true;
                break;
            }
        }
        if(!load){//未命中物理地址满载
            int cur[]={-1,-1};
            int far[]={-1,-1};
            for(int i=0;i<phz;i++){
                 bool find=false;
                for(int j=n+1;j<ins;j++){
                   
                    if(ref[j]/page_size==table[i][0]){
                            cur[0]=i;
                            cur[1]=j;
                            find=true;
                            break;
                    }
                }
                if(!find){
                    index=i;
                    break;
                }
                if(cur[1]>far[1]){
                    far[0]=cur[0];
                    far[1]=cur[1];
                    index=i;
                }
            }
            //根据索引置换
            v_table[table[index][0]]=-1;
            table[index][0]=m;
            v_table[m]=index;
            table[index][1]=table[index][2]=*t;
            load=true;
        }
    }
    else{//命中
        table[v_table[m]][2]=*t;
        return 0;
    }
    return 1;
}




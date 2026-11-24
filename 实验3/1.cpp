#include<iostream>
using namespace std;
#define max_p 10
#define max_s 10
int p,s;
int ava[max_s+1];
int max_need[max_p+1][max_s+1];
int all[max_p+1][max_s+1];
int need[max_p+1][max_s+1];
int safe[max_p+1];
int work[max_s+1];
int cnt=0;
bool finish[max_p+1]={false};


void init(){
for(int i=1;i<=s;i++)
	cin>>ava[i];
for(int i=1;i<=p;i++)
	for(int j=1;j<=s;j++)
	cin>>max_need[i][j];
for(int i=1;i<=p;i++)
	for(int j=1;j<=s;j++)
	{cin>>all[i][j];	
    need[i][j]=max_need[i][j]-all[i][j];	
}
for(int j=1;j<=s;j++)
	work[j]=ava[j];
}


//--------------------------------------------------------//

bool issafe(){
	bool progress=true;
	for(int j=1;j<=s;j++) work[j]=ava[j];   
    for(int i=1;i<=p;i++) finish[i]=false; 
	cnt=0;
while(progress){
progress=false;
for(int i=1;i<=p;i++){
	if (finish[i]) continue;
	bool test=true;
		for(int j=1;j<=s;j++){
			if(need [i][j]>work[j]){
		 		test=false;
				break;
			}	
	
		}	
	if(test){
		for(int j=1;j<=s;j++){
			work[j]+=all[i][j];
		}
			finish[i]=true;
			progress=true;
			safe[cnt]=i;
			cnt++;
			
	}		
}		
}
return cnt==p;
}


//----------------------------------------------------------//
bool request(){
	int req_p,req_s[max_s+1];
	cout<<"进程号:"<<endl;
	cin>>req_p;
	cout<<"申请资源数:"<<endl;
	for(int i=1;i<=s;i++){
		cin>>req_s[i];
	}
	for(int i=1;i<=s;i++){
		if(req_s[i]>need[req_p][i]){
			cout <<"请求不合理"<< endl;
			return false;
		}
		if(req_s[i]>ava[i]){
			cout<<"资源不足"<<endl;
			return false;
		}
	
	}
		for(int  i=1;i<=s;i++){
			ava[i]-=req_s[i];
			need[req_p][i]-=req_s[i];
			all[req_p][i]+=req_s[i];

		}
	
	if(issafe()){
		cout<<"申请成功:"<<endl;
		return true;
	}
		for(int i=1;i<=s;i++){
			ava[i]+=req_s[i];
			need[req_p][i]+=req_s[i];
			all[req_p][i]-=req_s[i];
	}
	cout<<"申请失败，系统将进入不安全状态:"<<endl;
	return false;
}


//-------------------------------------------------------//


int main(){
	cin>>p>>s;
	init();
	if(!issafe()){
		cout<<"system is not safe"<<endl;
	return 0;
	}
	cout<<"初始安全序列: ";
	for(int j=0;j<p;j++) 
	cout<<safe[j]<<endl;
 	cout<<endl;
	while(true){
	if(request()){
		cout<<"system safe number:"<<endl;
		for(int j=0;j<p;j++)
			cout<<safe[j]<<endl;
	}		
	cout<<"是否继续申请资源?1=是,0=否"<<endl;
	int again;
	cin>>again;
	if(!again)break;
	}
	return 0;
}
//------------------------------------------------------//
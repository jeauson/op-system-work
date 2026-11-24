#define _GNU_SOURCE
#include<unistd.h>
#include<stdio.h>
#include<errno.h>
#include<string.h>
int main(void){
int n[]={0,2,-3};
for(int i=0;i<=2;i++){
long result=0;
long r=syscall(462,n[i],&result);
if(r==-1)
printf("%s\n",strerror(errno));
else 
printf("n=%d,ret=%ld,expect%ld,\n",n[i],result,(long)n[i]*n[i]*n[i]);
}
}

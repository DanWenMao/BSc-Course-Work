/*
AI USAGE STATEMENT
Deepseek_V3 helped polish the code, which has been pointed out in the annotation, and find the error.
*/

#include<mpi.h>
#include<stdio.h>

#define N 1024

int main(int argc,char* argv[]){
    int myrank,np,src,dest,tag;
    double A[N],B[N],SUM=0;
    MPI_Status status;   // Deepseek_V3 recommended
    MPI_Request request_send,request_recv;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
    MPI_Comm_size(MPI_COMM_WORLD,&np);

    for (int i=0;i<N;i++){
        A[i]=myrank;
    }
    src=myrank-1;
    if(src<0){
        src=np-1;
    }
    dest=myrank+1;
    if(dest>np-1){
        dest=0;
    }

    tag=111;

    if(np==1){
        MPI_Irecv(B,N,MPI_DOUBLE,src,tag,MPI_COMM_WORLD,&request_recv);
        MPI_Isend(A,N,MPI_DOUBLE,dest,tag,MPI_COMM_WORLD,&request_send);
        MPI_Wait(&request_recv,&status);
        MPI_Wait(&request_send,&status); 
        /*Deepseek_V3: “MPI标准不允许进程通过常规 Send/Recv 与自身通信（除非使用 MPI_PROC_NULL 或特殊方法）。
        当进程尝试 MPI_Send 给自己时，会阻塞等待 MPI_Recv，但 MPI_Recv 也在等待 MPI_Send → 死锁。”
        一般情况下，似乎在编译时会优化dest==src的情况；但学校服务器暂时不能使用，本地的WSL虚拟机似乎不支持优化；因此采用了MPI_Irecv/Isend。
        */
    }
    else if(myrank%2==0){
        MPI_Send(A,N,MPI_DOUBLE,dest,tag,MPI_COMM_WORLD);
        MPI_Recv(B,N,MPI_DOUBLE,src,tag,MPI_COMM_WORLD,&status);
    }else{
        MPI_Recv(B,N,MPI_DOUBLE,src,tag,MPI_COMM_WORLD,&status);
        MPI_Send(A,N,MPI_DOUBLE,dest,tag,MPI_COMM_WORLD);
    }

    for(int i=0;i<N;i++){
        SUM+=B[i];
    }
    printf("Process %d:%lf\n",myrank,SUM/N);

    MPI_Finalize();
    return 0;
}
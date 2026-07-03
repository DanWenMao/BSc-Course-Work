#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "mpi.h"

#define N 1024

int int_pow(int b, int e) {
    int result=1;
    for (int i=0; i<e; i++) {
        result*=b;
    }
    return result;
}

int main(int argc,char *argv[]){
    int rank,np,n;
    double start,end;
    int Message[N];
    MPI_Status status;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&np);

    if(rank==0){
        srand(time(0));
        for(int i=0;i<N;i++){
            Message[i]=rand()%100;
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    if(rank==0){
        start=MPI_Wtime();
    }
    for(n=0;int_pow(2,n+1)<np;n++){
        //printf("%d\n",n);
        if(rank<int_pow(2,n)){
            MPI_Send(Message,N,MPI_INT,rank+int_pow(2,n),n,MPI_COMM_WORLD);
        }
        if(rank>=int_pow(2,n)&&rank<int_pow(2,n+1)){
            MPI_Recv(Message,N,MPI_INT,rank-int_pow(2,n),n,MPI_COMM_WORLD,&status);
            printf("Rank %d received data from Rank %d, the first data %d\n",rank,rank-int_pow(2,n),Message[0]);
        }
    }
    if(rank<np-int_pow(2,n)){
        MPI_Send(Message,N,MPI_INT,rank+int_pow(2,n),n,MPI_COMM_WORLD);
    }
    if(rank>=int_pow(2,n)){
        MPI_Recv(Message,N,MPI_INT,rank-int_pow(2,n),n,MPI_COMM_WORLD,&status);
        printf("Rank %d received data from Rank %d, the first data %d\n",rank,rank-int_pow(2,n),Message[0]);
    }
    MPI_Barrier(MPI_COMM_WORLD);
    if(rank==0){
        end=MPI_Wtime();
        printf("Point to Point:%f\n",end-start);
    }

    if(rank==0){
        start=MPI_Wtime();
    }
    MPI_Bcast(Message,N,MPI_INT,0,MPI_COMM_WORLD);
    if(rank==0){
        end=MPI_Wtime();
        printf("Bcast:%f\n",end-start);
    }
    
    MPI_Finalize();
    return 0;
}

/*
测试输出结果

Rank 1 received data from Rank 0, the first data 89
Rank 2 received data from Rank 0, the first data 89
Rank 3 received data from Rank 1, the first data 89
Rank 4 received data from Rank 0, the first data 89
Rank 5 received data from Rank 1, the first data 89
Rank 6 received data from Rank 2, the first data 89
Rank 7 received data from Rank 3, the first data 89
Rank 8 received data from Rank 0, the first data 89
Rank 9 received data from Rank 1, the first data 89
Point to Point:0.006521
Bcast:0.000191

是因为输出缓冲区被阻塞了吗？没有按照一般的顺序输出。
*/
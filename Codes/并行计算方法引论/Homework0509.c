#include <stdio.h>
#include <mpi.h>
#include <time.h>
#include <stdlib.h>

#define N 4

// 实现将矩阵A的对角元素传递给矩阵B的对角元素
// 仅在同一进程内传递，扩展为不同进程之间，这是容易实现的，参考之前作业逻辑即可
int main(int argc,char *argv[]){
    
    int **A,**B;
    int *A_temp,*B_temp;
    int np,myrank,dest=0,src=0;
    MPI_Datatype type1;
    MPI_Status status;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
    MPI_Comm_size(MPI_COMM_WORLD,&np);

    A_temp=(int*)malloc(N*N*sizeof(int));
    A=(int**)malloc(N*sizeof(int*));
    for(int i=0;i<N;i++){
        A[i]=A_temp+N*i;
    }

    B_temp=(int*)malloc(N*N*sizeof(int));
    B=(int**)malloc(N*sizeof(int*));
    for(int i=0;i<N;i++){
        B[i]=B_temp+N*i;
    }

    srand(time(NULL)*myrank);
    printf("A:\n");
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            A[i][j]=rand()%100;
            printf("%d\t",A[i][j]);
        }
        printf("\n");
    }
    printf("B (init):\n");
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            B[i][j]=0;
            printf("%d\t",B[i][j]);
        }
        printf("\n");
    }

    MPI_Type_vector(N,1,N+1,MPI_INT,&type1);
    MPI_Type_commit(&type1);

    MPI_Sendrecv(A_temp,1,type1,dest,111,
                B_temp,1,type1,src,111,
                MPI_COMM_WORLD,&status);

    printf("B (set):\n");
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            printf("%d\t",B[i][j]);
        }
        printf("\n");
    }

    free(A);
    free(B);
    free(A_temp);
    free(B_temp);
    MPI_Type_free(&type1);
    MPI_Finalize();

    return 0;
}

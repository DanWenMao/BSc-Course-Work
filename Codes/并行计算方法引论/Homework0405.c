/*
AI USAGE STATEMENT
Deepseek_V3 helped polish the code, which has been pointed out in the annotation, and find the error.
*/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include "mpi.h"

#define M 1024
#define N 1024
#define L 1024

void Matrix_Multi_ijk(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int m1,int m2);
void Matrix_Multi_jik(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int n1,int n2);
void Matrix_Multi_ikj(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int m1,int m2);

int main(int argc,char *argv[])
{
    // initialize
    int rank,np,length,remainder,start_row,end_row;
    double start,end;
    float A[M][N]={0},B[N][L]={0},C[M][L]={0};
    FILE *file=NULL;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&np);

    if(rank==0){
        srand(time(0));
        for(int i=0;i<M;i++){
            for(int j=0;j<N;j++){
                A[i][j]=rand()%100;
            }
        }
        for(int i=0;i<N;i++){
            for(int j=0;j<L;j++){
                B[i][j]=rand()%100;
            }
        }

        file = fopen("result.txt", "w");
        if (file == NULL) {
            printf("无法打开文件！\n");
            MPI_Abort(MPI_COMM_WORLD, 1);   // Deepseek_V3 recommended
            return 1;
        }
    }
    MPI_Bcast(A, M * N, MPI_FLOAT, 0, MPI_COMM_WORLD);  // Deepseek_V3 recommended
    MPI_Bcast(B, N * L, MPI_FLOAT, 0, MPI_COMM_WORLD);  // Deepseek_V3 recommended


    // i-j-k cycle
    length=M/np;
    remainder=M%np;
    start_row=(rank<remainder)?(rank*(length+1)):(rank*length+remainder);
    end_row=(rank<remainder)?((rank+1)*(length+1)):((rank+1)*length+remainder);

    MPI_Barrier(MPI_COMM_WORLD);
    start=MPI_Wtime();
    Matrix_Multi_ijk(A,B,C,start_row,end_row);
    MPI_Barrier(MPI_COMM_WORLD);
    end=MPI_Wtime();

    if (rank==0){
        fprintf(file,"i-j-k cycle:%fs\n",end-start);
    }

    memset(C, 0, sizeof(float)*M*L); // Deepseek_V3 recommended

    // j-i-k cycle
    length=N/np;
    remainder=N%np;
    start_row=(rank<remainder)?(rank*(length+1)):(rank*length+remainder);
    end_row=(rank<remainder)?((rank+1)*(length+1)):((rank+1)*length+remainder);

    MPI_Barrier(MPI_COMM_WORLD);
    start=MPI_Wtime();
    Matrix_Multi_jik(A,B,C,start_row,end_row);
    MPI_Barrier(MPI_COMM_WORLD);
    end=MPI_Wtime();
    
    if (rank==0){
        fprintf(file,"j-i-k cycle:%fs\n",end-start);
    }

    memset(C, 0, sizeof(float)*M*L); // Deepseek_V3 recommended

    // i-k-j cycle
    length=M/np;
    remainder=M%np;
    start_row=(rank<remainder)?(rank*(length+1)):(rank*length+remainder);
    end_row=(rank<remainder)?((rank+1)*(length+1)):((rank+1)*length+remainder);

    MPI_Barrier(MPI_COMM_WORLD);
    start=MPI_Wtime();
    Matrix_Multi_ikj(A,B,C,start_row,end_row);
    MPI_Barrier(MPI_COMM_WORLD);
    end=MPI_Wtime();
    
    if (rank==0){
        fprintf(file,"i-k-j cycle:%fs\n",end-start);
        fclose(file);
    }


    MPI_Finalize();
    return 0;
}

void Matrix_Multi_ijk(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int m1,int m2)
{
    int i,j,k;

    for(i=m1;i<m2;i++){
        for(j=0;j<L;j++){
            for(k=0;k<N;k++){
                Matrix_res[i][j]=Matrix_res[i][j]+Matrix_a[i][k]*Matrix_b[k][j];
            }
        }
    }
}

void Matrix_Multi_jik(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int n1,int n2)
{
    int i,j,k;

    for(j=n1;j<n2;j++){
        for(i=0;i<M;i++){
            for(k=0;k<N;k++){
                Matrix_res[i][j]=Matrix_res[i][j]+Matrix_a[i][k]*Matrix_b[k][j];
            }
        }
    }
}

void Matrix_Multi_ikj(float (*Matrix_a)[N], float (*Matrix_b)[L], float (*Matrix_res)[L], int m1,int m2)
{
    int i,j,k;

    for(i=m1;i<m2;i++){
        for(k=0;k<N;k++){
            for(j=0;j<L;j++){
                Matrix_res[i][j]=Matrix_res[i][j]+Matrix_a[i][k]*Matrix_b[k][j];
            }
        }
    }
}
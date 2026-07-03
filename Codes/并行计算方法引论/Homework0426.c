/*
测试1
命令行：mpirun -np 8 test 4K
输出：
The circular algorithm: wall time=0.000142
MPI_Allgather:          wall time=0.000066
Tree_Allgather:         wall time=0.000197

测试2
命令行：mpirun -np 8 test 4M
输出：
The circular algorithm: wall time=0.030592
MPI_Allgather:          wall time=0.032610
Tree_Allgather:         wall time=0.043063

测试3
命令行：mpirun -np 8 test 8M
输出：
The circular algorithm: wall time=0.059247
MPI_Allgather:          wall time=0.064056
Tree_Allgather:         wall time=0.081441

数据量大，居然循环算法更优！*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <mpi.h>

int My_Allgather(void *sendbuf, int sendcount, MPI_Datatype sendtype,
	     void *recvbuf, int recvcount, MPI_Datatype recvtype,
	     MPI_Comm comm)
{
    int myrank,nprocs,sender,receiver,sendtag,recvtag;
    int *asendrecv;
    char *sendptr,*recvptr;
    int sendtype_size, recvtype_size;
    MPI_Status status;

    MPI_Comm_size(MPI_COMM_WORLD,&nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD,&myrank);

    MPI_Type_size(sendtype, &sendtype_size);
    MPI_Type_size(recvtype, &recvtype_size);

    sendptr=(char *)sendbuf;
    recvptr=(char *)recvbuf;

    sender=(myrank==0)?(nprocs-1):(myrank-1);
    receiver=(myrank==nprocs-1)?0:(myrank+1);
    asendrecv=malloc(nprocs*sizeof(int));
    for(int i=0;i<nprocs;i++){
        asendrecv[i]=(myrank-i>-1)?(myrank-i):(myrank-i+nprocs);
    }
    
    memcpy(recvptr+asendrecv[0]*recvcount*sendtype_size,sendptr,sendcount*sendtype_size);

    /*    
    if(myrank==2){
        for(int i=0;i<nprocs;i++){
            fprintf(stderr,"%d\t",asendrecv[i]);
        }
        fprintf(stderr,"\n");
    }*/

    for(int i=0;i<nprocs-1;i++){
        sendtag=10000+100*receiver+i;
        recvtag=10000+100*myrank+i;
        // Attention: sendtag and recvtag should fit each other
        /*fprintf(stderr, "Rank %d: Sending to %d (tag %d), Receiving from %d (tag %d)\n",
                myrank, receiver, sendtag, sender, recvtag);*/
        MPI_Sendrecv(recvptr+asendrecv[i]*sendcount*sendtype_size,sendcount,sendtype,receiver,sendtag,
                    recvptr+asendrecv[i+1]*recvcount*sendtype_size,recvcount,recvtype,sender,recvtag,
                    comm,&status);
        //fprintf(stderr,"Completed: The %d-th step!\n",i+1);
    }

    free(asendrecv);
    return MPI_SUCCESS;
}

/*根进程先全部接收消息，再广播给所有进程*/
int Tree_Allgather(void *sendbuf, int sendcount, MPI_Datatype sendtype,
	     void *recvbuf, int recvcount, MPI_Datatype recvtype,
	     MPI_Comm comm)
{    
    int nprocs;

    MPI_Comm_size(MPI_COMM_WORLD,&nprocs);

    MPI_Gather(sendbuf,sendcount,sendtype,recvbuf,recvcount,recvtype,0,comm);
    MPI_Bcast(recvbuf,nprocs*sendcount,sendtype,0,comm);

    return MPI_SUCCESS;
}
/*------------------------------------------------------------------------*/
#if 1
typedef unsigned char byte;

static void check(int nprocs, int myrank, size_t size, byte *buffer)
{
    size_t i, j;
    
    for (j = 0; j < nprocs; j++)
	for (i = 0; i < size; i++)
	    if (buffer[j * size + i] != ((j + 1) & 255)) {
		fprintf(stderr, "Process %d: incorrect value at block %d, "
				"position %d\n", myrank, j, i);
		MPI_Abort(MPI_COMM_WORLD, 1);
	    }
}

int main(int argc, char **argv)
{
    int nprocs, myrank;
    byte *send_buffer, *recv_buffer;
    size_t size = 0 /* this makes gcc happy */ ;
    double time0, time1;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    if (argc != 2) {
	if (myrank == 0)
	    fprintf(stderr, "Usage:   %s buffersize[K|M|G]\n", argv[0]);

	MPI_Finalize();
	exit(1);
    }
    else {
	char *p;
	size = strtol(argv[1], &p, 10);
	switch (toupper(*p)) {
	    case 'G':
		size *= 1024;
	    case 'M':
		size *= 1024;
	    case 'K':
		size *= 1024;
	    	break;
	}
    }
    if (size <= 0) {
	fprintf(stderr, "Process %d: invalid size %d\n", myrank, size);
	MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (myrank == 0) {
	fprintf(stderr, "Allgather with %d processes, buffer size: %d\n", 
			nprocs, size);
    }

    send_buffer = malloc(size);
    recv_buffer = malloc(nprocs * size);
    if (send_buffer == NULL || recv_buffer == NULL) {
	fprintf(stderr, "Process %d: memory allocation error!\n", myrank);
	MPI_Abort(MPI_COMM_WORLD, 1);
    }
    
    memset(send_buffer, myrank + 1, size);

    memset(recv_buffer, 0, nprocs * size);
    MPI_Barrier(MPI_COMM_WORLD);
    time0 = MPI_Wtime();
    My_Allgather(send_buffer, size, MPI_BYTE, recv_buffer, size, MPI_BYTE,
		  MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    time1 = MPI_Wtime();
    if (myrank == 0)
	fprintf(stderr, "The circular algorithm: wall time = %lf\n",
			time1 - time0);
    check(nprocs, myrank, size, recv_buffer);

    memset(recv_buffer, 0, nprocs * size);
    MPI_Barrier(MPI_COMM_WORLD);
    time0 = MPI_Wtime();
    MPI_Allgather(send_buffer, size, MPI_BYTE, recv_buffer, size, MPI_BYTE,
		  MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    time1 = MPI_Wtime();
    if (myrank == 0)
	fprintf(stderr, "MPI_Allgather: wall time = %lf\n", time1 - time0);
    check(nprocs, myrank, size, recv_buffer);

    memset(recv_buffer, 0, nprocs * size);
    MPI_Barrier(MPI_COMM_WORLD);
    time0 = MPI_Wtime();
    Tree_Allgather(send_buffer, size, MPI_BYTE, recv_buffer, size, MPI_BYTE,
		  MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    time1 = MPI_Wtime();
    if (myrank == 0)
	fprintf(stderr, "Tree_Allgather: wall time = %lf\n", time1 - time0);
    check(nprocs, myrank, size, recv_buffer);

    MPI_Finalize();
    return 0;
}
#endif


#include <math.h>
#include "allvars.h"
#include "proto.h"
#include "chealpix.h"

void AllocateArrays()
{

  // Set local slab size

  long      N  = Parameters.N;
  long  Nside  = Parameters.Nside;

  mapsize  = nside2npix(Nside);

  if(Parameters.N % nproc != 0){
    if(myid==0) printf(
	        "\n # of slices %d does not divide into # of procs %d, exiting\n\n",
		Parameters.N,nproc);
    MPI_Finalize();
    return;
  } else {
    Nlocal = N / nproc;
    size = Nlocal*N*N;
    size_fftw = Nlocal*N*(N+2);
  }
  
  int nmaps =
     Parameters.DoMap[KAPCODE]+
     Parameters.DoMap[KSZCODE]+
     Parameters.DoMap[TAUCODE];

  int Nfields = 4; // 1LPT only, delta + S_1LPT
  if(Parameters.lptcode==2) Nfields += 3;
  
  float overhead_usage = (float)ovrt;
  float mesh_usage = (float)total_local_size*Nfields*4.;
  float buffer_usage = (float)Nlocal*(float)N*N*4.*0;
  float map_usage = mapsize*nmaps*4.*2.; // factor of two is for local map buffers

  float estimated_usage = overhead_usage + mesh_usage + buffer_usage + map_usage;
  estimated_usage /= pow(1024.,3); // GB per process
  overhead_usage  /= pow(1024.,3);
  mesh_usage      /= pow(1024.,3);
  buffer_usage    /= pow(1024.,3);
  map_usage       /= pow(1024.,3);

  if(myid==0) printf( "\n  overhead usage is %f GB",overhead_usage);
  if(myid==0) printf( "\n      mesh usage is %f GB",mesh_usage);
  if(myid==0) printf( "\n    buffer usage is %f GB",buffer_usage);
  if(myid==0) printf( "\n       map usage is %f GB",map_usage);
  if(myid==0) printf( "\n estimated usage is %f GB per process",estimated_usage);

  delta1 = new float[size_fftw]();
  delta = delta1;

  sx1=sx2=sy1=sy2=sz1=sz2=delta;

  if(Parameters.lptcode>0){
    sx1 = new float[size_fftw]();
    sy1 = new float[size_fftw]();
    sz1 = new float[size_fftw]();
  }

  if(Parameters.lptcode==2){
    sx2 = new float[size_fftw]();
    sy2 = new float[size_fftw]();
    sz2 = new float[size_fftw]();
    delta2 = delta1;
  }

  if (myid==0){
    if(Parameters.DoMap[KAPCODE]==1); kapmap = (float *)malloc( mapsize*sizeof(float));
    if(Parameters.DoMap[KSZCODE]==1); kszmap = (float *)malloc( mapsize*sizeof(float));
    if(Parameters.DoMap[TAUCODE]==1); taumap = (float *)malloc( mapsize*sizeof(float));
  }

  if(myid==0) printf("\n arrays allocated...");

}


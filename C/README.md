# websky-lpt

Install & Compile C code

1. create a new copy of the file Make.mach.generic and rename to your machine:
    cp Make.mach.generic Make.mach.\<your-machine\>
2. edit the file Make.mach.\<your-machine\> to reflect your libraries and C/C++ compiler flags (you need to have fftw-2.1.5)
3. run configure (which just concatenates two files to make the Makefile):
    ./configure \<your-machine\>
4. compile:
    make

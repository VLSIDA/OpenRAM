FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
RUN echo "America/Los_Angeles" > /etc/timezone

RUN apt-get update
RUN apt-get --no-install-recommends -y upgrade

### Dependencies ###
# General tools for building etc.
RUN apt-get install --no-install-recommends -y build-essential git ssh vim gosu autoconf automake libtool bison flex
# Use bash instead of dash
# Must be on one line or else ln won't work without a shell!
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# Needed by OpenRAM
RUN apt-get install --no-install-recommends -y  python3 python3-numpy python3-scipy python3-pip python3-matplotlib python3-venv python3-sklearn python3-subunit python3-coverage
# Needed by Netgen
RUN apt-get install --no-install-recommends -y m4 csh  tk tk-dev tcl-dev
# Needed by ngspice
RUN apt-get install --no-install-recommends -y libxaw7-dev libreadline8 libreadline-dev
# X11
RUN apt-get install --no-install-recommends -y libx11-dev libcairo2-dev
# Klayout
RUN apt-get install --no-install-recommends -y  qt5-default qtcreator ruby-full ruby-dev python3-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5multimedia5-plugins libqt5multimedia5 libqt5svg5-dev libqt5designer5 libqt5designercomponents5 libqt5xmlpatterns5-dev qttools5-dev

### Klayout ###
#ARG KLAYOUT_COMMIT=v0.27.8
ARG KLAYOUT_COMMIT=ea1bf40a1ee1c1c934e47a0020417503ab3d7e7e
WORKDIR /root
RUN git clone https://github.com/KLayout/klayout
WORKDIR /root/klayout
RUN git checkout ${KLAYOUT_COMMIT}
RUN ./build.sh -qt5 -debug -j$(nproc)
RUN cp -r bin-debug /usr/local/klayout
RUN rm -rf /root/klayout

### Trilinos ###
ARG TRILINOS_COMMIT=trilinos-release-12-12-1
WORKDIR /root
RUN apt-get update
RUN apt-get install --no-install-recommends -y cmake libfftw3-dev mpich libblas-dev liblapack-dev libsuitesparse-dev libfl-dev openmpi-bin libopenmpi-dev gfortran
RUN git clone --depth 1 --branch ${TRILINOS_COMMIT} https://github.com/trilinos/Trilinos.git
RUN mkdir /root/Trilinos/build
WORKDIR /root/Trilinos/build
RUN cmake \
    -G "Unix Makefiles" \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpic++ \
    -DCMAKE_Fortran_COMPILER=mpif77 \
    -DCMAKE_CXX_FLAGS="-O3 -fPIC" \
    -DCMAKE_C_FLAGS="-O3 -fPIC" \
    -DCMAKE_Fortran_FLAGS="-O3 -fPIC" \
    -DCMAKE_INSTALL_PREFIX=/usr/local/XyceLibs/Parallel \
    -DCMAKE_MAKE_PROGRAM="make" \
    -DTrilinos_ENABLE_NOX=ON \
    -DNOX_ENABLE_LOCA=ON \
    -DTrilinos_ENABLE_EpetraExt=ON \
    -DEpetraExt_BUILD_BTF=ON \
    -DEpetraExt_BUILD_EXPERIMENTAL=ON \
    -DEpetraExt_BUILD_GRAPH_REORDERINGS=ON \
    -DTrilinos_ENABLE_TrilinosCouplings=ON \
    -DTrilinos_ENABLE_Ifpack=ON \
    -DTrilinos_ENABLE_ShyLU=ON \
    -DTrilinos_ENABLE_Isorropia=ON \
    -DTrilinos_ENABLE_AztecOO=ON \
    -DTrilinos_ENABLE_Belos=ON \
    -DTrilinos_ENABLE_Teuchos=ON \
    -DTeuchos_ENABLE_COMPLEX=ON \
    -DTrilinos_ENABLE_Amesos=ON \
    -DAmesos_ENABLE_KLU=ON \
    -DTrilinos_ENABLE_Sacado=ON \
    -DTrilinos_ENABLE_Kokkos=ON \
    -DTrilinos_ENABLE_Zoltan=ON \
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES=OFF \
    -DTrilinos_ENABLE_CXX11=ON \
    -DTPL_ENABLE_AMD=ON \
    -DAMD_LIBRARY_DIRS="/usr/lib" \
    -DTPL_AMD_INCLUDE_DIRS="/usr/include/suitesparse" \
    -DTPL_ENABLE_BLAS=ON \
    -DTPL_ENABLE_LAPACK=ON \
    -DTPL_ENABLE_MPI=ON \
    /root/Trilinos
RUN make -j 4 
RUN make install

ARG XYCE_COMMIT=b7bb12d81f11d8b50141262537299b09d64b5565
WORKDIR /root
RUN git clone https://github.com/Xyce/Xyce.git
WORKDIR /root/Xyce
RUN git checkout ${XYCE_COMMIT}
RUN ./bootstrap
RUN mkdir /root/Xyce/build
WORKDIR /root/Xyce/build
RUN ../configure CXXFLAGS="-O3 -std=c++11" \
    ARCHDIR="/usr/local/XyceLibs/Parallel" \
    CPPFLAGS="-I/usr/include/suitesparse" \
    --enable-mpi CXX=mpicxx CC=mpicc F77=mpif77 \
    --prefix=/usr/local/Xyce/Parallel --enable-shared --enable-xyce-shareable 
RUN make -j 4 install

### Ngspice ###
ARG NGSPICE_COMMIT=032b1c32c4dbad45ff132bcfac1dbecadbd8abb0
WORKDIR /root
RUN git clone git://git.code.sf.net/p/ngspice/ngspice
WORKDIR /root/ngspice
RUN git checkout ${NGSPICE_COMMIT}
RUN ./autogen.sh
RUN ./configure --enable-openmp --with-readline
RUN make
RUN make install
RUN rm -rf /root/ngspice

### Netgen ###
#ARG NETGEN_COMMIT=1.5.195
ARG NETGEN_COMMIT=1.5.221
WORKDIR /root
#RUN git clone https://github.com/RTimothyEdwards/netgen.git netgen
RUN git clone git://opencircuitdesign.com/netgen netgen
WORKDIR /root/netgen
RUN git checkout ${NETGEN_COMMIT}
RUN ./configure
RUN make -j$(nproc)
RUN make install
RUN rm -rf /root/netgen

### iVerilog ###
RUN apt-get install --no-install-recommends -y iverilog

### Magic ###
#ARG MAGIC_COMMIT=db4fa65bfc096e63954b37b188ea27b90ab31839
#ARG MAGIC_COMMIT=8.3.274
ARG MAGIC_COMMIT=8.3.311
WORKDIR /root
#RUN git clone https://github.com/RTimothyEdwards/magic.git magic
RUN git clone git://opencircuitdesign.com/magic magic
WORKDIR /root/magic
RUN git checkout ${MAGIC_COMMIT}
COPY mrg.patch /root/magic
RUN git apply mrg.patch
RUN ./configure
RUN make
RUN make install
RUN rm -rf /root/magic


### CLEAN UP ###
# Remove development tools to save space
RUN apt-get remove -y build-essential autoconf automake libtool bison flex  tcl-dev tk-dev cmake
# Cleanup to save some space
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


# ### SET UP A GENERIC USER ###
RUN useradd cad-user
RUN mkdir /home/cad-user
RUN chown -R cad-user /home/cad-user
RUN chgrp -R cad-user /home/cad-user
ADD set-paths.sh /home/cad-user/.bashrc
USER cad-user
WORKDIR /home/cad-user

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
ARG KLAYOUT_COMMIT=ea1bf40a1ee1c1c934e47a0020417503ab3d7e7e
WORKDIR /root
RUN git clone https://github.com/KLayout/klayout
WORKDIR /root/klayout
RUN git checkout ${KLAYOUT_COMMIT}
RUN ./build.sh -qt5 \
 && cp -r bin-release /usr/local/klayout
RUN rm -rf /root/klayout

### Magic ###
ARG MAGIC_COMMIT=8.3.197
WORKDIR /root
RUN git clone git://opencircuitdesign.com/magic-8.3 magic
WORKDIR /root/magic
RUN git checkout ${MAGIC_COMMIT}
RUN ./configure \
 && make \
 && make install
RUN rm -rf /root/magic

### Ngspice ###
ARG NGSPICE_COMIT=032b1c32c4dbad45ff132bcfac1dbecadbd8abb0
WORKDIR /root
RUN git clone git://git.code.sf.net/p/ngspice/ngspice
WORKDIR /root/ngspice
RUN git checkout ${NGSPICE_COMMIT}
RUN ./autogen.sh \
 && ./configure --enable-openmp --with-readline \
 && make \
 && make install
RUN rm -rf /root/ngspice

### Netgen ###
ARG NETGEN_COMMIT=e4a15f12fbdd3480b6adc0eeba09df269ed7b387
WORKDIR /root
RUN git clone git://opencircuitdesign.com/netgen-1.5 netgen
WORKDIR /root/netgen
RUN git checkout ${NETGEN_COMMIT}
RUN ./configure \
 && make -j$(nproc) \
 && make install
RUN rm -rf /root/netgen

#ARG XYCE_COMMIT=b7bb12d81f11d8b50141262537299b09d64b5565
#ARG TRILINOS_COMIT=

### CLEAN UP ###
# Remove development tools to save space
RUN apt-get remove -y build-essential autoconf automake libtool bison flex  tcl-dev tk-dev
# Cleanup to save some space
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


# ### SET UP A GENERIC USER ###
# WORKDIR /p
# RUN echo "cd ~" >> /etc/skel/.bashrc
# RUN echo "source /set-paths.sh" >> /etc/skel/.bashrc
# ADD set-paths.sh /set-paths.sh
# RUN chmod 755 /set-paths.sh

### ADD ENTRY POINT ###
# COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN chmod 755 /usr/local/bin/entrypoint.sh
# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# CMD ["/bin/bash"]

RUN mkdir /home/cad-user
RUN useradd cad-user
RUN chown -R cad-user /home/cad-user
RUN chgrp -R cad-user /home/cad-user
USER cad-user
WORKDIR /home/cad-user

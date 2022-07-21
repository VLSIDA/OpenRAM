# Docker images for OpenRAM #

## Installing Docker ##

There are a number of ways to install Docker.  Pick your favorite.

* On Mac from docker.com with .app:
 https://docs.docker.com/docker-for-mac/install/

* On Windows from docker.com:
 https://docs.docker.com/docker-for-windows/install/

* On Ubuntu:
 https://docs.docker.com/install/linux/docker-ce/ubuntu/

NOTE: If you plan to use a VPN, do *NOT* use the Docker Toolbox for
Mac or the docker from [Macports](https://www.macports.org/
"Macports") as these require a network socket that breaks when you
install some VPN software. To understand the difference, check out [this
page](https://docs.docker.com/docker-for-mac/docker-toolbox/).

## Running Docker ##

### Terminal only ###

* To run as a generic user:
```
make mount
```

## Updating the image ##

If there are updates to the image, you can pull a new one from the hub with:
```
make pull
```
This is not automatically done, so if you have a problem, make sure you are up-to-date.

## Building your own image ##

You can run the build script to build a local image:

```
make build
```

If you want to change things, modify the openram-ubuntu/Dockerfile and let me know what should be fixed.

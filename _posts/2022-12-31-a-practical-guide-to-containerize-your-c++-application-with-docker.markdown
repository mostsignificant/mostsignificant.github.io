---
layout: post
title: "A Practical Guide To Containerize Your C++ Application With Docker"
date: 2022-12-31 12:00:00 +0200
categories: C++ docker
comments: true
published: true
excerpt: |
  If you have C++ code that you want to deploy as a Docker container, this guide will help you to write your
  first Dockerfile and build and run your C++ application.
image_url: /assets/images/unsplash/lionello-delpiccolo-Dv65oNf9UI4-unsplash.jpg
image_description: |
  Photo by [Lionello DelPiccolo](https://unsplash.com/es/@liodp?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/Dv65oNf9UI4?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

This blog post is mostly aimed at C++ developers whithout much Docker experience but who want to get started
deploying their applications via container. If some concepts are already known to you, feel free to skip to the next
sections.

## Today's Example: simplehttpserver

For this exercise I have reused an example from the wonderful
[Boost.Beast](https://www.boost.org/doc/libs/1_81_0/libs/beast/doc/html/index.html) library. This example is an
asynchronous HTTP server which serves static files from a local directory. The server consists of a single
```main.cpp``` file with according ```CMakeLists.txt``` files written by me.

There are several examples on the Beast library's
[website](https://www.boost.org/doc/libs/1_81_0/libs/beast/doc/html/beast/examples.html#beast.examples.servers) and I
have used the fairly simple
[http_server_async.cpp](https://www.boost.org/doc/libs/1_81_0/libs/beast/example/http/server/async/http_server_async.cpp).
Maybe in the future I will switch to C++20's coroutines - they do make Boost.Asio (which the Beast library is based
upon) arguably simpler to write and read.

The code uses Boost's asynchronous IO handling to serve each HTTP request. The simplehttpserver features command line
arguments to configure host, port, document root and the number of used threads.

```sh
Allowed command line options:
  --help                      produce help message
  --host arg (=0.0.0.0)       host address to bind to
  --port arg (=8080)          port to expose to
  --doc_root arg (=/var/www/) root directory to serve
  --threads arg (=1)          number of threads to use
```

## The Quickest Docker Introduction

If you do not know Docker yet, let me quickly introduce you to the most important concepts. The most important thing to
remember is: Docker is not a virtual machine. Docker is a mechanism to containerize applications and isolate the
processes running these applications.

> Virtual machines are about isolating hardware, Docker is about isolating processes.

There are two central entities in the Docker world: *images* and *container*. A *Docker Image* is created from a so
called *Dockerfile*. This file describes the commands to build an image. From this image a *Docker Container* can be
created: they are the actual running instances of the images. The *Docker engine* is responsible for instantiating and
running the containers.

![Docker Build And runtime](/assets/images/posts/2022_12_31_docker_build_and_run_time.png "Docker Build And runtime")

There are additional concepts that are not important for our example in this blog post. However, I want to mention them
in case you want to investigate further.

- *Docker Volume* is a mechanism to have a Docker managed file share between your container. You can map these volumes
via so-called *bind mounts* into a container.
- *Docker Networking* allows you to specify virtual Docker networks. Network traffic from and to containers is routed
through a Docker proxy. This allows different setups for networking between individual containers.
- *Docker Compose* is a feature to build and run several different containers from a single ```docker-compose.yml```
file. You can specify the exact images for the docker containers, the container names, networks, volumes and much more.
For example, if you want to run a MySQL container and your custom REST API service container along with a REDIS
container for cache, you can set this up with Docker compose.

## Installing The Docker Engine

Before you get started, you need to install [Docker](https://www.docker.com). The Docker website recommends the usage of
Docker desktop but it is not required to run our example. I prefer the command line to GUI applications when it
comes to building, running and everything else about Docker containers.

However, on MacOS I found it easier to just install Docker Desktop for the engine. If you still want to just install the
engine without the desktop application, follow these excellent tutorials for
[MacOS](https://unix.stackexchange.com/questions/667940/how-to-install-docker-engine-in-macos-without-docker-desktop)
or [Windows with WSL](https://www.paulsblog.dev/how-to-install-docker-without-docker-desktop-on-windows/).

The following command installs the Docker engine on Linux distros with ```apt``` as package manager:

```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Find more informations about installing the Docker engine on the
[official documentation](https://docs.docker.com/engine/install/) including adding the correct repository and
troubleshooting.

## Writing The Dockerfile

The initial project structure is a simple C++ project with a single source code directory and a CMake file. The
directory contains the mentioned ```main.cpp``` file. The CMake file builds the project by linking the required *Beast*
and *Threads* libraries.

```sh
src/
CMakeLists.txt
```

To get started with containerizing, create a new Dockerfile in your project directory:

```sh
touch Dockerfile
```

This Dockerfile will contain all necessary commands to build your Docker image. The most important commands in a
Dockerfile are the following:

- ```FROM``` creates a new stage from an existing Docker image
- ```RUN``` executes a Linux command in the image
- ```COPY``` copies files or folders from the local file system into the image
- ```CMD``` or ```ENTRYPOINT``` is executed when the image is instantiated as container

Again, it is important to remember the difference between images (build time) and container (runtime). The commands
```FROM```, ```RUN```, and ```COPY``` are executed at build time. The commands ```CMD``` or ```ENTRYPOINT``` are
executed at runtime.

We are using a [multi-stage build](https://docs.docker.com/build/building/multi-stage/) for our image. Multi-stage
builds are best practice if you are building an application in the container. We are planning on having a *build* stage
where we install build tools and dependencies, copy the required source files into the image and run CMake configuration
and build to build the application binary. In the second stage, which builds the final image, we are installing the
runtime dependencies and create a runtime user. After this, we just copy the built binary into the final image and
define the entrypoint which starts the simplehttpserver.

![Docker Multi-Stage](/assets/images/posts/2022_12_31_docker_image.png "Docker Multi-Stage")

### The Build Stage

The ```FROM``` command specifies the image to build upon. In this case, we are using the small *alpine* image. It is
best practice to specify the exact version of the image (in this case 3.17.0). The following keyword ```AS``` specifies
the name of the stage, in our case *build*.

```sh
FROM alpine:3.17.0 AS build
```

The next command installs the dependencies that are required to build our simplehttpserver application. It is best
practice to specify the version numbers, too. This ensures reproducible builds.

```sh
RUN apk update && \
    apk add --no-cache \
        build-base=0.5-r3 \
        cmake=3.24.3-r0 \
        boost1.80-dev=1.80.0-r3
```

We are using the ```WORKDIR``` command to change into a directory for building the application (which is created if not
yet existing, so you do not need to run ```mkdir``` beforehand). Afterwards we are copying the source folder and the CMake
file into this directory. I prefer explicitly stating the folders or individual files for copying to ensure that no
additional stuff is copied by accident.

```sh
WORKDIR /simplehttpserver

COPY src/ ./src/
COPY CMakeLists.txt .
```

After the copy step, we are creating and changing to a *build* directory with the ```WORKDIR``` command again. Here it
is just a simple matter of executing CMake and building the application. Be aware that the parallel argument is optional
and could be better passed as ```ARG``` to the Dockerfile - but this is outside of the scope of this blog post. For
example, GitHub runners have two available threads as far as I know. On my local machine, I am using all eight available
threads.

```sh
WORKDIR /simplehttpserver/build

RUN cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . --parallel 8
```

### The Final Image

For the final image we are declaring this stage with another ```FROM```statement again. We are also using the same
*alpine* image as a basis as we did for the build stage.

```sh
FROM alpine:3.17.0
```

We are installing the runtime libraries - in our case Boost's program options, which we used for scanning the command
line arguments. Additionally the libstdc++ library, which is not part of the used alpine base image. We do not need the
used Beast library, since it is header-only and already in our built binary.

```sh
RUN apk update && \
    apk add --no-cache \
    libstdc++=12.2.1_git20220924-r4 \
    boost1.80-program_options=1.80.0-r3
```

As next step and best practice, we are creating a user called *shs* for running our simplehttpserver application.
Otherwise the application is run as root (inside the container).

```sh
RUN addgroup -S shs && adduser -S shs -G shs
USER shs
```

After this we are copying the built simplehttpserver binary from the build stage to our final image. The ```--chown```
option specifies the ownership and the ```--from``` option the name of the stage where to copy from.

```sh
COPY --chown=shs:shs --from=build \
    ./simplehttpserver/build/src/simplehttpserver \
    ./app/
```

The last command is the starting point that is executed at runtime when the container is instantiated from this image.
This allows any command line arguments to be passed, too.

```sh
ENTRYPOINT [ "./app/simplehttpserver" ]
```

You can find the full Dockerfile in my
[GitHub repo](https://github.com/mostsignificant/simplehttpserver/blob/main/Dockerfile).

## Building The Docker Image

The Docker image can be built by executing the following command in the project directory. The option ```-t``` is used
to specify the repository, name and optionally the tag of the image, according to the schema
```<repository>/<name>:<tag>```. If you do not declare a tag after the colon, Docker will use the tag *latest*. The
following command builds the image *mostsignificant/simplehttpserver:latest* which can be used later to specify to
instantiate a container.

```sh
docker build . -t mostsignificant/simplehttpserver
```

During the build you can see the different stages and layers being built. Each command in the Dockerfile adds a new
layer. Thus it is important to have a multi-stage build to have only the built binary and the run-time dependencies in
it. After building, run the following command to list all your local images with their information.

```sh
docker image ls
```

```sh
REPOSITORY                         TAG      IMAGE ID       CREATED       SIZE
mostsignificant/simplehttpserver   latest   afb9c03f8849   2 hours ago   14.4MB
```

14.4 MB is a reasonable size for this image - if you had used *debian:bullseye-slim* as base for this image, the
resulting size would have been a whopping 104 MB. Reducing an image's size can be a daunting task, but there are tools
to support this task, for example [dive](https://github.com/wagoodman/dive) which helps inspect the different layers
of an image. Be aware that files added in earlier layers during the build process can be deleted in a later layer - but
the original data is still in the resulting image. Therefore you can:

- use multi-stage builds and copy only the needed files from earlier stages to your final image
- or use remote repositories to install from instead of copying install packages into the image
- or download, unpack, install and remove packages in a single ```RUN``` command

## Running The Docker Image As Container

The following command runs the image and instantiates a container:

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/var/www \
  -p 8080:8080 \
  -d \
  mostsignificant/simplehttpserver:latest
```

We are using the following command line arguments:

- ```--mount``` mounts a local path to a path in the container: we are mapping the current path to the ```/var/www```
  directory, thus enabling the simplehttpserver application to serve all files in the current directory via HTTP
- ```-p``` maps a port from inside the container to the host: the simplehttpserver's default port *8080* is mapped to the
  same host port, but you can use any other available port
- ```-d``` starts the container in detached mode

The running Docker containers can also be inspected:

```sh
docker ps
```

```sh
CONTAINER ID   IMAGE                                     COMMAND                  CREATED         STATUS         PORTS                    NAMES
635e4dafcdb6   mostsignificant/simplehttpserver:latest   "./app/simplehttpser…"   3 seconds ago   Up 2 seconds   0.0.0.0:8080->8080/tcp   serene_torvalds
```

The container names are randomly generated if not specified otherwise - in our case *serene_torvalds* (I think it is
always good to have Linus in a serene mood /s). You can use the container id (hash) or name to access it, for example:

- ```docker stop 635e4dafcdb6``` to stop the container (and its processes)
- ```docker rm 635e4dafcdb6``` to remove the stopped container (but not the image!)
- ```docker inspect 635e4dafcdb6``` to get more information about the container

## Publishing The Docker Image

In order to publish your docker image, you need to create an account at the [Docker Hub](https://hub.docker.com) first. Be
aware that your account name needs to be the repository name you used earlier (or you just rename the image). In my case
my account name is *mostsignificant*, thus I name the images accordingly: *mostsignificant/<app-name>:<tag>*.

After you create your account, you must login to Docker Hub via the following command and provide credentials:

```sh
docker login
```

After logging in, the image can be pushed to the Docker Hub.

```sh
docker push mostsignificant/simplehttpserver:latest
```

And that's it. Now anybody can download and run your Docker image.

![Docker Hub](/assets/images/posts/2022_12_31_docker_hub.png "Docker Hub")

## Next Steps

Now you got your first Docker image with your application running. As always, there are some TLC steps to improve your
image and everything around it. Here are some suggestions:

- **Build pipeline**: You can integrate the Docker build and push step into your build pipeline. If you are using GitHub
  Actions there is an
  [excellent documentation](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images) on how to
  do it: either to GitHub's own repository called GitHub Packages or Docker Hub.
- **Testing**: You can also include a test step in you build stage (for example via *CTest*). Just include the test in a way
  that the Docker image build does not fail if the tests fail - this way you can copy your test results file
  [out of the image](https://stackoverflow.com/a/51186557) and pass it to your build pipeline. Than the build pipeline
  can prevent the publishing of the image if previous tests failed.
- **Linting**: You can use a Docker linter like [hadolint](https://hadolint.github.io/hadolint/) to check your Dockerfile
  for common best practice violations.
- **Documentation**: Use [labels](https://docs.docker.com/engine/reference/builder/#label) to improve the documentation of
  your Dockerfile and add a README about your image to your site on Docker Hub.
- **.dockerignore**: Add a [.dockerignore file](https://docs.docker.com/engine/reference/builder/#dockerignore-file) to
  your project directory to prevent docker builds to copy unwanted files or folders into your image (and be careful with
  the ```COPY``` command in general)

## Conclusion

I hope this little tutorial helped any C++ developer not familiar with Docker to get started containerizing their
applications. The full example can be found on my [GitHub repo](https://github.com/mostsignificant/simplehttpserver) and
the built image on my [Docker Hub repo](https://hub.docker.com/repository/docker/mostsignificant/simplehttpserver).
There is a lot more to learn about the Docker world, and the official [documentation](https://docs.docker.com) and
[reference](https://docs.docker.com/reference/) is a good start.

Keep on coding and keep on creating! Happy New Year!

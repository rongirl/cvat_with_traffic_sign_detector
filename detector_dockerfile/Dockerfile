ROM ubuntu:22.04

# Build arguments
ARG UBUNTU_RELEASE_YEAR
ARG ZED_SDK_MAJOR
ARG ZED_SDK_MINOR
ARG CUDA_MAJOR
ARG CUDA_MINOR
ENV OPENCV_VERSION 4.x
ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Europe/Moscow

# OpenCV Version
ARG OPENCV_VERSION

# Install dependencies
RUN apt-get update || true && apt-get upgrade -y &&\
    apt-get install --no-install-recommends -y \
	build-essential \ 
    gcc \ 
    g++ \
	cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \ 
    libavformat-dev \ 
    libswscale-dev \
	libtbb2 \ 
    libtbb-dev \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \
    yasm \ 
    libatlas-base-dev\
    gfortran\
    libpq-dev \
    libxine2-dev \ 
    libglew-dev \ 
    libtiff5-dev \ 
    zlib1g-dev \ 
    libavutil-dev \
    libpostproc-dev \
    libeigen3-dev \ 
    python3-dev \ 
    python3-pip \ 
    python3-numpy \ 
    libx11-dev tzdata \
&& rm -rf /var/lib/apt/lists/*

# Set Working directory
WORKDIR /opt


# Install OpenCV 
RUN git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git && \
    cd opencv && \
    mkdir build && \
    cd build && \
    cmake \
	-D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/ \
	-D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
	-D WITH_V4L=ON \
	-D WITH_QT=OFF \
	-D WITH_OPENGL=ON \
	-D WITH_GSTREAMER=ON \
	-D OPENCV_GENERATE_PKGCONFIG=ON \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D INSTALL_PYTHON_EXAMPLES=OFF \
	-D INSTALL_C_EXAMPLES=OFF \
	-D BUILD_EXAMPLES=OFF .. && \
   make -j"$(nproc)" && \
   make install

RUN apt update && apt install libcpprest-dev -y

RUN sed -i '86 i INTERFACE_LINK_LIBRARIES "OpenSSL::SSL"' /usr/lib/x86_64-linux-gnu/cmake/cpprestsdk/cpprestsdk-targets.cmake

RUN git clone --branch trafficSignDetection   https://github.com/osechkina-masha/adas_spbu.git &&\
    cd adas_spbu && \
    cd traffic_signs_detection && \
    cd traffic_signs_detection && \
    cmake . && \
    make


EXPOSE 8083

CMD ["./adas_spbu/traffic_signs_detection/traffic_signs_detection/traffic_signs_detection"]
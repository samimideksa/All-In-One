FROM ubuntu:16.04

RUN apt-get update 
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        python3.6 \
        python3.6-dev \
        python3-pip \
        python-setuptools \
        cmake \
        wget \
        curl \
        libsm6 \
        libxext6 \ 
        libxrender-dev

COPY requirements.txt /tmp

WORKDIR /tmp

# 
# RUN python3.6 -m pip install -r requirements.txt

RUN curl "https://bootstrap.pypa.io/get-pip.py" | python3.6

RUN pip install --upgrade pip
RUN pip install --upgrade requests
RUN pip install --upgrade setuptools
RUN python3.6 -m pip install -r requirements.txt

COPY . /All-In-One
WORKDIR /All-In-One
RUN python3.6 -m pip install -U pip
RUN cd allinonemodels && wget http://144.76.153.5/aio_model/freeze2.h5
EXPOSE 50051

RUN cd Service && python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. detect_image.proto

CMD ["python3.6", "Service/server.py"]

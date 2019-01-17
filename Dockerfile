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
RUN pip install --upgrade gdown
RUN python3.6 -m pip install -r requirements.txt

COPY . /All-In-One
WORKDIR /All-In-One
RUN python3.6 -m pip install -U pip
RUN git clone https://github.com/circulosmeos/gdown.pl && cd gdown.pl && ./gdown.pl https://drive.google.com/file/d/1hXliiDFQGFRRNKGbxX7pUkMvq55wLYtZ/view?usp=sharing model.tar.gz && mv model.tar.gz model.tar && tar xvf model.tar && cd model
EXPOSE 50051

RUN cd grpc && python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. all_in_one.proto

CMD ["python3.6", "grpc/allinone_server.py"]
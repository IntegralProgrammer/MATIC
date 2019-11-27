FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install \
	build-essential \
	python \
	python-setuptools \
	nano \
	gcc-arm-none-eabi \
	python-networkx \
	python-lxml \
	curl

RUN curl -L https://github.com/unicorn-engine/unicorn/archive/1.0.1.tar.gz -o unicorn-1.0.1.tar.gz
COPY unicorn-1.0.1.sha256sum /
RUN sha256sum -c unicorn-1.0.1.sha256sum
RUN tar -xvf unicorn-1.0.1.tar.gz
RUN cd unicorn-1.0.1 && ./make.sh && ./make.sh install
RUN cd /unicorn-1.0.1/bindings/python && python setup.py install

COPY src /src
ENTRYPOINT ["bash"]

FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install \
    python3 \
    python3-venv \
    python3-pip

RUN pip3 install setuptools

COPY /home/erdem/Ws/PyPi/edit/edit/ /root/packages/edit/
WORKDIR /root/packages/edit
RUN pip3 install /root/packages/edit

CMD ["python3","test/edit.py"]



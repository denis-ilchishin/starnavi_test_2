FROM python:3.9

RUN apt update -y && \
    apt upgrade -y

ARG USER=container
ARG USER_ID=1000
ENV HOME=/home/${USER}
ENV VSCODE=${HOME}/.vscode-server/extensions

RUN mkdir ${HOME} && \
    useradd -u ${USER_ID} -d ${HOME} ${USER} && \
    mkdir -p ${VSCODE}

ADD requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY . ${HOME}/app

RUN chown ${USER}:${USER} -R ${HOME}

WORKDIR ${HOME}/app/src

USER ${USER}
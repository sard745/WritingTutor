FROM huggingface/transformers-pytorch-gpu:4.28.1
LABEL maintainer="nightowl-jp"
RUN apt update
RUN mkdir /work
RUN apt install -y wget build-essential libpcre2-dev libffi-dev python3-dev libbz2-dev liblzma-dev libicu-dev libblas-dev liblapack-dev
RUN apt install -y --no-install-recommends software-properties-common dirmngr
COPY ./requirements.txt /work/requirements.txt
RUN python3 -m pip install -r /work/requirements.txt

ENV AZURE_API_KEY=Set your Azure API Key
ENV AZURE_API_ENDPOINT=Set your Azure API Endpoint

WORKDIR /home/work

EXPOSE 8501

# docker build -t ase/azure ./
# docker run -t -d -v /home/suzuki.h.ci/AutoSummEval:/home/work -p 8501:8501 --gpus '"device=0"' --name ase ase/azure /bin/bash
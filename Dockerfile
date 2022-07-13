FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
  apt-get install -y python3 python3-pip \
    python3-numpy python3-pandas python3-sklearn && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 8050

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "index.py" ]

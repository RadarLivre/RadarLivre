FROM ubuntu:22.04

WORKDIR /app
COPY . .

ENV TZ=America/Fortaleza
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y python3-pip \
    && apt install -y tzdata \
    && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get install -y \
    binutils \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

RUN python3 -m pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
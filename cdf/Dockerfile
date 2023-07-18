FROM --platform=linux/amd64 osgeo/gdal:ubuntu-full-3.6.3

WORKDIR /code

RUN apt-get -y update 
RUN apt -y install python3-pip libspatialindex-dev \
    && apt-get install -y --no-install-recommends \
       gdal-bin \
       libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
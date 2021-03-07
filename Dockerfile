FROM python:3
WORKDIR /src
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install --no-install-recommends -y libgl1-mesa-glx libsm6 -y
RUN apt-get install --reinstall libxcb-xinerama0

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "src/main.py" ]

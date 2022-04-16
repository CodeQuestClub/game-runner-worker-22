FROM python:3.9

RUN apt update && apt install -y vim cmake pkg-config 
RUN apt install -y mesa-utils libglu1-mesa-dev freeglut3-dev mesa-common-dev
RUN apt install -y libglew-dev libglfw3-dev libglm-dev
RUN apt install -y libao-dev libmpg123-dev

COPY ./requirements.txt /codequest/requirements.txt
COPY ./app /codequest/app

WORKDIR /codequest
RUN pip install -r requirements.txt

CMD ["python", "./app/main.py"]
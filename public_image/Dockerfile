FROM python:3.10

RUN apt update && apt install -y vim cmake pkg-config 
RUN apt install -y mesa-utils libglu1-mesa-dev freeglut3-dev mesa-common-dev
RUN apt install -y libglew-dev libglfw3-dev libglm-dev
RUN apt install -y libao-dev libmpg123-dev

COPY ./requirements.txt /codequest/requirements.txt
COPY ./run_game.sh /codequest/run_game.sh
COPY ./get_bot_names.py /codequest/get_bot_names.py

WORKDIR /codequest
RUN chmod +x run_game.sh
RUN pip install -r requirements.txt

CMD ./run_game.sh
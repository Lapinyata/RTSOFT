Порядок установки

$ sudo xhost +local

$ sudo docker build -t z2 .

$ sudo docker run -it --env="DISPLAY" --net=host z2

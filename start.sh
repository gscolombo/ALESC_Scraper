#! /usr/bin/sh

image="gscolombo/alesc-crawler:latest"


if [ -z "$(docker images -q $image 2> /dev/null)" ]; then
    echo "Image \"$image\" not found.\nStarting build...\n"
    docker build -t $image .
fi
echo "\n"
clear
docker run -itv $PWD/data:/home/datapolicy/data $image python src/main.py
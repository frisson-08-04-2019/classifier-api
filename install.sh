#!/bin/bash

sudo apt update
sudo apt-get install python3-pip python3-dev -y
conda create -n classifier-api pip python=3.7.1 -y
source activate classifier-api
easy_install -U pip
git submodule init
git submodule update
pip install --ignore-installed --upgrade -r requirements.txt
pip install --ignore-installed --upgrade -r flask_app/classifier/requirements.txt
conda install pytorch=1.0.1 torchvision cudatoolkit=9.0 cudnn=7.1.2 -c pytorch -y

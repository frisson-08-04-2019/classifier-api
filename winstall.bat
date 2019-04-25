@echo off
PATH = %PATH%;%USERPROFILE%\Miniconda3\Scripts;%PROGRAMFILES%\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin;C:\cudnn-9.0-windows10-x64-v7.4.1.5\cuda\bin;%PROGRAMFILES(X86)%\Graphviz2.38\bin
conda create -n classifier-api pip python=3.7.1 -y
call activate classifier-api
git submodule init
git submodule update
pip install --ignore-installed --upgrade -r requirements.txt
pip install --ignore-installed --upgrade -r flask_app\classifier\requirements.txt
conda install pytorch=1.0.1 torchvision cudatoolkit=9.0 -c pytorch -y

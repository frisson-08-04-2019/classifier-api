@echo off
chcp 65001
PATH = %PATH%;%USERPROFILE%\Miniconda3\Scripts;C:\Program Files\7-Zip;%PROGRAMFILES%\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin;C:\cudnn-9.0-windows10-x64-v7.4.1.5\cuda\bin;%PROGRAMFILES(X86)%\Graphviz2.38\bin
call activate classifier-api

IF ["%~1"] == [""] (
  cmd /k
) ELSE (
  IF NOT ["%~1"] == ["setenv"] (
    start "" "%~1"
  )
)

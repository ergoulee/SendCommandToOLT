echo off
set cmd1=py.exe "D:\autosend\test.py" "activate" "1" %*  
set cmd2=py.exe "D:\autosend\test.py" "activate" "2" %* 
start %cmd1%
start %cmd2%

echo off
set cmd1=py.exe "D:\autosend\test3.py" "activate" %*  
set cmd2=py.exe "D:\autosend\test4.py" "activate" %* 
start %cmd1%
start %cmd2%

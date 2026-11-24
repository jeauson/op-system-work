@echo off
set "PATH=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer;%PATH%"
call "%ProgramFiles%\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
set "TMP=C:\Temp"
set "TEMP=C:\Temp"
cl /nologo /EHsc /std:c++17 /source-charset:utf-8 /execution-charset:gbk %*

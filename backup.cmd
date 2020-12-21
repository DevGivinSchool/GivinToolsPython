rem Дата и время для имени файла, учитываются часы < 10 (один знак вместо двух => 07).
FOR /F "tokens=1-4 delims=., " %%i IN ('DATE /t') DO SET pdate=%%k_%%j_%%i
FOR /F "tokens=1-4 delims=:"  %%b IN ('TIME /T') DO SET ptime=%%b_%%c
set date_name=%pdate%_%ptime%
rem echo %date_name%

rem Base Project Folder
SET BASEPATH=c:\MyGit
rem Folder Project Name 
SET PNAME=GivinToolsPython
rem Backup Path
SET BP=d:\YandexDisk\MyGitBackup\GivinToolsPython
rem Path to WinRAR
SET WINRAR=C:\Program Files\WinRAR\WinRAR.exe
rem Path to 7-Zip
SET SZIP=c:\Program Files\7-Zip\7z.exe

mkdir "%BP%"
rem "%WINRAR%" a -r -s -m5 -md1024 -ag_YYYYMMDD-NN "%BP%\%PNAME%.rar" "c:\MyGit\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -xr!log -xr!PASSWORDS.py -xr!SETTINGS.py -xr!__pycache__ "%BP%\%date_name%_%PNAME%.7z" "%BASEPATH%\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -p%mypass% "%BP%\%date_name%_%PNAME%_PASS.7z" "%BASEPATH%\%PNAME%\core\PASSWORDS.py"
rem Delete backups except last three
cd /d "%BP%"
for /f "skip=6 eol=: delims=" %%F in ('dir /b /o-d *.7z') do @del "%%F"

pause

rem @echo off
set dd=%DATE:~0,2%
set mm=%DATE:~3,2%
set yyyy=%DATE:~6,4%
set curdate=%yyyy%%mm%%dd%

"C:\Program Files (x86)\pgAdmin 4\v4\runtime\pg_dump.exe" --file "D:\YandexDisk\TEMP\GS\gs%curdate%.sql" --host %GSHOST% --port %GSPORT% --username %GSUSER% --verbose --encoding "UTF8" %GSDATABASE%
"c:\Program Files\7-Zip\7z.exe" a -tzip -mx5 -sdel -y D:\YandexDisk\TEMP\GS\gs%curdate%.zip D:\YandexDisk\TEMP\GS\*.sql
rem Удаление архивов старше 30 дней
forfiles /p D:\YandexDisk\TEMP\GS /m *.zip /s /d -30 /c "cmd /c del @path /q"
rem pause

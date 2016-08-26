@ECHO OFF 
SETLOCAL
set arg1=%1
FOR %%i IN ("%arg1%") DO (
  set filepath=%%~pi
  goto :next
)
:next

:: Define BS to contain a backspace
::for /f %%q in ('"prompt $H&for %%r in (1) do rem"') do set "BS=%%q"
ECHO | set /p name="transfer_input_files = mosaic_to_raster.py," 
(FOR /f "delims=" %%a IN ('dir %arg1% /b') DO (
    (   ECHO | set /p name="%filepath%"
		ECHO | set /p name="%%a"
		ECHO | set /p name=","
	)
))>listfiles.csv
TYPE listfiles.csv
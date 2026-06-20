cd %~dp0
set "tmx2ea=%~dp0Tools\tmx2ea\tmx2ea.exe"
echo Running full make hack.

copy FE8_clean.gba myHack.gba

cd "%~dp0Tables"
echo: | (c2ea "%~dp0FE8_clean.gba" -installer "%base_dir%Tables/TableInstaller.event")

cd "%~dp0Text"
echo: | (textprocess_v2 text_buildfile.txt --parser-exe "%parsefile%" --installer "InstallTextData.event" --definitions "TextDefinitions.event")

  cd "%~dp0Maps"
  echo: | ("%tmx2ea%" -s "MasterMapInstaller.event")

cd "%~dp0EventAssembler"

ColorzCore A FE8 "-output:%~dp0myHack.gba" "-input:%~dp0ROM Buildfile.event" "--nocash-sym:%~dp0FE8Hack.sym" "--build-times"
type "%~dp0FE8_clean.sym" >> "%~dp0myHack.sym"

cd "%~dp0ups"

ups diff -b "%~dp0FE8_clean.gba" -m "%~dp0myHack.gba" -o "%~dp0myHack.ups"

pause

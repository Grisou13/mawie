@echo off
REM CMD /C npm install -g reveal-md
reveal-md --host %computername% -D -w --preprocessor processor.js presentation.md

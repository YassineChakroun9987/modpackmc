@echo off
title Green Lanterns - Dev Server
cd /d "%~dp0"

REM NeoForge build to launch. Keep it identical to the greenlanterns TLauncher client.
set "NEOFORGE=21.1.265"

REM NeoForge 1.21.1 needs Java 21. The system default here is Java 25, so we
REM use the Java 21 runtime that ships with the Minecraft launcher instead.
set "JAVA=%APPDATA%\.minecraft\runtime\java-runtime-delta\windows\java-runtime-delta\bin\java.exe"
if not exist "%JAVA%" (
  echo [WARN] Java 21 not found at:
  echo        %JAVA%
  echo        Falling back to "java" on PATH. NeoForge 1.21.1 expects Java 21.
  set "JAVA=java"
)

"%JAVA%" @user_jvm_args.txt @libraries/net/neoforged/neoforge/%NEOFORGE%/win_args.txt nogui %*

REM Clean "stop" exits with code 0 and the window closes. A crash keeps it open so you can read it.
if errorlevel 1 (
  echo.
  echo [!] Server exited with an error. Check logs\latest.log and crash-reports\
  pause
)

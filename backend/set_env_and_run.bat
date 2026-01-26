@echo off
REM Set encoding environment variables
set PGCLIENTENCODING=UTF8
set PYTHONIOENCODING=utf-8

REM Run the command passed as argument
%*

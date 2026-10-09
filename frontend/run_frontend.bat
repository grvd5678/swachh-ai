@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo Starting Swachh.ai Frontend (Next.js 16)...
echo ========================================================
npm.cmd run dev
pause


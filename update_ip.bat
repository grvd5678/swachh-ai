@echo off
set /p NEW_IP="Enter new Fargate IP: "
echo NEXT_PUBLIC_API_URL=http://%NEW_IP%:8000 > frontend\.env.local
echo Updated frontend\.env.local to http://%NEW_IP%:8000
echo.
echo Now restart npm run dev OR redeploy Vercel with new env var.
pause

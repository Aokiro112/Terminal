@echo off
echo Starting Advanced Terminal...

start "Django Server" cmd /k "cd C:\Terminal\backend && python manage.py runserver 8000"

timeout /t 3 /nobreak > nul

start "Node.js Server" cmd /k "cd C:\Terminal\node-server && node server.js"

timeout /t 3 /nobreak > nul

start "Terminal Client" cmd /k "cd C:\Terminal\shell && python client.py"

echo All servers started!
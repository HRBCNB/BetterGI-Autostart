@echo off
:: 设置代码页为 UTF-8
chcp 65001 >nul

:: 管理员权限检测
NET SESSION >nul 2>&1
if %errorlevel% neq 0 (
    echo 请右键以管理员身份运行此脚本！
    pause
    exit /b 1
)


:: ==============================
:: 先搜索并关闭后台进程
:: ==============================
echo.
echo ==============================
echo 开始关闭后台程序
echo ==============================

call :KillByKeyword "QQ"
call :KillByKeyword "Afterburner"
call :KillByKeyword "RivaTuner"
call :KillByKeyword "YuanShen"
call :KillByKeyword "BetterGI"

echo.
echo 后台程序处理完成。
echo.


:: ==============================
:: 停止 Windows Audio 服务
:: ==============================
echo 正在停止系统音频服务……

net start | find "Windows Audio" >nul

if errorlevel 1 (
    echo 音频服务当前未运行，无需停止。
) else (
    net stop Audiosrv /y

    if errorlevel 1 (
        echo 音频服务停止过程中出现异常。
        echo 等待确认状态……
        timeout /t 2 >nul
    ) else (
        echo 音频服务已停止。
    )
)


:: ==============================
:: 最小化所有窗口
:: ==============================
echo.
echo 正在最小化所有窗口……

powershell -NoProfile -Command "(New-Object -ComObject Shell.Application).MinimizeAll()"

timeout /t 1 /nobreak >nul


:: ==============================
:: 启动 BetterGI
:: ==============================
echo.
echo 正在启动 BetterGI……

cd /d "D:\Program Files\BetterGI"

if not exist "BetterGI.exe" (
    echo 找不到 BetterGI.exe！
    goto RestoreAudio
)

.\BetterGI.exe --startOneDragon 默认配置


:: ==============================
:: 恢复 Windows Audio 服务
:: ==============================
:RestoreAudio

echo.
echo 正在恢复系统音频服务……

net start Audiosrv

if errorlevel 1 (
    echo 音频服务启动失败，或者已经运行。
) else (
    echo 音频服务已恢复。
)


echo.
echo 脚本执行完毕。
exit


:: ==============================
:: 按关键字模糊搜索并关闭进程
:: ==============================
:KillByKeyword

echo.
echo ===== 搜索包含 "%~1" 的进程 =====

set "found=0"

for /f "tokens=1 delims=," %%i in ('
    tasklist /FO CSV /NH ^| findstr /I "%~1"
') do (
    set "found=1"
    echo 正在关闭：%%~i
    taskkill /F /IM "%%~i"
)

if "%found%"=="0" (
    echo 没有找到包含 "%~1" 的进程。
)

exit /b
import subprocess
from time import sleep
import pyautogui
import psutil
import os
import sys
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import win32com.client
import time


def show_desktop():
    """
    最小化所有窗口，显示桌面
    """
    shell = win32com.client.Dispatch("Shell.Application")
    shell.MinimizeAll()


def mute_default_speaker(mute=True):
    """
    静音或取消静音默认扬声器
    :param mute: True 静音，False 取消静音
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1 if mute else 0, None)


def find_and_kill_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 模糊匹配进程名（不区分大小写）
            if process_name.lower() in proc.info['name'].lower():
                print(f"检测到进程: {proc.info['name']} (PID: {proc.info['pid']})")

                # 1. 首先尝试优雅终止
                proc.terminate()

                try:
                    # 2. 等待进程结束，时间改为 10 秒
                    print(f"正在等待进程退出 (最多等待 10s)...")
                    proc.wait(timeout=3)
                    print(f"进程 {proc.info['name']} 已安全关闭。")

                except psutil.TimeoutExpired:
                    # 3. 如果 3 秒后还没关掉，则强制杀掉
                    print(f"等待超时，正在强制中止进程: {proc.info['name']}...")
                    proc.kill()
                    # 再次确认是否杀掉（通常 kill 是即时的）
                    proc.wait(timeout=2)
                    print(f"进程 {proc.info['name']} 已被强制中止。")

                print(f"检测到进程: {proc.info['name']} (PID: {proc.info['pid']})")

                # 1. 首先尝试优雅终止
                proc.terminate()

                try:
                    # 2. 等待进程结束
                    print(f"正在等待进程退出 (最多等待 3s)...")
                    proc.wait(timeout=3)
                    print(f"进程 {proc.info['name']} 已安全关闭。")

                except psutil.TimeoutExpired:
                    # 3. 如果 3 秒后还没关掉，则强制杀掉
                    print(f"等待超时，正在强制中止进程: {proc.info['name']}...")
                    proc.kill()
                    proc.wait(timeout=2)
                    print(f"进程 {proc.info['name']} 已被强制中止。")

        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            print(
                f"权限不足，无法操作进程: {proc.info['name']} (PID: {proc.info['pid']})。请尝试以管理员身份运行脚本。")
        except psutil.ZombieProcess:
            print(f"发现僵尸进程 {proc.info['name']}，跳过。")
        except Exception as e:
            print(f"操作进程时发生错误: {e}")
            print(f"操作进程时发生错误: {e}")


def read_config(file_path):
    coordinates = []
    exe_path = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取第一行作为exe路径
        exe_path = file.readline().strip()
        # 读取剩余部分作为坐标
        for line in file:
            line = line.strip()
            if line:  # 跳过空行
                if line.startswith('#'):  # 跳过注释
                    continue
                try:
                    x, y = map(int, line.split(','))
                    coordinates.append((x, y))
                except ValueError:
                    print(f"跳过无效的坐标行: {line}")
    return exe_path, coordinates


def click_coordinates(coordinates):
    for coord in coordinates:
        x, y = coord
        print(f"点击: {x}, {y}")
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        sleep(1)


if __name__ == "__main__":
    # 显示桌面
    print("正在最小化所有窗口...")
    time.sleep(1)
    show_desktop()
    print("已显示桌面！")

    # 静音
    mute_default_speaker(True)

    # 关闭监控软件
    print('正在清理冲突进程...')
    find_and_kill_process('MSIAfterburner')
    find_and_kill_process('RivaTunerStatisticsServer')

    # 关闭 BetterGI 相关
    find_and_kill_process('bettergi')
    find_and_kill_process('yuanshen')

    # 关闭QQ vx 防止弹窗干扰
    find_and_kill_process('QQ.exe')
    find_and_kill_process('WeChat')

    # 获取路径
    base_dir = os.path.dirname(sys.executable if getattr(
        sys, 'frozen', False) else __file__)
    config_path = os.path.join(base_dir, "config.txt")

    if not os.path.exists(config_path):
        print(f"错误: 找不到配置文件 {config_path}")
        sys.exit(1)

    # 读取并启动
    exe_path, coords = read_config(config_path)

    if exe_path and os.path.exists(exe_path):
        print(f"启动目标程序: {exe_path}")
        subprocess.Popen(exe_path)
        # 等待启动
        sleep(10)
        # 执行点击
        click_coordinates(coords)
    else:
        print(f"错误: 无法找到可执行文件路径，请检查 config.txt 第一行。")


# [一键打包并分发]
# pyinstaller -F -w --clean ./src/auto_start.py ; cp ./dist/auto_start.exe "./每日任务/" ; cp ./dist/auto_start.exe "./自动锄地/"

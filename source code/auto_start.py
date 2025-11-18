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
                print(f"正在终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
                p = psutil.Process(proc.info['pid'])
                p.terminate()  # 尝试优雅终止
                p.wait(timeout=3)  # 等待3秒确认结束
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            print(f"权限不足，无法终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
        except Exception as e:
            print(f"终止进程时发生错误: {e}")


def read_config(file_path):
    coordinates = []
    exe_path = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取第一行作为exe路径
        exe_path = file.readline().strip()
        # 读取剩余部分作为坐标
        for line in file:
            if line.strip():  # 跳过空行
                if line.strip().startswith('#'):  # 跳过注释
                    continue
                x, y = map(int, line.strip().split(','))
                coordinates.append((x, y))
    return exe_path, coordinates


def click_coordinates(coordinates):
    for coord in coordinates:
        x, y = coord
        print(f"点击: {x}, {y}")
        pyautogui.moveTo(x, y, duration=0.5)  # 移动到指定位置，duration为移动时间
        pyautogui.click()
        sleep(1)


if __name__ == "__main__":
    #显示桌面
    print("正在最小化所有窗口...")
    time.sleep(1)  # 可以延迟1秒，看效果
    show_desktop()
    print("已显示桌面！")

     #静音
    mute_default_speaker(True)

    #关闭小飞机
    print('尝试关闭微星小飞机进程')
    find_and_kill_process('MSIAfterburner')
    find_and_kill_process('RivaTunerStatisticsServer')


    # 关闭原神与BetterGI进程
    print('尝试关闭原神与BetterGI进程')
    find_and_kill_process('yuanshen')
    find_and_kill_process('bettergi')

    #关闭Snipaste截图程序
    find_and_kill_process('Snipaste')

    # 获取当前脚本或exe文件所在目录，保证能正确读取config.txt
    base_dir = os.path.dirname(sys.executable if getattr(
        sys, 'frozen', False) else __file__)
    config_path = os.path.join(base_dir, "config.txt")

    # 读取配置文件，获取要打开的exe路径和坐标列表
    exe_path, coords = read_config(config_path)

    # 启动指定的.exe文件
    print(f"启动BetterGI: {exe_path}")
    process = subprocess.Popen(exe_path)

    # 等待几秒以确保应用程序已完全启动，这里设置为5秒，可以根据实际情况调整
    sleep(5)

    # 执行点击操作
    click_coordinates(coords)

    #pyinstaller --onefile auto_start.py


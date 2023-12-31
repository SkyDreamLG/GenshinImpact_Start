import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    import os
    import win32gui
    import win32print
    import win32con
    import cv2
    import numpy as np
    import psutil
    import pyautogui
    from PIL import ImageGrab
    from PIL import Image
    print('运行本程序前请确保原神游戏内图像设置已设置为独占全屏，否则会导致效果不佳')
    print('如果运行后原神游戏程序未被成功拉起，请检查游戏主程序路径是否已经正确设置')
    print('已设置的游戏主程序路径信息保存在本程序所在位置下的“yuanshen_path.txt”文件中')
    print('如发现设置错误，请手动修改该文件内容至正确路径或再次运行本程序并在询问是否重新设置游戏主程序文件路径时选择是以重新设置路径为正确位置')
    input('按回车键继续')

    # 检查原神是否已经启动
    if os.system('tasklist /FI "IMAGENAME eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0:
        print("原神 已在运行!")
        os.system('pause')
        exit()


    # 定义设置原神游戏路径功能函数
    def ys_path():
        path = str(input('请输入原神游戏主程序文件绝对路径（不要带有引号）：'))  # 获取用户输入的路径数据并写入变量
        with open('yuanshen_path.txt', 'w') as path_save:
            path_save.write(path)
        return path

    # 尝试读取路径记录文件
    try:
        # 打开路径记录文件
        with open('yuanshen_path.txt') as path_save:
            path_0 = path_save.read()  # 读取文件
            path = path_0.rstrip()  # 去除读取路径结尾空行并将路径数据写入对应变量
        try:
            user_choose = str(input('是否重新设置原神主程序游戏文件绝对路径？（Y/N）：'))  # 获取用户意愿
            user_choose = user_choose.lower()  # 将用户输入转化为小写
            if user_choose == 'y':  # 若用户输入为是，则执行重置函数
                ys_path()
            else:  # 若用户输入为否，则跳过
                print('已跳过')
                input('按回车键继续')
        except:  # 防止用户输入错误值，若输入错误则视为跳过
            print('已跳过')
            input('按回车键继续')
    except:
        print('错误：原神游戏主程序文件路径未指定，请指定原神游戏主程序文件位置')
        ys_path()

    # 获取屏幕分辨率
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

    pyautogui.FAILSAFE = False  # 关闭FailSafe

    while True:
        # 截图
        screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, w, h))), cv2.COLOR_BGR2RGB)
        # 计算屏幕白色像素比例
        white_pixels = np.count_nonzero(screenshot >= [250, 250, 250])
        total_pixels = screenshot.shape[0] * screenshot.shape[1]
        white_percentage = white_pixels / total_pixels * 100
        print(f"屏幕含原量{white_percentage}%")
        # 判断是否满足启动条件
        if white_percentage >= 90:
            break

    # 创建白色过渡图片，以等待原神程序加载

    img = Image.new("RGB", (w, h), (255, 255, 255))
    img.save("1.jpg")
    img = cv2.imread("1.jpg")
    out_win = "output_style_full_screen"
    cv2.namedWindow(out_win, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(out_win, img)

    print(path)
    # 原神，启动！
    os.startfile(path)
    cv2.waitKey(10000)
    print('原神，启动！！！！')
    for proc in psutil.process_iter():
        if proc.name() == 'YuanShen.exe':
            print('原神已启动！！！！')
            break


else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)  # 以管理员权限重新运行程序
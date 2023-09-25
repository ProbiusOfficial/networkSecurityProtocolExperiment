import winreg as reg
import ctypes

def modify_registry():

    # 初始化值项dword的值为None。
    dword_value = None

    # 用RegOpenKeyEx() 函数打开注册表项:
    try:
        key = reg.OpenKeyEx(
            reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Test",
            0,
            reg.KEY_ALL_ACCESS
        )
        print("项 DisableRegistryTools 已经存在!")
        new_key = False
    except FileNotFoundError:
        # 如果该注册表项不存在，则用RegCreateKeyEx() 函数创建该项。
        key = reg.CreateKeyEx(
            reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Test",
            0,
            reg.KEY_ALL_ACCESS
        )
        print("项 DisableRegistryTools 不存在，已经创建!")
        new_key = True

    # 如果该项为新创建的，则新建立一个REG_SZ值项DisableChangePassword和一个REG_DWORD值项dword。
    if new_key:
        reg.SetValueEx(key, "DisableChangePassword", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "dword", 0, reg.REG_DWORD, 0)
    else:
        # 如果该值项已经存在，则用RegQueryValueEx() 读取值项DisableRegistryTools的dword的值。
        try:
            dword_value, _ = reg.QueryValueEx(key, "dword")
        except FileNotFoundError:
            dword_value = None
   
    # 用wsprintf() 和MessageBox() 函数把项值显示在屏幕上。
    message = f"项 DisableRegistryTools 的值: {dword_value}" if dword_value is not None else "项 DisableRegistryTools 未找到或未设置!"
    ctypes.windll.user32.MessageBoxW(0, message, "注册表值", 1)

    # 将值项dword的值置为1。
    reg.SetValueEx(key, "dword", 0, reg.REG_DWORD, 1)

    # 用RegFlushKey() 函数将对注册表项的修改写入注册表。
    reg.FlushKey(key)

    # 用RegCloseKey() 函数关闭打开的注册表项。
    reg.CloseKey(key)

# 执行函数
modify_registry()

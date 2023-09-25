#include <windows.h>
#include <iostream>
#include <string>

int main() {
    HKEY hKey;
    LONG result;
    DWORD dwType = REG_DWORD;
    DWORD dwValue;
    DWORD dwSize = sizeof(DWORD);
    wchar_t message[256];

    // 打开或创建注册表项
    result = RegOpenKeyEx(HKEY_CURRENT_USER, TEXT("Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"), 0, KEY_ALL_ACCESS, &hKey);
    if (result == ERROR_FILE_NOT_FOUND) {
        result = RegCreateKeyEx(HKEY_CURRENT_USER, TEXT("Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"), 0, NULL, REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, NULL, &hKey, NULL);
        if (result != ERROR_SUCCESS) {
            MessageBox(NULL, TEXT("Failed to create registry key"), TEXT("Error"), MB_OK);
            return 1;
        }
        RegSetValueEx(hKey, TEXT("DisableChangePassword"), 0, REG_SZ, (BYTE *)"", sizeof(""));
        dwValue = 0;
        RegSetValueEx(hKey, TEXT("dword"), 0, REG_DWORD, (BYTE *)&dwValue, sizeof(dwValue));
    } else {
        RegQueryValueEx(hKey, TEXT("DisableRegistryTools"), NULL, &dwType, (BYTE *)&dwValue, &dwSize);
    }

    // 使用 wsprintf 显示值
    wsprintf(message, TEXT("DisableRegistryTools value: %d"), dwValue);
    MessageBox(NULL, message, TEXT("Registry Value"), MB_OK);

    // 修改 dword 值
    dwValue = 1;
    RegSetValueEx(hKey, TEXT("dword"), 0, REG_DWORD, (BYTE *)&dwValue, sizeof(dwValue));

    // 关闭注册表项
    RegCloseKey(hKey);

    return 0;
}

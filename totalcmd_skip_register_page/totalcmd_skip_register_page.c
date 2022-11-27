#include "windows.h"
#include <stdio.h>


BOOL CALLBACK EnumChildProc(HWND hwnd, LPARAM lParam) {
    static char target_control_idx = 3;
    static char current_control_idx = 0;
    static TCHAR szWndTitle[1024];

    if (current_control_idx == target_control_idx) {
        int nLen = GetWindowText(hwnd, szWndTitle, sizeof(szWndTitle));
        if (nLen) {
            *(char *) lParam = *(char *) szWndTitle;
            return FALSE;
        }
    }
    ++current_control_idx;
    return TRUE;
}


int main(void) {
    char *totalcmd_path = "d:\\software\\totalcmd\\TOTALCMD64.EXE";
    char *totalcmd_class_name = "TNASTYNAGSCREEN";
    int sleep_time = 1000;
    char num;

    popen(totalcmd_path, "r");
    Sleep(sleep_time);

    HWND hwnd = FindWindow(TEXT(totalcmd_class_name), NULL);
    EnumChildWindows(hwnd, EnumChildProc, (LPARAM) &num);

    int key;
    if (num == '1') {
        key = VK_NUMPAD1;
    } else if (num == '2') {
        key = VK_NUMPAD2;
    } else if (num == '3') {
        key = VK_NUMPAD3;
    }

    PostMessage(hwnd, WM_KEYDOWN, key, 0);
    return 0;
}
import pyautogui
import keyboard
import time

def move_cursor(x, y, speed):
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x + x * speed, current_y + y * speed)

def click_middle():
    pyautogui.click(button='middle')

def select_area():
    pyautogui.mouseDown(button='left')

mouse_control_enabled = True
move_speed = 10       # Обычная скорость мыши
accelerated_speed = 55  # Ускоренная скорость мыши
hold_time_threshold = 0.5  # Порог перед ускорением мыши

scroll_speed = 10  # Скорость прокрутки колесика

blocked_keys = set()

def toggle_mouse_control():
    global mouse_control_enabled
    mouse_control_enabled = not mouse_control_enabled
    print(f"Управление мышью {'включено' if mouse_control_enabled else 'выключено'}")

keyboard.add_hotkey('caps lock', toggle_mouse_control)

def suppress_key(key):
    keyboard.block_key(key)
    blocked_keys.add(key)

keys_to_suppress = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right', 'z', 'x', 'c', 'v', 'b', 'q']

for key in keys_to_suppress:
    suppress_key(key)

def main():
    print("Нажмите 'Caps Lock' для отключения/включения управления мышью.")
    print("Нажмите 'z/я' для ЛКМ мыши.")
    print("Нажмите 'x/ч' для ПКМ мыши.")
    print("Нажмите 'c/с' для колесика мыши вниз.")
    print("Нажмите 'v/м' для колесика мыши вверх.")
    print("Нажмите 'b/и' для клика по колесицу мыши.")
    print("Зажмите 'q/й' и двигайтесь для выделения области.")
    print("Для выхода из приложения, нажмите крестик сверху.")
    print("")
    key_hold_times = {}

    while True:
        if mouse_control_enabled:
            for key in keys_to_suppress:
                keyboard.block_key(key)

            keys = keys_to_suppress
            for key in keys:
                if keyboard.is_pressed(key):
                    if key not in key_hold_times:
                        key_hold_times[key] = time.time()
                    elapsed_time = time.time() - key_hold_times[key]
                    speed = accelerated_speed if elapsed_time > hold_time_threshold else move_speed

                    if key == 'w' or key == 'up':
                        move_cursor(0, -1, speed)
                    elif key == 'a' or key == 'left':
                        move_cursor(-1, 0, speed)
                    elif key == 's' or key == 'down':
                        move_cursor(0, 1, speed)
                    elif key == 'd' or key == 'right':
                        move_cursor(1, 0, speed)
                    elif key == 'z':
                        pyautogui.click(button='left')
                    elif key == 'x':
                        pyautogui.click(button='right')
                    elif key == 'c':
                        pyautogui.scroll(-scroll_speed)
                    elif key == 'v':
                        pyautogui.scroll(scroll_speed)
                    elif key == 'b':
                        click_middle()
                    elif key == 'q':
                        select_area()
                else:
                    if key in key_hold_times:
                        del key_hold_times[key]
        else:
            for key in blocked_keys:
                keyboard.unblock_key(key)
            blocked_keys.clear()

if __name__ == "__main__":
    main()

# os_info.py
import platform
import subprocess
from datetime import datetime

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def run_cmd(cmd):
    """Безопасный запуск команды."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, encoding='utf-8', errors='ignore', timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def detect_device_type():
    """Определяет, ноутбук это или стационарный ПК."""
    if HAS_PSUTIL:
        try:
            bat = psutil.sensors_battery()
            if bat is not None:
                return "💻 Ноутбук"
        except Exception:
            pass
    system = platform.system()
    # Дополнительная проверка для Windows/Linux через chassis type
    if system == "Windows":
        chassis = run_cmd('wmic systemenclosure get chassistypes')
        if "8" in chassis or "9" in chassis or "10" in chassis or "14" in chassis:
            return "💻 Ноутбук"
    elif system == "Linux":
        chassis = run_cmd("cat /sys/class/dmi/id/chassis_type 2>/dev/null")
        try:
            if int(chassis) in (8, 9, 10, 14):
                return "💻 Ноутбук"
        except Exception:
            pass
    elif system == "Darwin":
        model = run_cmd("sysctl -n hw.model")
        if "Book" in model or "MacBook" in model:
            return "💻 Ноутбук"
    return "🖥️ Стационарный ПК"


def get_os_info():
    """Собирает полную информацию об ОС и железе."""
    info = {}

    info["Тип устройства"] = detect_device_type()
    info["Имя устройства"] = platform.node() or "Неизвестно"
    info["Тип системы"] = f"{platform.system()} ({platform.machine()})"
    info["Выпуск ОС"] = platform.release()
    info["Версия ОС"] = platform.version() or "Неизвестно"
    info["Процессор"] = platform.processor() or "Неизвестно"

    if HAS_PSUTIL:
        try:
            freq = psutil.cpu_freq()
            freq_str = f"{freq.max:.0f} МГц" if freq else "N/A"
            info["Ядра / потоки"] = f"{psutil.cpu_count(logical=False)} / {psutil.cpu_count(logical=True)}"
            info["Частота CPU"] = freq_str
            info["ОЗУ (всего)"] = f"{psutil.virtual_memory().total / (1024**3):.2f} ГБ"
            # Информация о батарее
            bat = psutil.sensors_battery()
            if bat is not None:
                info["Батарея: заряд"] = f"{bat.percent:.0f}%"
                info["Батарея: статус"] = "🔌 Заряжается" if bat.power_plugged else "🔋 От сети"
        except Exception:
            pass

    system = platform.system()

    # ============= WINDOWS =============
    if system == "Windows":
        # Модель устройства и производитель
        model = run_cmd('wmic csproduct get name,vendor')
        model_lines = [l.strip() for l in model.splitlines()
                       if l.strip() and "Name" not in l and "Vendor" not in l]
        if model_lines:
            info["Модель / производитель"] = model_lines[0]

        gpu = run_cmd('wmic path win32_VideoController get name')
        gpu_lines = [l.strip() for l in gpu.splitlines()
                     if l.strip() and l.strip() != "Name"]
        info["Видеопроцессор"] = ", ".join(gpu_lines) if gpu_lines else "Неизвестно"

        uuid = run_cmd('wmic csproduct get uuid')
        uuid_lines = [l.strip() for l in uuid.splitlines()
                      if l.strip() and l.strip() != "UUID"]
        info["Код устройства"] = uuid_lines[0] if uuid_lines else "Неизвестно"

        pid = run_cmd('wmic os get serialnumber')
        pid_lines = [l.strip() for l in pid.splitlines()
                     if l.strip() and l.strip() != "SerialNumber"]
        info["Код продукта"] = pid_lines[0] if pid_lines else "Неизвестно"

        os_data = run_cmd('wmic os get installdate,buildnumber')
        os_lines = [l.strip() for l in os_data.splitlines()
                    if l.strip() and "InstallDate" not in l and "BuildNumber" not in l]
        if os_lines:
            parts = os_lines[0].split()
            if len(parts) >= 2:
                info["Сборка установки"] = parts[0]
                try:
                    date_str = parts[1][:8]
                    dt = datetime.strptime(date_str, "%Y%m%d")
                    info["Дата установки"] = dt.strftime("%d.%m.%Y")
                except Exception:
                    info["Дата установки"] = parts[1]
            elif len(parts) == 1:
                info["Сборка установки"] = parts[0]
                info["Дата установки"] = "Неизвестно"

    # ============= LINUX =============
    elif system == "Linux":
        info["Модель / производитель"] = (
            run_cmd("cat /sys/class/dmi/id/sys_vendor 2>/dev/null") + " " +
            run_cmd("cat /sys/class/dmi/id/product_name 2>/dev/null")
        ).strip() or "Неизвестно"

        gpu = run_cmd("lspci | grep -iE 'vga|3d' | head -1")
        info["Видеопроцессор"] = gpu if gpu else "Неизвестно"

        uuid = run_cmd("cat /sys/class/dmi/id/product_uuid")
        info["Код устройства"] = uuid if uuid else "Неизвестно"

        info["Код продукта"] = run_cmd("cat /sys/class/dmi/id/product_name") or "Неизвестно"
        info["Дата установки"] = run_cmd("stat -c %y / 2>/dev/null | cut -d' ' -f1") or "Неизвестно"
        info["Сборка установки"] = run_cmd("uname -r") or "Неизвестно"

    # ============= MACOS =============
    elif system == "Darwin":
        info["Модель / производитель"] = run_cmd(
            'system_profiler SPHardwareDataType | grep "Model Name" | cut -d: -f2'
        ).strip() or "Apple"

        gpu = run_cmd("system_profiler SPDisplaysDataType | grep Chipset")
        info["Видеопроцессор"] = gpu.replace("Chipset Model:", "").strip() if gpu else "Неизвестно"

        uuid = run_cmd("system_profiler SPHardwareDataType | grep UUID")
        info["Код устройства"] = uuid.split(":")[-1].strip() if uuid else "Неизвестно"
        info["Код продукта"] = "Не применимо (macOS)"
        info["Сборка установки"] = run_cmd("sw_vers -buildVersion") or "Неизвестно"
        info["Дата установки"] = run_cmd("stat -f %SB -t %Y-%m-%d /") or "Неизвестно"

    return info

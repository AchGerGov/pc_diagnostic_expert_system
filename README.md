# 🖥️ Экспертная система диагностики ПК и ноутбуков

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge)
![Rules](https://img.shields.io/badge/Правил-159-00E5FF?style=for-the-badge)
![Platform](https://img.shields.io/badge/Платформа-Windows%20%7C%20Linux%20%7C%20macOS-4FC3F7?style=for-the-badge)
![License](https://img.shields.io/badge/Лицензия-Учебный%20проект-9E9E9E?style=for-the-badge)

**Гибридная интеллектуальная система для диагностики компьютерной техники**  
Продукционная экспертная система + NLP-распознавание + умный поиск по базе знаний


</div>


---

##  О проекте

**Экспертная система диагностики** — это приложение, которое помогает пользователю самостоятельно определить причину неисправности компьютера или ноутбука и получить пошаговый план действий по её устранению.

Система работает на основе **продукционной модели знаний** — формата «ЕСЛИ (симптомы) → ТО (диагноз)». Каждое правило описывает конкретную неисправность, а механизм вывода сопоставляет введённые симптомы с базой знаний и выдаёт наиболее вероятные причины.

###  Зачем это нужно?

- **Пользователю** — быстро найти причину поломки без вызова мастера.
- **Начинающему мастеру** — получить структурированный чек-лист диагностики.
- **Студенту** — наглядный пример гибридной интеллектуальной системы в области IT.

###  Учебная ценность

Проект демонстрирует применение:
- **продукционной модели** знаний (классический подход к экспертных системам);
- **нечёткого вывода** (ранжирование правил по проценту совпадения);
- **обработки естественного языка** (стемминг, токенизация);
- **интеллектуального поиска** (ранжирование по релевантности);
- **кроссплатформенной разработки** (Windows, Linux, macOS).

---

##  Ключевые возможности

###  Модуль «Диагностика»
- **159 продукционных правил**, покрывающих ПК и ноутбуки всех брендов.
- **Переключатель типа устройства** (🖥️ ПК / 💻 Ноутбук) — система показывает только релевантные симптомы.
- **ИИ-распознавание текста** — опишите проблему словами, система сама отметит нужные симптомы.
- **Ранжирование диагнозов** по проценту совпадения с визуальной шкалой.
- **Пошаговые рекомендации** — конкретные действия, а не общие фразы.

### Модуль «Информация о системе»
- Автоматическое определение **типа устройства** (ПК или ноутбук).
- Модель, производитель, серийный номер (HP, Dell, Lenovo, ASUS, Acer, MSI, Apple и др.).
- Характеристики процессора, ОЗУ, видеокарты.
- Данные об ОС: выпуск, версия, дата установки, сборка.
- **Для ноутбуков** — состояние и заряд аккумулятора.
- Полная поддержка **Windows / Linux / macOS**.

###  Модуль «База знаний (ИИ)»
- **40+ статей** по устройству ПК, диагностике, профилактике и апгрейду.
- **Умный поиск** с ранжированием по релевантности.
- **Стемминг русского языка** — система понимает разные формы слов.
- **Быстрые подсказки** — чипы популярных вопросов в один клик.

###  Интерфейс
- **Тёмная тема** с неоновой подсветкой (#00E5FF).
- **Три вкладки** в одном окне — без переключения между приложениями.
- **Прокрутка** длинных списков и текстов.
- **Кастомные кнопки** с закруглёнными углами и hover-эффектами.
- **Шрифт Consolas** для читаемости технической информации.

---

### Принцип работы диагностики
Пользователь → Симптомы → Сопоставление с правилами → Ранжирование → Рекомендации

Каждое правило проверяет: все ли его условия есть среди симптомов, % совпадения = (совпало / всего) × 100; Сортировка по убыванию процента

---

### Требования
- **Python 3.8** или выше
- **Tkinter** (входит в стандартную поставку Python)
- **psutil** — для сбора информации о железе

---

##  Быстрый старт: клонирование, настройка, сборка и запуск

Проект не требует «сборки» в классическом смысле (нет компиляции) — достаточно установить зависимости и запустить главный файл. Ниже — три сценария: **Windows**, **Linux/macOS** и **WSL Ubuntu**.

---

###  Шаг 1. Клонирование репозитория

Откройте терминал (или Git Bash на Windows) и выполните:

```bash
git clone https://github.com/AchErGov/pc_diagnostic_expert_system.git
cd pc_diagnostic_expert_system
```

Если Git не установлен:

- **Windows:** скачайте с [git-scm.com](https://git-scm.com/download/win) и установите.
- **Ubuntu/Debian:** `sudo apt install -y git`
- **macOS:** `brew install git`

---

###  Шаг 2. Проверка версии Python

Убедитесь, что у вас **Python 3.8 или выше**:

```bash
python --version
# или, если python не в PATH:
python3 --version
```

Если Python не установлен:

- **Windows:** скачайте с [python.org](https://www.python.org/downloads/). При установке **обязательно** поставьте галочку «Add Python to PATH».
- **Ubuntu/Debian:** `sudo apt install -y python3 python3-pip python3-venv python3-tk`
- **macOS:** `brew install python-tk`

>  Пакет `python3-tk` содержит библиотеку Tkinter, на которой построен интерфейс. Без него приложение не запустится.

---

###  Шаг 3. Создание виртуального окружения

Виртуальное окружение изолирует зависимости проекта от системных — это хорошая практика.

**Windows (PowerShell или CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS / WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
```

После активации в начале строки терминала появится `(venv)` — это значит, что окружение работает.

---

### 📥 Шаг 4. Установка зависимостей

Все зависимости перечислены в файле `requirements.txt`. Установите их одной командой:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Что установится:**
- `psutil` — библиотека для сбора данных о системе (CPU, ОЗУ, батарея).

Остальные модули (`tkinter`, `platform`, `subprocess`) входят в стандартную библиотеку Python.

**Проверка установки:**
```bash
python -c "import psutil; print('psutil', psutil.__version__)"
```
Должно вывести версию, например `psutil 5.9.8`.

---

### 🧪 Шаг 5. Быстрая проверка структуры проекта

Убедитесь, что все файлы на месте:

```bash
ls
# или на Windows:
dir
```

Ожидаемый список:

```
gui.py               knowledge_base.py     requirements.txt
inference_engine.py  main.py               rules.py
nlp_processor.py     os_info.py            smart_search.py
utils.py             README.md             LICENSE
.gitignore           requirements-dev.txt
```

---

###  Шаг 6. Запуск приложения

```bash
python main.py
```

Через 1–2 секунды откроется окно с тремя вкладками:

- ** Диагностика** — выбор симптомов и получение рекомендаций.
- ** Информация о системе** — автоопределение параметров вашего устройства.
- ** База знаний (ИИ)** — умный поиск по 40+ статьям.

**Чтобы закрыть приложение** — просто закройте окно. В терминале выполните `deactivate` для выхода из виртуального окружения.

---

##  Отдельно: запуск в WSL Ubuntu

Если вы работаете в **Windows 11** и хотите запустить проект в Linux-окружении (например, чтобы проверить кроссплатформенность):

**1. Установите WSL и Ubuntu (если ещё не установлены):**
```powershell
wsl --install -d Ubuntu
```
Перезагрузите компьютер и запустите Ubuntu из меню Пуск.

**2. Обновите систему и установите зависимости:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-tk git
```

**3. Клонируйте и запустите проект:**
```bash
cd ~
git clone https://github.com/AchErGov/pc_diagnostic_expert_system.git
cd pc_diagnostic_expert_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Благодаря **WSLg** (встроен в Windows 11) окно приложения отобразится прямо поверх Windows — без дополнительных X-серверов.

>  **На Windows 10** потребуется установить X-сервер (например, VcXsrv) и задать переменную `$DISPLAY`. Подробная инструкция — в разделе [Troubleshooting](#-возможные-проблемы).

---

##  Запуск на macOS

```bash
# Установка Homebrew (если ещё нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка Python
brew install python-tk

# Клонирование и запуск
git clone https://github.com/AchErGov/pc_diagnostic_expert_system.git
cd pc_diagnostic_expert_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

>  На macOS Tkinter иногда конфликтует с системным Python. Если возникнут проблемы — установите Python через `brew` и используйте его.

---

##  Обновление проекта до последней версии

Если репозиторий обновлялся и вы хотите получить свежие изменения:

```bash
cd pc_diagnostic_expert_system
git pull origin main
pip install -r requirements.txt
python main.py
```

---

##  Полное удаление проекта (если понадобится)

```bash
# Удалить папку с проектом
cd ..
rm -rf pc_diagnostic_expert_system

# Windows:
rmdir /s /q pc_diagnostic_expert_system
```

---

## ⚙️ Возможные проблемы

###  `ModuleNotFoundError: No module named 'psutil'`
**Причина:** зависимости не установлены или активировано не то окружение.
**Решение:**
```bash
pip install -r requirements.txt
```

###  `ModuleNotFoundError: No module named 'tkinter'`
**Причина:** не установлен пакет Tkinter.
**Решение:**
- **Ubuntu/Debian:** `sudo apt install -y python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **macOS:** `brew install python-tk`
- **Windows:** переустановите Python с галочкой «tcl/tk and IDLE».

###  `_tkinter.TclError: no display name and no $DISPLAY environment variable`
**Причина:** WSL без WSLg (обычно Windows 10) или запуск по SSH без X11-forwarding.
**Решение:** установите X-сервер (VcXsrv) и задайте переменную:
```bash
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
```

###  `ModuleNotFoundError: No module named 'nlp_processor'`
**Причина:** файл называется `nip_processor.py` вместо `nlp_processor.py` (опечатка).
**Решение:** переименуйте файл или обновите репозиторий до последней версии.

###  Приложение запускается, но окно не появляется
**Причина:** графическая подсистема недоступна.
**Решение:** проверьте `echo $DISPLAY` (на Linux/WSL должно быть непустым) или запустите проект на «живой» Windows.

###  `pip: command not found`
**Причина:** pip не установлен или не в PATH.
**Решение:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

##  Краткая шпаргалка

Скопируйте один блок — и проект запустится:

**Windows:**
```powershell
git clone https://github.com/AchErGov/pc_diagnostic_expert_system.git
cd pc_diagnostic_expert_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Linux / WSL / macOS:**
```bash
git clone https://github.com/AchErGov/pc_diagnostic_expert_system.git
cd pc_diagnostic_expert_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

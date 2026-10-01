# gui.py
import tkinter as tk
from tkinter import scrolledtext, ttk
from inference_engine import InferenceEngine
from utils import RoundedButton
from nlp_processor import match_symptoms
from knowledge_base import QA_PAIRS
from smart_search import search_knowledge
from os_info import get_os_info


class DiagnosticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Экспертная система диагностики ПК и ноутбуков + ИИ")
        self.root.geometry("1050x820")
        self.root.configure(bg="#0B0C10")
        self.root.resizable(False, False)

        self.font_consolas = ("Consolas", 11)
        self.font_consolas_bold = ("Consolas", 11, "bold")
        self.font_title = ("Consolas", 16, "bold")

        # Движок + выбор устройства
        self.current_device = "pc"
        self.engine = InferenceEngine(device=self.current_device)
        self.all_conditions = self.engine.all_conditions
        self.check_vars = {}

        self._setup_style()
        self.create_widgets()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background="#1A1A2E", borderwidth=0, tabmargins=[5, 5, 5, 0])
        style.configure('TNotebook.Tab', background="#0B0C10", foreground="#E0E0E0",
                        padding=[22, 10], font=("Consolas", 11, "bold"), borderwidth=0)
        style.map('TNotebook.Tab',
                  background=[('selected', "#00E5FF")],
                  foreground=[('selected', "#0B0C10")])

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#0B0C10")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="⚡ ЭКСПЕРТНАЯ СИСТЕМА ДИАГНОСТИКИ ПК И НОУТБУКОВ ⚡",
                 font=self.font_title, fg="#00E5FF", bg="#0B0C10").pack(pady=(0, 15))

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        self.tab_diagnostic = tk.Frame(self.notebook, bg="#1A1A2E")
        self.tab_system = tk.Frame(self.notebook, bg="#1A1A2E")
        self.tab_knowledge = tk.Frame(self.notebook, bg="#1A1A2E")

        self.notebook.add(self.tab_diagnostic, text="🔍 Диагностика")
        self.notebook.add(self.tab_system, text="💻 Информация о системе")
        self.notebook.add(self.tab_knowledge, text="🧠 База знаний (ИИ)")

        self._build_diagnostic_tab()
        self._build_system_tab()
        self._build_knowledge_tab()

    # ============================================================
    # ВКЛАДКА 1: ДИАГНОСТИКА
    # ============================================================
    def _build_diagnostic_tab(self):
        content = self.tab_diagnostic

        # --- Переключатель устройства ---
        dev_row = tk.Frame(content, bg="#1A1A2E")
        dev_row.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(dev_row, text="Тип устройства:",
                 font=self.font_consolas_bold, fg="#00E5FF", bg="#1A1A2E").pack(side="left", padx=(0, 15))

        self.btn_pc = RoundedButton(
            dev_row, text="🖥️ ПК", command=lambda: self._switch_device("pc"),
            width=120, height=35, corner_radius=10,
            bg_color="#00E5FF", hover_color="#66FFFF",
            text_color="#0B0C10", font_size=12
        )
        self.btn_pc.pack(side="left", padx=5)

        self.btn_laptop = RoundedButton(
            dev_row, text="💻 Ноутбук", command=lambda: self._switch_device("laptop"),
            width=140, height=35, corner_radius=10,
            bg_color="#4A148C", hover_color="#6A1B9A",
            text_color="#FFFFFF", font_size=12
        )
        self.btn_laptop.pack(side="left", padx=5)

        self.device_label = tk.Label(dev_row, text="(активно: ПК)",
                                     font=("Consolas", 10), fg="#9E9E9E", bg="#1A1A2E")
        self.device_label.pack(side="left", padx=15)

        # --- Блок ИИ ---
        ai_frame = tk.Frame(content, bg="#1A1A2E")
        ai_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(ai_frame, text="🧠 Опишите симптомы текстом (ИИ распознает):",
                 font=self.font_consolas, fg="#00E5FF", bg="#1A1A2E").pack(anchor="w")

        input_row = tk.Frame(ai_frame, bg="#1A1A2E")
        input_row.pack(fill="x", pady=5)

        self.text_input = tk.Entry(input_row, font=self.font_consolas, bg="#0B0C10",
                                   fg="white", insertbackground="white", relief="flat",
                                   highlightthickness=1, highlightcolor="#00E5FF")
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_ai = RoundedButton(
            input_row, text="🧠 Распознать",
            command=self.ai_recognize,
            width=140, height=35, corner_radius=10,
            bg_color="#FF4081", hover_color="#FF80AB",
            text_color="#FFFFFF", font_size=12
        )
        self.btn_ai.pack(side="right")

        # --- Чекбоксы ---
        checkbox_frame = tk.Frame(content, bg="#1A1A2E")
        checkbox_frame.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(checkbox_frame, bg="#1A1A2E", highlightthickness=0)
        scrollbar = tk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1A1A2E")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Первое заполнение
        self._populate_checkboxes()

        # --- Кнопки ---
        btn_frame = tk.Frame(content, bg="#1A1A2E")
        btn_frame.pack(pady=10)

        self.btn_diagnose = RoundedButton(
            btn_frame, text="🔍 Диагностировать",
            command=self.perform_diagnosis,
            width=180, height=45, corner_radius=15,
            bg_color="#00E5FF", hover_color="#66FFFF",
            text_color="#0B0C10", font_size=14
        )
        self.btn_diagnose.pack(side="left", padx=15)

        self.btn_reset = RoundedButton(
            btn_frame, text="🔄 Сбросить всё",
            command=self.reset_all,
            width=160, height=45, corner_radius=15,
            bg_color="#FF4081", hover_color="#FF80AB",
            text_color="#FFFFFF", font_size=14
        )
        self.btn_reset.pack(side="left", padx=15)

        # --- Результат ---
        result_frame = tk.Frame(content, bg="#00E5FF", bd=2, relief="flat")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, font=self.font_consolas,
            fg="#E0E0E0", bg="#0B0C10", insertbackground="white",
            height=10, bd=0, highlightthickness=0
        )
        self.result_text.pack(fill="both", expand=True, padx=3, pady=3)
        self.result_text.config(state="disabled")

    def _populate_checkboxes(self):
        """Пересоздаёт чекбоксы по актуальному списку симптомов."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.check_vars = {}
        for condition in self.all_conditions:
            var = tk.BooleanVar()
            self.check_vars[condition] = var
            cb = tk.Checkbutton(
                self.scrollable_frame, text=condition, variable=var,
                font=self.font_consolas, fg="#E0E0E0", bg="#1A1A2E",
                selectcolor="#0B0C10", activebackground="#1A1A2E",
                activeforeground="#00E5FF", relief="flat", bd=0,
                padx=10, pady=5, anchor="w", justify="left", wraplength=850
            )
            cb.pack(fill="x", padx=5, pady=2)

    def _switch_device(self, device):
        """Переключает тип устройства и перестраивает интерфейс."""
        if device == self.current_device:
            return
        self.current_device = device
        self.engine.set_device(device)
        self.all_conditions = self.engine.all_conditions
        self._populate_checkboxes()

        # Обновляем подпись
        name = "ПК" if device == "pc" else "Ноутбук"
        self.device_label.config(text=f"(активно: {name})")

        # Очищаем результат
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")

    # ============================================================
    # ВКЛАДКА 2: ИНФОРМАЦИЯ О СИСТЕМЕ
    # ============================================================
    def _build_system_tab(self):
        content = self.tab_system

        header = tk.Frame(content, bg="#1A1A2E")
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(header, text="💻 Параметры вашей системы (собираются автоматически)",
                 font=self.font_consolas_bold, fg="#00E5FF", bg="#1A1A2E").pack(side="left")

        btn_refresh = RoundedButton(
            header, text="🔄 Обновить",
            command=self.refresh_system_info,
            width=120, height=32, corner_radius=10,
            bg_color="#00E5FF", hover_color="#66FFFF",
            text_color="#0B0C10", font_size=11
        )
        btn_refresh.pack(side="right")

        info_frame = tk.Frame(content, bg="#00E5FF", bd=2, relief="flat")
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.info_text = scrolledtext.ScrolledText(
            info_frame, wrap=tk.WORD, font=self.font_consolas,
            fg="#E0E0E0", bg="#0B0C10", insertbackground="white",
            bd=0, highlightthickness=0
        )
        self.info_text.pack(fill="both", expand=True, padx=3, pady=3)
        self.info_text.config(state="disabled")

        self.refresh_system_info()

    def refresh_system_info(self):
        info = get_os_info()
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)

        self.info_text.insert(tk.END, "══════ ПАРАМЕТРЫ УСТРОЙСТВА ══════\n\n")
        device_keys = ["Тип устройства", "Имя устройства", "Модель / производитель",
                       "Тип системы", "Код устройства", "Код продукта",
                       "Процессор", "Ядра / потоки", "Частота CPU",
                       "Видеопроцессор", "ОЗУ (всего)",
                       "Батарея: заряд", "Батарея: статус"]
        for key in device_keys:
            if key in info:
                self.info_text.insert(tk.END, f"  • {key}:  {info[key]}\n")

        self.info_text.insert(tk.END, "\n══════ ХАРАКТЕРИСТИКИ ОС ══════\n\n")
        for key in ["Выпуск ОС", "Версия ОС", "Дата установки", "Сборка установки"]:
            if key in info:
                self.info_text.insert(tk.END, f"  • {key}:  {info[key]}\n")

        self.info_text.config(state="disabled")

    # ============================================================
    # ВКЛАДКА 3: БАЗА ЗНАНИЙ (ИИ)
    # ============================================================
    def _build_knowledge_tab(self):
        content = self.tab_knowledge

        header = tk.Frame(content, bg="#1A1A2E")
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(header, text="🧠 Умный поиск по базе знаний (задайте вопрос):",
                 font=self.font_consolas_bold, fg="#00E5FF", bg="#1A1A2E").pack(anchor="w")

        search_row = tk.Frame(content, bg="#1A1A2E")
        search_row.pack(fill="x", padx=20, pady=5)

        self.search_input = tk.Entry(search_row, font=self.font_consolas, bg="#0B0C10",
                                     fg="white", insertbackground="white", relief="flat",
                                     highlightthickness=1, highlightcolor="#00E5FF")
        self.search_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_input.bind("<Return>", lambda e: self.perform_search())

        btn_search = RoundedButton(
            search_row, text="🔎 Найти",
            command=self.perform_search,
            width=140, height=35, corner_radius=10,
            bg_color="#00E5FF", hover_color="#66FFFF",
            text_color="#0B0C10", font_size=12
        )
        btn_search.pack(side="right")

        tips_frame = tk.Frame(content, bg="#1A1A2E")
        tips_frame.pack(fill="x", padx=20, pady=(5, 10))

        tk.Label(tips_frame, text="Популярные вопросы:",
                 font=("Consolas", 10), fg="#9E9E9E", bg="#1A1A2E").pack(anchor="w")

        examples = ["Что такое ОЗУ?", "Перегрев ноутбука", "Залил ноутбук",
                    "Аккумулятор быстро садится", "Как выбрать ЗУ?"]
        chips_row = tk.Frame(tips_frame, bg="#1A1A2E")
        chips_row.pack(anchor="w", pady=3)

        for ex in examples:
            btn = tk.Label(chips_row, text=ex, font=("Consolas", 9),
                           fg="#00E5FF", bg="#0B0C10", padx=10, pady=4, cursor="hand2")
            btn.pack(side="left", padx=3)
            btn.bind("<Button-1>", lambda e, q=ex: self._quick_search(q))

        result_frame = tk.Frame(content, bg="#00E5FF", bd=2, relief="flat")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.search_result = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, font=self.font_consolas,
            fg="#E0E0E0", bg="#0B0C10", insertbackground="white",
            bd=0, highlightthickness=0
        )
        self.search_result.pack(fill="both", expand=True, padx=3, pady=3)
        self.search_result.config(state="disabled")
        self._show_search_welcome()

    def _show_search_welcome(self):
        welcome = ("Добро пожаловать в базу знаний!\n\n"
                   "Задайте вопрос — система найдёт ближайшие по смыслу ответы.\n"
                   "Примеры: «Как выбрать блок питания?», «Почему тормозит ноутбук?», "
                   "«Залил клавиатуру».\n\n"
                   "Используйте поле выше или нажмите на популярный вопрос.")
        self.search_result.config(state="normal")
        self.search_result.delete(1.0, tk.END)
        self.search_result.insert(tk.END, welcome)
        self.search_result.config(state="disabled")

    def _quick_search(self, query):
        self.search_input.delete(0, tk.END)
        self.search_input.insert(0, query)
        self.perform_search()

    def perform_search(self):
        query = self.search_input.get().strip()
        if not query:
            self._show_search_welcome()
            return
        results = search_knowledge(query, QA_PAIRS, top_n=3)
        self.search_result.config(state="normal")
        self.search_result.delete(1.0, tk.END)
        if not results:
            self.search_result.insert(tk.END,
                "🤔 Не удалось найти подходящий ответ.\n\n"
                "Попробуйте переформулировать вопрос или воспользуйтесь примером.")
        else:
            self.search_result.insert(tk.END, f"🔍 Найдено ответов: {len(results)}\n")
            self.search_result.insert(tk.END, "═" * 60 + "\n\n")
            for i, (qa, score) in enumerate(results, 1):
                self.search_result.insert(tk.END,
                    f"► Результат {i}  [релевантность: {int(score*100)}%]\n")
                self.search_result.insert(tk.END, f"❓ {qa['question']}\n\n")
                self.search_result.insert(tk.END, f"{qa['answer']}\n\n")
                self.search_result.insert(tk.END, "─" * 60 + "\n\n")
        self.search_result.config(state="disabled")

    # ============================================================
    # ЛОГИКА ДИАГНОСТИКИ
    # ============================================================
    def perform_diagnosis(self):
        facts = [cond for cond, var in self.check_vars.items() if var.get()]
        if not facts:
            self.show_result("⚠️ Вы не отметили ни одного симптома.")
            return
        diagnosis = self.engine.diagnose_from_facts(facts)
        self.show_result(self.format_diagnosis(diagnosis))

    def format_diagnosis(self, diagnosis):
        if not diagnosis:
            return ("🔍 Совпадений не найдено.\n"
                    "Возможно, проблема не в аппаратной части или симптомы указаны неполно.")
        lines = [f"✅ Найдено рекомендаций: {len(diagnosis)}\n"]
        for idx, item in enumerate(diagnosis, 1):
            rule = item["rule"]
            percent = item["percent"]
            matched = item["matched"]
            total = item["total"]
            bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
            lines.append(f"► Рекомендация {idx}  [Совпадение: {percent}% ({matched}/{total}) {bar}]")
            lines.append(f"   {rule['result']}\n")
        return "\n".join(lines)

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def reset_all(self):
        for var in self.check_vars.values():
            var.set(False)
        self.text_input.delete(0, tk.END)
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")

    def ai_recognize(self):
        raw_text = self.text_input.get()
        if not raw_text.strip():
            self.show_result("⚠️ Введите описание симптомов.")
            return
        recognized = match_symptoms(raw_text, self.all_conditions)
        if not recognized:
            self.show_result("🤔 ИИ не распознал знакомых симптомов.\n"
                             "Попробуйте описать проблему иначе.")
            return
        for var in self.check_vars.values():
            var.set(False)
        for symptom in recognized:
            if symptom in self.check_vars:
                self.check_vars[symptom].set(True)
        self.show_result(f"🧠 ИИ распознал следующие симптомы:\n- " + "\n- ".join(recognized) +
                         "\n\n✅ Нажмите «Диагностировать».")
        self.text_input.delete(0, tk.END)

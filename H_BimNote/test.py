import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
import time
import threading


class MoodSpinner(ttk.Frame):
    def __init__(self, master=None, moods=None, **kwargs):
        super().__init__(master, **kwargs)

        self.moods = moods or [
            "🔥열정",
            "😴나른",
            "🤯과부하",
            "✨영감",
            "😎여유",
            "🥶냉정",
            "🧠아이디어",
            "🫠현타",
        ]
        self.result_var = tk.StringVar(value="기분을 골라보자!")
        self.advice_var = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(self, text="🌀 무드 스피너", font=("Helvetica", 20))
        title.pack(pady=10)

        spin_button = ttk.Button(
            self, text="돌려!", bootstyle="success-outline", command=self._on_spin_click
        )
        spin_button.pack(pady=20)

        result_label = ttk.Label(
            self, textvariable=self.result_var, font=("Helvetica", 16)
        )
        result_label.pack(pady=10)

        self.advice_label = ttk.Label(
            self,
            textvariable=self.advice_var,
            font=("Helvetica", 12),
            wraplength=350,
            foreground="#6c757d",
        )
        self.advice_label.pack(pady=10)

    def _on_spin_click(self):
        threading.Thread(target=self._spin_animation).start()

    def _spin_animation(self):
        self.result_var.set("🎲 스피너 작동 중...")
        self.advice_var.set("")
        time.sleep(0.5)

        for _ in range(15):
            self.result_var.set(random.choice(self.moods))
            time.sleep(0.05)

        final_choice = random.choice(self.moods)
        self.result_var.set(f"🎉 오늘의 무드: {final_choice}")
        self.advice_var.set(self.get_ai_message(final_choice))

    def get_ai_message(self, mood):
        # 여기 LLM 연동 가능 (예: OpenAI API 호출)
        mood_quotes = {
            "🔥열정": "오늘은 당신의 열정이 세상을 바꿀지도 몰라요!",
            "😴나른": "조금 느리더라도, 당신은 제 길을 가고 있어요.",
            "🤯과부하": "잠시 쉬어가도 괜찮아요. 리셋도 능력이에요.",
            "✨영감": "지금 떠오른 그 생각, 꼭 메모해 두세요!",
            "😎여유": "이 여유 속에서 진짜 중요한 게 보여요.",
            "🥶냉정": "냉정함 속에서도 따뜻함을 잃지 마세요.",
            "🧠아이디어": "지금의 아이디어가 내일의 혁신이 될 수 있어요.",
            "🫠현타": "현타도 성장의 일부예요. 곧 다시 올라가요!",
        }
        return mood_quotes.get(mood, "오늘도 당신만의 속도로, 멋지게 살아가세요.")


# 테스트용 단독 실행
if __name__ == "__main__":
    app = ttk.Window("무드 스피너 테스트", themename="morph", size=(400, 300))
    spinner = MoodSpinner(app)
    spinner.pack(fill=BOTH, expand=True, padx=20, pady=20)
    app.mainloop()

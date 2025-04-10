# import math
# import pandas as pd
# from scipy.interpolate import interp1d
# import ttkbootstrap as tb
# from ttkbootstrap.constants import *
# from tkinter import scrolledtext  # ✅ 추가

# # --- 보정계수 테이블 ---
# Ce = {
#     0: [
#         1.014427093,
#         1.239688571,
#         1.581491544,
#         2.046642511,
#         2.845255728,
#         4.129173595,
#         6.437380435,
#         8.212274407,
#         11.09433023,
#         13.95193761,
#         18.58024011,
#         23.3660208,
#         31.56620663,
#         42.03772369,
#         53.62823059,
#         70.40271776,
#         91.10968418,
#         116.2301553,
#         146.1679833,
#         181.2027783,
#         227.8758435,
#         290.7050432,
#         376.2077022,
#         578.1664373,
#         792.3395838,
#         1166.47122,
#         1645.031368,
#         2128.870776,
#         2677.211841,
#         3464.637916,
#         5000,
#         10000,
#     ],
#     1: [
#         1.570909091,
#         1.563636364,
#         1.554545455,
#         1.541818182,
#         1.525454545,
#         1.505454545,
#         1.472727273,
#         1.452727273,
#         1.427272727,
#         1.403636364,
#         1.376363636,
#         1.354545455,
#         1.321818182,
#         1.290909091,
#         1.261818182,
#         1.229090909,
#         1.2,
#         1.176363636,
#         1.154545455,
#         1.136363636,
#         1.12,
#         1.105454545,
#         1.089090909,
#         1.069090909,
#         1.054545455,
#         1.036363636,
#         1.023636364,
#         1.014545455,
#         1.009090909,
#         1,
#         1,
#         1,
#     ],
# }
# df1 = pd.DataFrame(Ce)
# fq = interp1d(df1[0], df1[1], kind="linear")

# # --- 코드 맵 ---
# code_map = {
#     "ASCE 7-05": (50, 3),
#     "EN 1991.1.4": (50, 600),
#     "KDS 41 10 15": (100, 600),
#     "ASCE 7-10 category I": (300, 3),
#     "ASCE 7-10 category II": (700, 3),
#     "ASCE 7-10 category III": (1700, 3),
#     "BS 6399": (50, 3600),
# }


# class Wind_Conversion:
#     def Wind_Speed(self, RP, AT, Vel, nRP, nAT):
#         C_RPover50 = 0.36 + 0.1 * math.log(12 * RP)
#         C_nRPover50 = 0.36 + 0.1 * math.log(12 * nRP)
#         C_ATover3600 = fq(AT)
#         C_nATover3600 = fq(nAT)
#         nVel = round(C_nRPover50 / C_RPover50 * C_nATover3600 / C_ATover3600 * Vel, 2)
#         return nVel


# def launch_app():
#     app = tb.Window(themename="minty")
#     app.title("H_Wind Speed Conversion Tool")
#     app.geometry("540x730")

#     converter = Wind_Conversion()
#     history = []  # 변환 히스토리 저장 리스트

#     # -------------------- Mode Selection --------------------
#     mode_frame = tb.Frame(app)
#     mode_frame.pack(pady=10, anchor="w", padx=20)

#     tb.Label(mode_frame, text="Conversion Mode:", font=("Arial", 10, "bold")).pack(
#         side="left", padx=(0, 10)
#     )
#     mode = tb.StringVar(value="Basic")
#     mode_combo = tb.Combobox(
#         mode_frame,
#         textvariable=mode,
#         values=["Basic", "Advanced"],
#         state="readonly",
#         width=20,
#     )
#     mode_combo.pack(side="left")

#     # -------------------- Input Fields --------------------
#     input_frame = tb.Frame(app)
#     input_frame.pack(pady=10, fill="x", padx=20)

#     def labeled_entry(frame, label_text):
#         tb.Label(frame, text=label_text).pack(anchor="w")
#         entry = tb.Entry(frame, width=30)
#         entry.pack(pady=2, fill="x")
#         return entry

#     entry_rp = labeled_entry(input_frame, "Initial return period (year)")
#     entry_at = labeled_entry(input_frame, "Initial averaging time (seconds)")
#     entry_vel = labeled_entry(input_frame, "Wind speed under Initial conditions (m/s)")

#     # -------------------- Basic Mode Target Code --------------------
#     basic_frame = tb.Frame(app)
#     basic_frame.pack(pady=10, fill="x", padx=20)

#     tb.Label(basic_frame, text="Target Code", font=("Arial", 10, "bold")).pack(
#         anchor="w"
#     )
#     code_var = tb.StringVar()
#     code_combo = tb.Combobox(
#         basic_frame,
#         textvariable=code_var,
#         values=list(code_map.keys()),
#         state="readonly",
#         width=30,
#     )
#     code_combo.pack(pady=2, fill="x")

#     # -------------------- Advanced Mode Fields --------------------
#     advanced_frame = tb.Frame(app)
#     tb.Label(advanced_frame, text="Target return period (year)").pack(anchor="w")
#     entry_nrp = tb.Entry(advanced_frame, width=30)
#     entry_nrp.pack(pady=2, fill="x")
#     tb.Label(advanced_frame, text="Target averaging time (seconds)").pack(anchor="w")
#     entry_nat = tb.Entry(advanced_frame, width=30)
#     entry_nat.pack(pady=2, fill="x")

#     def update_mode(*args):
#         if mode.get() == "Basic":
#             basic_frame.pack(pady=10, fill="x", padx=20)
#             advanced_frame.pack_forget()
#         else:
#             basic_frame.pack_forget()
#             advanced_frame.pack(pady=10, fill="x", padx=20)

#     mode_combo.bind("<<ComboboxSelected>>", update_mode)

#     # -------------------- Result + Button --------------------
#     bottom_frame = tb.Frame(app)
#     bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

#     convert_btn = tb.Button(bottom_frame, text="변환하기", bootstyle="primary-outline")
#     convert_btn.pack(pady=(0, 15))

#     result_title = tb.Label(
#         bottom_frame,
#         text="Modified Wind speed for Target conditions",
#         font=("Arial", 10, "bold"),
#     )
#     result_title.pack(anchor="w")

#     result_label = tb.Label(
#         bottom_frame,
#         text="결과가 여기에 표시됩니다.",
#         font=("Arial", 11),
#         wraplength=440,
#         foreground="blue",
#     )
#     result_label.pack(anchor="w")

#     # -------------------- History (ScrolledText) --------------------
#     tb.Label(bottom_frame, text="Conversion History", font=("Arial", 10, "bold")).pack(
#         anchor="w", pady=(10, 0)
#     )

#     # 히스토리 출력창 생성
#     history_box = scrolledtext.ScrolledText(bottom_frame, height=7, wrap="word")
#     history_box.pack(fill="both", expand=False)

#     # ✅ 키보드 입력 차단, Ctrl+C는 허용
#     def block_typing(event):
#         if (event.state & 0x4) and event.keysym.lower() in ("c", "a"):
#             return  # Ctrl+C, Ctrl+A 허용
#         return "break"

#     history_box.bind("<Key>", block_typing)

#     def append_history_log(text):
#         history_box.insert("end", text + "\n")
#         history_box.see("end")

#     # -------------------- 계산 함수 --------------------
#     def calculate():
#         try:
#             RP = float(entry_rp.get())
#             AT = float(entry_at.get())
#             Vel = float(entry_vel.get())

#             if mode.get() == "Basic":
#                 code = code_var.get()
#                 if code not in code_map:
#                     result_label.config(text="⚠️ Target Code를 선택해주세요.")
#                     return
#                 nRP, nAT = code_map[code]
#             else:
#                 nRP = float(entry_nrp.get())
#                 nAT = float(entry_nat.get())

#             nVel = converter.Wind_Speed(RP, AT, Vel, nRP, nAT)

#             result_label.config(
#                 text=f"변환된 풍속: {nVel} m/s\n(재현주기 {nRP}년, 평균시간 {nAT}초 기준)"
#             )

#             log_text = f"{Vel} → {nVel} m/s (RP: {RP}→{nRP}, AT: {AT}→{nAT})"
#             history.append(log_text)
#             append_history_log(log_text)

#         except Exception as e:
#             result_label.config(text=f"⚠️ 입력 오류: {e}")

#     convert_btn.config(command=calculate)

#     # -------------------- 엔터로 포커스 이동 --------------------
#     entry_rp.bind("<Return>", lambda e: entry_at.focus_set())
#     entry_at.bind("<Return>", lambda e: entry_vel.focus_set())
#     entry_vel.bind(
#         "<Return>",
#         lambda e: (
#             code_combo.focus_set() if mode.get() == "Basic" else entry_nrp.focus_set()
#         ),
#     )
#     entry_nrp.bind("<Return>", lambda e: entry_nat.focus_set())
#     entry_nat.bind("<Return>", lambda e: calculate())
#     code_combo.bind("<Return>", lambda e: calculate())

#     update_mode()
#     app.mainloop()


# if __name__ == "__main__":
#     launch_app()

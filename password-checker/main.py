import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

from checker import check_strength
from generator import generate_password, generate_passphrase


COLORS = {
    "bg":       "#0d0d0f",
    "surface":  "#16161a",
    "surface2": "#1e1e24",
    "border":   "#2a2a35",
    "text":     "#e8e8f0",
    "muted":    "#6b6b80",
    "accent":   "#00e5a0",
    "danger":   "#ff4f6a",
    "warn":     "#ffb547",
}

LEVEL_COLORS = {
    "Very Strong": "#00e5a0",
    "Strong":      "#00e5a0",
    "Fair":        "#ffb547",
    "Weak":        "#ff4f6a",
    "Very Weak":   "#ff4f6a",
    "empty":       "#6b6b80",
}


class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Tool")
        self.geometry("520x700")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self._build_ui()

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(hdr, text="// password_tool.py", font=("Courier", 14, "bold"),
                 fg=COLORS["accent"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(hdr, text="Strength checker · Entropy analyser · Secure generator",
                 font=("Arial", 10), fg=COLORS["muted"], bg=COLORS["bg"]).pack(anchor="w")

        # ── Checker section ──────────────────────────────────
        self._section_label("CHECK STRENGTH")
        self._build_checker()

        # ── Generator section ────────────────────────────────
        self._section_label("GENERATE PASSWORD")
        self._build_generator()

    def _section_label(self, text):
        tk.Label(self, text=text, font=("Arial", 9, "bold"),
                 fg=COLORS["muted"], bg=COLORS["bg"]
                 ).pack(anchor="w", padx=24, pady=(18, 4))

    def _build_checker(self):
        frame = tk.Frame(self, bg=COLORS["surface"], bd=0)
        frame.pack(fill="x", padx=24, pady=4)
        frame.configure(highlightbackground=COLORS["border"], highlightthickness=1)

        # Password entry
        self.pw_var = tk.StringVar()
        self.pw_var.trace_add("write", self._on_pw_change)
        entry_frame = tk.Frame(frame, bg=COLORS["surface"])
        entry_frame.pack(fill="x", padx=16, pady=(16, 8))

        self.pw_entry = tk.Entry(entry_frame, textvariable=self.pw_var,
                                  font=("Courier", 13), fg=COLORS["text"],
                                  bg=COLORS["surface2"], bd=0,
                                  insertbackground=COLORS["accent"],
                                  show="•")
        self.pw_entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=8)

        self.show_btn = tk.Button(entry_frame, text="👁", font=("Arial", 11),
                                   fg=COLORS["muted"], bg=COLORS["surface2"], bd=0,
                                   command=self._toggle_vis, cursor="hand2", width=3)
        self.show_btn.pack(side="right")

        # Strength bar
        self.strength_label = tk.Label(frame, text="—", font=("Courier", 12, "bold"),
                                        fg=COLORS["muted"], bg=COLORS["surface"])
        self.strength_label.pack(anchor="w", padx=16)

        self.bar_canvas = tk.Canvas(frame, height=6, bg=COLORS["surface2"], bd=0,
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=16, pady=(4, 4))
        self.bar_rect = self.bar_canvas.create_rectangle(0, 0, 0, 6, fill=COLORS["accent"], width=0)

        self.entropy_label = tk.Label(frame, text="", font=("Courier", 10),
                                       fg=COLORS["muted"], bg=COLORS["surface"])
        self.entropy_label.pack(anchor="e", padx=16)

        # Criteria
        crit_frame = tk.Frame(frame, bg=COLORS["surface"])
        crit_frame.pack(fill="x", padx=16, pady=(8, 16))
        self.crit_labels = {}
        criteria_text = [
            ("length",    "≥ 12 characters"),
            ("uppercase", "Uppercase A-Z"),
            ("lowercase", "Lowercase a-z"),
            ("digit",     "Digits 0-9"),
            ("symbol",    "Symbols !@#$"),
            ("not_common","Not a common password"),
        ]
        for i, (key, text) in enumerate(criteria_text):
            row, col = divmod(i, 2)
            cell = tk.Frame(crit_frame, bg=COLORS["surface2"],
                            highlightbackground=COLORS["border"], highlightthickness=1)
            cell.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
            crit_frame.columnconfigure(col, weight=1)
            lbl = tk.Label(cell, text=f"  ○  {text}", font=("Arial", 10),
                           fg=COLORS["muted"], bg=COLORS["surface2"], anchor="w")
            lbl.pack(fill="x", ipady=6, ipadx=4)
            self.crit_labels[key] = lbl

    def _build_generator(self):
        frame = tk.Frame(self, bg=COLORS["surface"])
        frame.pack(fill="x", padx=24, pady=4)
        frame.configure(highlightbackground=COLORS["border"], highlightthickness=1)

        inner = tk.Frame(frame, bg=COLORS["surface"])
        inner.pack(fill="x", padx=16, pady=16)

        # Length slider
        len_row = tk.Frame(inner, bg=COLORS["surface"])
        len_row.pack(fill="x", pady=4)
        tk.Label(len_row, text="Length:", font=("Arial", 11), fg=COLORS["text"],
                 bg=COLORS["surface"]).pack(side="left")
        self.len_val = tk.IntVar(value=16)
        self.len_label = tk.Label(len_row, text="16", font=("Courier", 11, "bold"),
                                   fg=COLORS["accent"], bg=COLORS["surface"], width=3)
        self.len_label.pack(side="right")
        slider = tk.Scale(len_row, from_=8, to=32, orient="horizontal",
                          variable=self.len_val, bg=COLORS["surface"],
                          fg=COLORS["text"], troughcolor=COLORS["surface2"],
                          activebackground=COLORS["accent"], bd=0, highlightthickness=0,
                          showvalue=False, command=lambda v: self.len_label.config(text=str(int(float(v)))))
        slider.pack(side="right", fill="x", expand=True, padx=8)

        # Checkboxes
        self.opt_upper  = tk.BooleanVar(value=True)
        self.opt_digit  = tk.BooleanVar(value=True)
        self.opt_symbol = tk.BooleanVar(value=True)
        for var, label in [(self.opt_upper, "Include uppercase (A-Z)"),
                           (self.opt_digit,  "Include digits (0-9)"),
                           (self.opt_symbol, "Include symbols (!@#$%)")]:
            cb = tk.Checkbutton(inner, text=label, variable=var,
                                font=("Arial", 11), fg=COLORS["text"],
                                bg=COLORS["surface"], activebackground=COLORS["surface"],
                                selectcolor=COLORS["surface2"],
                                activeforeground=COLORS["accent"])
            cb.pack(anchor="w", pady=2)

        # Output box
        out_frame = tk.Frame(inner, bg=COLORS["surface2"],
                              highlightbackground=COLORS["border"], highlightthickness=1)
        out_frame.pack(fill="x", pady=(12, 8))
        self.gen_output = tk.Label(out_frame, text="— click generate —",
                                    font=("Courier", 12), fg=COLORS["muted"],
                                    bg=COLORS["surface2"], wraplength=420,
                                    justify="left", anchor="w")
        self.gen_output.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        tk.Button(out_frame, text="⧉", font=("Arial", 13), fg=COLORS["muted"],
                   bg=COLORS["surface2"], bd=0, command=self._copy_gen,
                   cursor="hand2").pack(side="right", padx=8)

        # Buttons
        btn_row = tk.Frame(inner, bg=COLORS["surface"])
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="generate_password()", font=("Courier", 11, "bold"),
                   fg=COLORS["bg"], bg=COLORS["accent"], bd=0, cursor="hand2",
                   command=self._generate, pady=10).pack(side="left", fill="x", expand=True, padx=(0,4))
        tk.Button(btn_row, text="passphrase()", font=("Courier", 11, "bold"),
                   fg=COLORS["accent"], bg=COLORS["surface2"], bd=0, cursor="hand2",
                   command=self._gen_passphrase, pady=10).pack(side="left", fill="x", expand=True)

    def _on_pw_change(self, *_):
        pw = self.pw_var.get()
        result = check_strength(pw)
        score = result["score"]

        color = LEVEL_COLORS.get(result["level"], COLORS["muted"])
        self.strength_label.config(text=result["level"] if pw else "—", fg=color)

        width = self.bar_canvas.winfo_width() or 460
        fill_w = int((score / 6) * width)
        self.bar_canvas.coords(self.bar_rect, 0, 0, fill_w, 6)
        self.bar_canvas.itemconfig(self.bar_rect, fill=color)

        self.entropy_label.config(
            text=f"entropy: {result['entropy']} bits" if pw else "")

        for key, lbl in self.crit_labels.items():
            passed = result.get("criteria", {}).get(key, False)
            symbol = "●" if passed else "○"
            text = lbl.cget("text")[3:]
            lbl.config(text=f"  {symbol}  {text}",
                       fg=COLORS["accent"] if passed else COLORS["muted"])

    def _toggle_vis(self):
        self.pw_entry.config(show="" if self.pw_entry.cget("show") == "•" else "•")

    def _generate(self):
        pw = generate_password(
            length=self.len_val.get(),
            use_uppercase=self.opt_upper.get(),
            use_digits=self.opt_digit.get(),
            use_symbols=self.opt_symbol.get(),
        )
        self.gen_output.config(text=pw, fg=COLORS["accent"])

    def _gen_passphrase(self):
        phrase = generate_passphrase(word_count=4)
        self.gen_output.config(text=phrase, fg=COLORS["warn"])

    def _copy_gen(self):
        text = self.gen_output.cget("text")
        if text == "— click generate —":
            return
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
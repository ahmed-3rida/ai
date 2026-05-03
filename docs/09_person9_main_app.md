# 👤 Person 9 — Main Entry Point, App Assembly & Theming

## ما هو دورك؟
أنت مسؤول عن **ملف `main.py`** و **ملف `gui/app.py`** — النقطة التي يُشغَّل منها البرنامج وكيف تتجمع كل الأجزاء معاً.

---

## 📄 ملفاتك

### `main.py` — نقطة الدخول
```python
from gui.app import KnightsTourApp

def apply_theme(app):
    style = ttk.Style(app)
    style.theme_use("clam")          # أقرب theme لمظهر مسطح داكن
    style.configure("TScale", ...)
    style.configure("Horizontal.TProgressbar", ...)

if __name__ == "__main__":
    app = KnightsTourApp()
    apply_theme(app)
    app.mainloop()          # ← يبقى البرنامج شغالاً حتى تُغلق النافذة
```

### `gui/app.py` — النافذة الرئيسية
يحتوي على `KnightsTourApp` التي تجمع كل الـ Mixins.

---

## 🧩 مفهوم الـ Mixins

المشروع يستخدم نمط **Mixin** لتقسيم كود الـ GUI:

```python
class KnightsTourApp(BoardMixin, ControlsMixin, SolverMixin, tk.Tk):
    ...
```

### ما هو الـ Mixin؟
Mixin هو class يحتوي على مجموعة من الدوال **بدون حالة مستقلة** (state) — يُصمَّم ليُضاف لـ class آخر عبر الـ Inheritance.

```
KnightsTourApp
├── BoardMixin    → دوال رسم اللوحة
├── ControlsMixin → دوال اللوحة الجانبية
├── SolverMixin   → دوال الحل والأنيميشن
└── tk.Tk         → النافذة الأساسية
```

Python يدعم **Multiple Inheritance** — يمكن لـ class أن يرث من أكثر من class واحد.

### ترتيب MRO (Method Resolution Order)
عندما تبحث Python عن دالة، تبحث بهذا الترتيب:
1. `KnightsTourApp` نفسها
2. `BoardMixin`
3. `ControlsMixin`
4. `SolverMixin`
5. `tk.Tk`

---

## 🏗️ `_build_ui()` — هيكل النافذة

```
┌────────────────────────────────────────────────┐
│  CS212 · AI Project · Spring 2025             │ ← header
│         Knight's Tour Solver                   │
│  Backtracking | Genetic Algorithm              │
├────────────────────────────────────────────────┤ ← separator (1px)
│ ┌──────────────┐ ┌──────────────────────────┐ │
│ │  LEFT PANEL  │ │      CANVAS (Board)      │ │
│ │ (controls)   │ │                          │ │
│ │              │ │      n × n grid          │ │
│ │  280px wide  │ │   (expands with window)  │ │
│ └──────────────┘ └──────────────────────────┘ │
├────────────────────────────────────────────────┤
│  Status bar: "Ready — select board size..."    │ ← bottom strip
└────────────────────────────────────────────────┘
```

### الكود

```python
# Body layout: 2 columns
body = tk.Frame(self, bg=BG)
body.columnconfigure(1, weight=1)   # العمود الثاني يتمدد مع النافذة
body.rowconfigure(0, weight=1)

# اللوحة الجانبية
self._panel = tk.Frame(body, bg=SURFACE, ...)
self._panel.grid(row=0, column=0, sticky="nsew")
self._build_controls(self._panel)   # ← ControlsMixin

# Canvas اللوحة
self._canvas = tk.Canvas(board_frame, bg=BG)
self._canvas.pack(fill="both", expand=True)
self._canvas.bind("<Configure>", lambda e: self._build_board())  # إعادة رسم عند تغيير الحجم
self._canvas.bind("<Button-1>", self._on_canvas_click)           # ← BoardMixin
```

---

## 🎨 `apply_theme()` — تطبيق الثيم

```python
style = ttk.Style(app)
style.theme_use("clam")   # أساس الـ theme

style.configure("TScale",
    background=SURFACE,
    troughcolor=SURFACE2,    # لون المسار خلف الـ slider
    sliderlength=16          # حجم مقبض الـ slider
)

style.configure("Horizontal.TProgressbar",
    troughcolor=SURFACE2,
    background=ACCENT,       # اللون الأزرق يملأ الـ bar
)
```

**لماذا نحتاج لـ Theme؟**  
لأن `ttk.Scale` و `ttk.Progressbar` لهم مظهر افتراضي أبيض/رمادي لا يتناسب مع الثيم الداكن.

---

## 🔑 الـ State المشترك

كل الـ Mixins تصل للـ state عبر `self` (الـ KnightsTourApp):

```python
# في __init__:
self.n          = tk.IntVar(value=6)      # حجم اللوحة
self.algo       = tk.StringVar(...)       # الخوارزمية المختارة
self.pop_size   = tk.IntVar(value=200)    # GA: حجم الـ population
self.gens       = tk.IntVar(value=500)    # GA: عدد الأجيال
self.start_r    = 0                       # نقطة البداية (صف)
self.start_c    = 0                       # نقطة البداية (عمود)
self.full_path  = []                      # آخر مسار محلول
self.cells      = {}                      # بيانات خلايا اللوحة
self.anim_delay = tk.IntVar(value=120)    # سرعة الأنيميشن
self.solving    = False                   # حارس: هل الحل جارٍ؟
```

---

## 🚀 `app.mainloop()` — قلب tkinter

```python
app.mainloop()
```

هذا السطر يُشغّل **حلقة الأحداث (Event Loop)**:
- ينتظر أحداث (ضغط، حركة الماوس، تغيير النافذة)
- يُنفّذ handlers المناسبة
- يُحدّث الشاشة
- يتوقف حين تُغلق النافذة

---

## ❓ أسئلة قد تُسأل عنها

**س: ما `if __name__ == "__main__"`؟**  
ج: يضمن أن الكود يعمل فقط عند تشغيل `main.py` مباشرة — وليس حين يُستورد كـ module.

**س: لماذا `tk.Tk` في الـ inheritance وليس عبر `super().__init__()`؟**  
ج: `KnightsTourApp` ترث من `tk.Tk` مباشرة وتستدعي `super().__init__()` الذي يُهيئ النافذة. هذا النمط شائع في tkinter.

**س: ما معنى `sticky="nsew"`؟**  
ج: يعني أن الـ widget يتمدد في كل الاتجاهات (North, South, East, West) لملء الخلية في الـ grid.

**س: ما الفرق بين `pack()` و `grid()`؟**  
ج: `pack()` يرص العناصر بشكل خطي (أفقياً أو عمودياً). `grid()` يضعها في شبكة صف/عمود. لا تخلط بينهما في نفس الـ Frame!

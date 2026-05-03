# 👤 Person 7 — GUI: Controls Panel & Settings Widgets

## ما هو دورك؟
أنت مسؤول عن **ملف `gui/controls.py`** — اللوحة الجانبية اليسرى بكل ما فيها من أزرار وإعدادات.

---

## 📄 ملفك: `gui/controls.py`

### المحتويات

| الدالة | الوظيفة |
|---|---|
| `_build_controls(p)` | بناء كل محتوى اللوحة الجانبية |
| `_lbl()` | مساعد: إنشاء Label مُنسّق |
| `_stat_card()` | بناء بطاقة إحصائية واحدة |
| `_tab_btn()` | إنشاء زر tab للخوارزمية |
| `_on_size_change()` | ردة فعل slider الحجم |
| `_select_algo()` | تغيير الخوارزمية |
| `_update_algo_buttons()` | تحديث مظهر الأزرار |

---

## 🏗️ `_build_controls()` — بناء اللوحة

اللوحة تُبنى من أعلى لأسفل بهذا الترتيب:

```
┌─────────────────────┐
│    CONFIGURATION    │  ← عنوان
│─────────────────────│
│  Board Size (n × n) │  ← label
│  [===slider===] [6] │  ← Slider + live number
│─────────────────────│
│      Algorithm      │  ← label
│ [Backtracking] [GA] │  ← Tab buttons
│  [GA params hidden] │  ← يظهر فقط عند اختيار GA
│─────────────────────│
│ "Click cell to..."  │  ← Hint label
│  [▶ SOLVE]          │  ← Run button
│  [↺ Replay]         │  ← Replay button
│─────────────────────│
│  Animation Speed    │
│ slow [=====] fast   │
│─────────────────────│
│ [Squares][Coverage] │  ← Stats grid
│ [Time  ][Result  ]  │
└─────────────────────┘
```

---

## 🎛️ Board Size Slider

```python
ttk.Scale(
    size_row,
    from_=BOARD_MIN,   # 5
    to=BOARD_MAX,      # 12
    orient="horizontal",
    variable=self.n,             # ← مرتبط بـ tk.IntVar
    command=self._on_size_change # ← يُستدعى عند التحريك
)
```

**`tk.IntVar`**: متغير tkinter خاص يُحدَّث تلقائياً ويُحدِّث كل Widget مرتبط به.

---

## 🔘 Algorithm Tab Buttons

```python
def _tab_btn(self, parent, text, algo_name):
    return tk.Button(
        ...,
        command=lambda: self._select_algo(algo_name)
    )
```

```python
def _update_algo_buttons(self):
    if algo == "backtracking":
        self._btn_bt.config(bg=ACCENT, fg="white")    # مضيء
        self._btn_ga.config(bg=SURFACE2, fg=MUTED)    # معتم
        self._ga_frame.pack_forget()                   # أخفِ GA params
    else:
        self._btn_ga.config(bg=ACCENT, fg="white")
        self._ga_frame.pack(...)                       # أظهر GA params
```

---

## 📊 `_stat_card()` — بطاقة الإحصائيات

```python
def _stat_card(self, parent, label, val, row, col):
    f = tk.Frame(parent, bg=SURFACE2, ...)
    f.grid(row=row, column=col, ...)          # شبكة 2×2

    tk.Label(f, text=label.upper(), ...).pack()  # العنوان
    var = tk.StringVar(value=val)
    tk.Label(f, textvariable=var, ...).pack()    # القيمة المتغيرة

    return var   # نُرجع المتغير ليُحدَّث لاحقاً
```

استخدامها بعد الحل:
```python
self._stat_squares.set("32/36")   # يتحدث تلقائياً في الـ UI
self._stat_cov.set("89%")
```

---

## ⏱️ `_on_size_change()` — تغيير الحجم

```python
def _on_size_change(self, val):
    v = int(float(val))       # تحويل من float لـ int
    self.n.set(v)
    self._size_lbl.config(text=str(v))   # تحديث الرقم الجانبي
    self.start_r = 0
    self.start_c = 0                     # إعادة البداية لـ (0,0)
    self.full_path = []
    self._build_board()                  # إعادة رسم اللوحة
```

---

## 🔘 GA Parameters Frame

```python
self._ga_frame = tk.Frame(p, bg=SURFACE)
# يُظهَر فقط حين يختار المستخدم "Genetic":
self._ga_frame.pack(fill="x", ...)
# ويُخفَى حين يختار "Backtracking":
self._ga_frame.pack_forget()
```

`pack_forget()` لا تحذف الـ widget، فقط تخفيها من الشاشة.

---

## ❓ أسئلة قد تُسأل عنها

**س: لماذا `int(float(val))`؟**  
ج: لأن `ttk.Scale` يُرسل القيمة كـ string أحياناً، وبعض الأنظمة ترسلها كـ "6.0" — نحولها لـ float أولاً ثم لـ int.

**س: ما الفرق بين `tk.Label` و `ttk.Scale`؟**  
ج: `tk.Label` من المكتبة القديمة (أكثر تحكماً في الألوان)، `ttk.Scale` من مكتبة الـ themed widgets (أجمل مظهراً).

**س: لماذا `_lbl()` دالة مساعدة وليس كتابة Label مباشرة؟**  
ج: لأننا نستخدم نفس الإعدادات (font, bg, fg) كثيراً — الدالة المساعدة تمنع التكرار (DRY principle).

**س: ما `tk.StringVar`؟**  
ج: متغير tkinter خاص مرتبط بـ Widget — حين يتغير المتغير بـ `.set()` يتحدث الـ Widget تلقائياً دون الحاجة لإعادة تهيئته.

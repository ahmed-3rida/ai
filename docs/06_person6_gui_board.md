# 👤 Person 6 — GUI: Board Drawing & User Interaction

## ما هو دورك؟
أنت مسؤول عن **ملف `gui/board.py`** — كل ما يخص رسم لوحة الشطرنج والتفاعل معها.

---

## 📄 ملفك: `gui/board.py`

### الدوال التي تحتوي عليها

| الدالة | الوظيفة |
|---|---|
| `_build_board()` | رسم اللوحة من الصفر |
| `_on_canvas_click()` | معالجة ضغط المستخدم |
| `_mark_start()` | تمييز خانة البداية |
| `_reset_board()` | إعادة اللوحة لحالتها الأصلية |
| `_render_path()` | رسم مسار الفارس خطوة بخطوة |

---

## 🎨 `_build_board()` — رسم اللوحة

### كيف نحسب حجم الخلايا؟

```python
W = canvas.winfo_width()   # عرض الـ Canvas بالبيكسل
H = canvas.winfo_height()  # ارتفاع الـ Canvas بالبيكسل

cell = min((W - 10) // n, (H - 10) // n)   # أكبر خلية تتسع

ox = (W - cell * n) // 2   # offset أفقي للتوسيط
oy = (H - cell * n) // 2   # offset رأسي للتوسيط
```

اللوحة دائماً **مُوسّطة** مهما كان حجم النافذة.

### نمط الشطرنج

```python
color = LIGHT_SQ if (r + col) % 2 == 0 else DARK_SQ
```

- (0,0) → 0%2=0 → فاتح
- (0,1) → 1%2=1 → داكن
- (1,0) → 1%2=1 → داكن
- (1,1) → 2%2=0 → فاتح

### تخزين بيانات الخلايا

```python
self.cells[(r, col)] = {
    "rect": rect_id,    # معرف المستطيل في Canvas
    "text": text_id,    # معرف النص (رقم الخطوة)
    "x1": x1, "y1": y1,
    "x2": x2, "y2": y2,
    "color": color      # اللون الأصلي للاستعادة لاحقاً
}
```

---

## 👆 `_on_canvas_click()` — الضغط على الخلية

```python
def _on_canvas_click(self, event):
    if self.solving:        # لا تغير البداية أثناء الحل
        return
    for (r, col), info in self.cells.items():
        if (info["x1"] <= event.x <= info["x2"] and
                info["y1"] <= event.y <= info["y2"]):
            self.start_r = r        # حفظ موقع البداية
            self.start_c = col
            self._hint_var.set(f"Start: ({r+1}, {col+1})")
            self._reset_board()     # مسح اللوحة
            return
```

---

## 🟢 `_mark_start()` — تمييز نقطة البداية

```python
canvas.create_rectangle(
    x1+2, y1+2, x2-2, y2-2,
    outline=START_OUT,   # إطار تركوازي
    width=3,
    tags="start_outline"
)
```

نرسم إطاراً بداخل الخلية (offset +2 من كل جهة).

---

## 🎬 `_render_path()` — رسم المسار

```python
def _render_path(self, path, up_to):
    self._reset_board()
    slice_ = path[:up_to]     # أول up_to خطوات فقط

    for i, (r, col) in enumerate(slice_):
        if i < len(slice_) - 1:
            # خانة مزارة → لون داكن + رقم الخطوة
            canvas.itemconfig(rect, fill=VISITED)
            canvas.itemconfig(text, text=str(i+1))
        else:
            # الموقع الحالي للفارس
            canvas.itemconfig(rect, fill=CURRENT)
            canvas.create_text(mx, my, text="♞", ...)
```

### لماذا `up_to`؟
لأن الأنيميشن يستدعي `_render_path(path, 1)` ثم `(path, 2)` ثم `(path, 3)` ... بمرور الوقت — هكذا تُرى الحركة تدريجياً.

---

## 🔧 `_reset_board()` — إعادة الضبط

```python
def _reset_board(self):
    for (r, col), info in self.cells.items():
        canvas.itemconfig(info["rect"], fill=info["color"])  # لون أصلي
        canvas.itemconfig(info["text"], text="")             # مسح الرقم
    canvas.delete("knight_icon")   # مسح أيقونة الفارس
    self._mark_start()             # إعادة رسم حدود البداية
```

---

## ❓ أسئلة قد تُسأل عنها

**س: ما هو `tk.Canvas`؟**  
ج: widget في tkinter يسمح برسم أشكال (مستطيلات، نصوص، خطوط...) وتحديثها ديناميكياً.

**س: لماذا نحذف `"start_outline"` قبل رسمه مجدداً؟**  
ج: لأن `create_rectangle()` يُضيف شكلاً جديداً كل مرة دون حذف القديم. `canvas.delete(tag)` يزيل كل الأشكال بنفس الـ tag.

**س: لماذا `self.cells` dictionary وليس list؟**  
ج: لأننا نبحث دائماً بالمفتاح `(row, col)` — الـ dictionary أسرع بكثير من البحث في list.

**س: ما معنى `winfo_width()`؟**  
ج: تُرجع العرض الفعلي للـ widget بالبيكسل في اللحظة الحالية. نستدعيها بعد ظهور النافذة لأن القيمة تكون 1 قبل ذلك.

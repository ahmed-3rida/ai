# 👤 Person 8 — GUI: Solver Threading & Animation

## ما هو دورك؟
أنت مسؤول عن **ملف `gui/solver.py`** — كيف يتواصل الـ GUI مع الخوارزميات، وكيف يتحرك الفارس على الشاشة.

---

## 📄 ملفك: `gui/solver.py`

### الدوال

| الدالة | الوظيفة |
|---|---|
| `_set_status()` | تحديث شريط الحالة السفلي |
| `_run_solver()` | زر SOLVE — يُطلق الخوارزمية |
| `_run_bt()` | Worker thread للـ Backtracking |
| `_run_ga()` | Worker thread للـ GA |
| `_update_ga_progress()` | تحديث progress bar الـ GA |
| `_ga_done()` | بعد انتهاء الـ GA |
| `_finish()` | مشترك — يُظهر النتائج ويُشغل الأنيميشن |
| `_replay()` | إعادة تشغيل الأنيميشن |
| `_animate()` | محرك الأنيميشن |

---

## 🧵 لماذا نستخدم Threads؟

```
❌ بدون Thread:
   ضغط SOLVE → الخوارزمية تعمل → الـ GUI يتجمد تماماً
   المستخدم يظن البرنامج علق!

✅ مع Thread:
   ضغط SOLVE → Thread جديد يشغل الخوارزمية
              → الـ GUI يبقى متجاوباً ومتحرك
```

### القاعدة الذهبية في tkinter
> **لا تُعدّل الـ GUI من Thread غير الرئيسي!**

لذلك نستخدم `self.after(0, lambda: ...)` لإرسال النتيجة للـ thread الرئيسي.

---

## ▶️ `_run_solver()` — زر SOLVE

```python
def _run_solver(self):
    if self.solving:          # منع تشغيل مزدوج
        return

    self.solving = True
    self._run_btn.config(state="disabled", text="⏳ Solving…")
    self._reset_board()

    if self.algo.get() == "backtracking":
        threading.Thread(
            target=self._run_bt,   # ← الدالة التي ستشتغل في Thread
            daemon=True            # ← يُغلق مع النافذة تلقائياً
        ).start()
    else:
        threading.Thread(target=self._run_ga, daemon=True).start()
```

---

## 🔵 `_run_bt()` — Backtracking Thread

```python
def _run_bt(self):
    # هذا الكود يعمل في Thread منفصل
    from algorithms.backtracking import backtracking_solve
    path, elapsed, success = backtracking_solve(n, self.start_r, self.start_c)

    # إرسال النتيجة للـ thread الرئيسي بشكل آمن
    self.after(0, lambda: self._finish(path, elapsed, success))
```

---

## 🟢 `_run_ga()` — GA Thread

```python
def _run_ga(self):
    def cb(gen, best_fit, best_path):
        pct = int((gen / gens) * 100)
        # إرسال تحديث progress bar للـ main thread
        self.after(0, lambda: self._update_ga_progress(gen, best_fit, target, pct))

    ga = GeneticKnightsTour(n, start_x=self.start_r, ...)
    path, elapsed, success = ga.solve(
        callback=cb,
        stop_flag=lambda: self._stop   # ← يمكن إيقافه
    )
    self.after(0, lambda: self._ga_done(path, elapsed, success))
```

---

## 🎬 `_animate()` — محرك الأنيميشن

```python
def _animate(self, path):
    self._step = 0

    def tick():
        self._step += 1
        self._render_path(path, self._step)  # ارسم حتى الخطوة الحالية

        if self._step < len(path):
            delay = max(20, 350 - self.anim_delay.get())
            self._anim_after = self.after(delay, tick)  # موعد الـ tick التالي
        else:
            self._set_status("Tour complete!", "ok")  # اكتملت الجولة

    tick()  # ابدأ أول tick
```

### كيف تعمل `self.after(delay, tick)`؟
- `after(ms, func)` تقول لـ tkinter: **"بعد `ms` مللي ثانية، نفّذ `func`"**
- هذا يُشغل الأنيميشن **بدون تجميد الـ UI** — مثل setInterval في JavaScript

### حساب التأخير
```python
delay = max(20, 350 - self.anim_delay.get())
```
- slider على "slow" (20) → delay = 350 - 20 = 330ms (بطيء)
- slider على "fast" (300) → delay = 350 - 300 = 50ms (سريع)

---

## 📊 `_finish()` — عرض النتائج

```python
def _finish(self, path, elapsed, success):
    total = n * n
    cov = round(len(path) / total * 100)

    self._stat_squares.set(f"{len(path)}/{total}")
    self._stat_cov.set(f"{cov}%")
    self._stat_time.set(f"{elapsed:.4f}s")
    self._stat_result.set("✓" if success else "Partial")

    self.solving = False
    self._run_btn.config(state="normal", text="▶  SOLVE")
    self._anim_btn.config(state="normal")
    self._animate(path)   # ابدأ الأنيميشن
```

---

## ❓ أسئلة قد تُسأل عنها

**س: ما `daemon=True` في Thread؟**  
ج: يعني أن الـ Thread يُغلق تلقائياً حين تُغلق النافذة الرئيسية. بدونه، قد يبقى البرنامج شغالاً في الخلفية بعد الإغلاق.

**س: لماذا `lambda: self._finish(...)` وليس `self._finish(...)` مباشرة؟**  
ج: `self.after(0, self._finish(...))` ستُنفّذ `_finish()` فوراً لحساب القيمة. نريد تمرير **مرجع للدالة** مع المعاملات، فنلفها بـ lambda.

**س: ماذا يحدث لو ضغط المستخدم SOLVE مرتين؟**  
ج: `if self.solving: return` تمنع التشغيل المزدوج.

**س: لماذا `max(20, ...)`؟**  
ج: لمنع delay = 0 أو قيمة سالبة، لأن `self.after(0, ...)` يُنفَّذ فوراً دون توقف وسيُجمّد الـ UI.

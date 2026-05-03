# 👤 Person 3 — Backtracking + Warnsdorff's Algorithm

## ما هو دورك؟
أنت مسؤول عن **ملف `algorithms/backtracking.py`** — الخوارزمية الأولى في المشروع.

---

## 📄 ملفك: `algorithms/backtracking.py`

### ما هي Backtracking؟
**Backtracking** (الرجوع للوراء) هي أسلوب بحث منهجي:
1. جرب خطوة
2. إذا أفضت لحل → ممتاز ✅
3. إذا وصلنا لطريق مسدود → **ارجع للخطوة السابقة** وجرب خياراً آخر

---

## 🧭 خطوات الخوارزمية

```
ابدأ من (sx, sy)
│
├─ ضع الفارس على الخانة، ضعها في path، وعلّمها "مزارة"
│
├─ هل زرنا n² خانة؟ → نجاح! ✅
│
├─ اجمع كل الحركات القانونية المتاحة
│   └─ رتّبها بـ Warnsdorff (الأقل degree أولاً)
│
├─ لكل حركة:
│   └─ استدعِ bt() بشكل تكراري (Recursion)
│       ├─ نجح؟ → ارجع True
│       └─ فشل؟ → جرب التالية
│
└─ لا يوجد حل من هنا → تراجع (Backtrack)
    ├─ أزل الخانة من path
    ├─ علّمها "غير مزارة"
    └─ ارجع False
```

---

## 🔑 الكود المشروح

```python
def backtracking_solve(n, sx, sy):
    visited = [[False] * n for _ in range(n)]  # جدول تتبع الزيارات
    path = []                                   # ترتيب الزيارات

    def bt(x, y, step):
        visited[x][y] = True    # علّم الخانة الحالية
        path.append((x, y))     # أضفها للمسار

        if step == n * n:       # هل اكتملت الجولة؟
            return True

        # الحركات المتاحة مرتبة بـ Warnsdorff
        neighbours = valid_moves(x, y, n, visited)
        neighbours.sort(key=lambda p: degree(p[0], p[1], n, visited))

        for nx, ny in neighbours:
            if bt(nx, ny, step + 1):
                return True         # وُجد حل!

        # ───── BACKTRACK ─────
        visited[x][y] = False   # أعد الخانة للحالة الأصلية
        path.pop()              # أزل من المسار
        return False            # أخبر الأب بالفشل

    t0 = time.time()
    success = bt(sx, sy, 1)    # ابدأ من الخطوة 1
    elapsed = time.time() - t0

    return path, elapsed, success
```

---

## 📊 لماذا Warnsdorff يُسرّع Backtracking؟

### بدون Warnsdorff (ترتيب عشوائي)
- الخوارزمية تجرب الكثير من المسارات الخاطئة
- على لوحة 8×8 قد تأخذ **دقائق أو ساعات**

### مع Warnsdorff
- دائماً نذهب للخانة الأصعب وصولاً أولاً
- تقريباً لا يحدث Backtrack حقيقي
- على لوحة 8×8 تجد الحل في **أجزاء من الثانية**

---

## 🔄 مثال مصغر (لوحة 5×5)

```
بداية: (0,0)
path = [(0,0)]

→ (1,2): degree=3 ← الأقل
→ (2,4): degree=2 ← الأقل
→ (4,3): degree=4
... وهكذا حتى نزور الـ 25 خانة
```

---

## ⏱️ التعقيد الزمني

| الحالة | التعقيد |
|---|---|
| بدون heuristic | O(8^(n²)) — أسي مخيف |
| مع Warnsdorff | شبه خطي — عملياً O(n²) |

---

## ❓ أسئلة قد تُسأل عنها

**س: ما الفرق بين Backtracking وBrute Force؟**  
ج: Brute Force تجرب كل شيء بدون تفكير. Backtracking تتوقف مبكراً حين تعرف أن المسار لن يؤدي لحل.

**س: هل Backtracking دائماً تجد الحل إذا وُجد؟**  
ج: نعم، هي **Complete Algorithm** — إذا كان الحل موجوداً ستجده بالتأكيد.

**س: متى تحدث عملية Backtrack في مشروعنا؟**  
ج: نادراً جداً بفضل Warnsdorff. تحدث فقط حين نصل لطريق مسدود تماماً (0 حركات متاحة).

**س: لماذا نستخدم Recursion وليس Loop؟**  
ج: لأن Recursion تُدير تلقائياً **stack** لتتذكر جميع الخطوات السابقة، مما يجعل Backtrack طبيعياً جداً.

**س: ماذا يُرجع `backtracking_solve()` إذا فشلت الخوارزمية؟**  
ج: `path=[]`, `success=False`, والوقت المستغرق.

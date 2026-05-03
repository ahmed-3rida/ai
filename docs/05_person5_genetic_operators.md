# 👤 Person 5 — Genetic Algorithm: Selection, Mutation & Main Loop

## ما هو دورك؟
أنت مسؤول عن **الجزء الثاني من `algorithms/genetic.py`**:
- `tournament_select()` — انتقاء الأفضل
- `mutate()` — الطفرة
- `solve()` — الحلقة الرئيسية للخوارزمية

---

## 🏆 `tournament_select()` — انتقاء البطولة

### الفكرة
بدلاً من ترتيب كل الـ population (بطيء)، نختار عشوائياً `k` أفراد ونأخذ الأفضل بينهم.

```python
def tournament_select(self, population):
    sample = random.sample(population, min(self.tournament_k, len(population)))
    return max(sample, key=self.fitness)
```

### مثال مع k=5
```
population = [A(36), B(29), C(31), D(34), E(28), F(33), ...]
عشوائياً نختار: [B(29), D(34), A(36), F(33), E(28)]
الفائز: A (fitness=36) ✅
```

### لماذا Tournament وليس ترتيب كامل؟
| الطريقة | الميزة | العيب |
|---|---|---|
| Rank Selection | دقيق | بطيء O(n log n) |
| **Tournament** | سريع | يحتفظ بالتنوع |

---

## 🧬 `mutate()` — الطفرة

### الفكرة
**قطع المسار** عند نقطة عشوائية ثم **إعادة نمو الذيل** بطريقة جديدة.

```python
def mutate(self, path):
    cut = random.randint(1, len(path)-1)   # نقطة القطع
    new_path = list(path[:cut])            # احتفظ بالبداية

    # أعد رسم visited للجزء المحفوظ
    visited = [[False]*n for _ in range(n)]
    for (x, y) in new_path:
        visited[x][y] = True

    # نمّ الذيل من جديد بطريقة Warnsdorff + عشوائية
    x, y = new_path[-1]
    while moves := valid_moves(x, y, n, visited):
        moves.sort(key=lambda p: (degree(...), random.random()))
        x, y = moves[0]
        visited[x][y] = True
        new_path.append((x, y))

    return new_path
```

### مثال
```
path قبل الطفرة: [A→B→C→D→E→F→G] (length=7)
cut = 3
new_path: [A→B→C] + نمو جديد → [A→B→C→X→Y→Z→W] (مختلف!)
```

### لماذا هذا النوع من الطفرة؟
- يحافظ على الجزء الجيد من البداية
- يستكشف مسارات جديدة من منتصف الطريق
- أفضل من تغيير نقطة عشوائية واحدة

---

## 🔄 `solve()` — الحلقة الرئيسية

```python
def solve(self, callback=None, stop_flag=None):
    target = n * n
    population = [self.random_tour() for _ in range(self.pop_size)]
    best_path = max(population, key=self.fitness)

    for gen in range(self.generations):
        # 1. ترتيب الـ population
        population.sort(key=self.fitness, reverse=True)

        # 2. تحديث الأفضل
        if fitness(population[0]) > fitness(best_path):
            best_path = population[0]

        # 3. هل وجدنا الحل الكامل؟
        if fitness(best_path) == target:
            break

        # 4. بناء الجيل الجديد
        new_pop = population[:self.elite_size]   # النخبة تُحفظ
        while len(new_pop) < self.pop_size:
            p1 = self.tournament_select(population)
            child = self.mutate(p1)
            new_pop.append(child)
        population = new_pop

    return best_path, elapsed, success
```

### تسلسل الجيل الواحد

```
جيل قديم (sorted by fitness)
├─ أفضل 10% (elite) ───────────────────────→ جيل جديد (unchanged)
└─ باقي 90%:
    └─ لكل مقعد فارغ:
        1. tournament_select() → أفضل الآباء
        2. mutate()            → طفل متطور
        └─ أضفه للجيل الجديد
```

---

## 📈 كيف تتحسن الحلول جيلاً بعد جيل؟

```
الجيل 1:  أفضل fitness = 28/36
الجيل 10: أفضل fitness = 32/36
الجيل 50: أفضل fitness = 35/36
الجيل 87: أفضل fitness = 36/36 ✅ 
```

---

## ❓ أسئلة قد تُسأل عنها

**س: لماذا نحفظ النخبة (elitism) بدون تعديل؟**  
ج: لأننا لا نريد خسارة أفضل حل وجدناه. بدون elitism قد يتدهور الـ best_path.

**س: هل نستخدم Crossover في مشروعنا؟**  
ج: لا. الكود يستخدم فقط Mutation لأن Crossover صعب التطبيق على Knight's Tour (المسارات يجب أن تكون متصلة). هذا اختيار تصميمي مقبول ومُبرر.

**س: متى يتوقف `solve()` قبل انتهاء الأجيال؟**  
ج: حالتان: (1) إذا وجد حلاً كاملاً `fitness == n²`، أو (2) إذا ضغط المستخدم على زر الإيقاف `stop_flag()`.

**س: ما دور `callback`؟**  
ج: يُرسل تحديثات لواجهة المستخدم (progress bar) دون توقف الخوارزمية.

**س: لماذا `sort(reverse=True)` وليس `min()`؟**  
ج: لأننا نحتاج لترتيب كل الـ population لاستخراج النخبة `population[:elite_size]`.

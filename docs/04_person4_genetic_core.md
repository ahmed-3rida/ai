# 👤 Person 4 — Genetic Algorithm: Structure & Core Concepts

## ما هو دورك؟
أنت مسؤول عن **الجزء الأول من `algorithms/genetic.py`**:
- فهم فكرة الخوارزمية الجينية ومصطلحاتها
- `__init__()` — إعداد المعاملات
- `random_tour()` — توليد الكروموسومات
- `fitness()` — قياس جودة الحل

---

## 🧬 ما هي الخوارزمية الجينية؟

تُحاكي **عملية التطور الطبيعي**:

```
جيل أول (Population) من الحلول العشوائية
           ↓
     [تقييم الجودة - Fitness]
           ↓
    [انتقاء الأفضل - Selection]
           ↓
  [إنشاء جيل جديد - Mutation]
           ↓
    تكرار حتى الحل المثالي
```

---

## 📚 المصطلحات الأساسية

| المصطلح | التعريف | في مشروعنا |
|---|---|---|
| **Chromosome** | حل واحد محتمل | مسار كامل للفارس = list of (row, col) |
| **Population** | مجموعة الحلول | 200 مسار مختلف |
| **Fitness** | جودة الحل | عدد الخانات المزارة (max = n²) |
| **Generation** | دورة تطور واحدة | تقييم → انتقاء → طفرة |
| **Elite** | الأفضل الذين لا يتغيرون | أفضل 10% يُنقلون للجيل التالي |

---

## 📄 جزء الكود الخاص بك

### `__init__()` — المعاملات

```python
def __init__(self, n, start_x=0, start_y=0,
             pop_size=200, generations=1000,
             mutation_rate=0.15, elite_frac=0.1, tournament_k=5):
```

| المعامل | القيمة الافتراضية | الوظيفة |
|---|---|---|
| `n` | — | حجم اللوحة |
| `start_x, start_y` | 0, 0 | نقطة البداية التي اختارها المستخدم |
| `pop_size` | 200 | عدد الحلول في كل جيل |
| `generations` | 1000 | الحد الأقصى لعدد الأجيال |
| `mutation_rate` | 0.15 | احتمال الطفرة (15%) |
| `elite_frac` | 0.1 | نسبة النخبة المحفوظة (10%) |
| `tournament_k` | 5 | عدد المتنافسين في Tournament Selection |

---

### `random_tour()` — توليد كروموسوم

```python
def random_tour(self):
    visited = [[False]*n for _ in range(n)]
    x, y = self.start_x, self.start_y   # ← يبدأ من نقطة المستخدم دائماً!
    path = [(x, y)]
    visited[x][y] = True

    for _ in range(n*n - 1):
        moves = valid_moves(x, y, n, visited)
        if not moves:
            break
        # Warnsdorff + عشوائية → تنوع في الـ population
        moves.sort(key=lambda p: (degree(...), random.random()))
        x, y = moves[0]
        visited[x][y] = True
        path.append((x, y))

    return path
```

**النقطة المهمة:** الفارق عن Backtracking هو إضافة `random.random()` في الترتيب — هذا يجعل كل كروموسوم مختلفاً قليلاً رغم أنه يستخدم Warnsdorff.

---

### `fitness()` — قياس الجودة

```python
def fitness(self, path):
    return len(path)   # ببساطة: كم خانة زرنا؟
```

- الجولة الكاملة: `fitness = n²` (أعلى قيمة ممكنة)
- جولة جزئية (علقنا): `fitness < n²`

---

## 📊 مثال توضيحي

على لوحة 6×6 (target = 36):
```
chromosome A: 36 خانة → fitness = 36 ✅ (كاملة)
chromosome B: 29 خانة → fitness = 29
chromosome C: 31 خانة → fitness = 31
```

الخوارزمية ستنتقي A وC على حساب B وتطورهم.

---

## ❓ أسئلة قد تُسأل عنها

**س: لماذا لا نختار نقطة بداية عشوائية في `random_tour()`؟**  
ج: لأن المستخدم اختار نقطة معينة، ويجب أن كل الحلول تبدأ منها.

**س: لماذا نستخدم 200 كروموسوم وليس 1000؟**  
ج: تناسب بين التنوع والسرعة. 200 يعطي تنوعاً كافياً دون إبطاء البرنامج.

**س: هل يمكن أن يكون fitness = 0؟**  
ج: لا، لأننا نبدأ دائماً بخانة البداية، فالأقل هو fitness = 1.

**س: ما الفرق بين `mutation_rate=0.15` و `elite_frac=0.1`؟**  
ج: 
- `mutation_rate`: احتمال أن يتعرض الـ child لطفرة
- `elite_frac`: نسبة الأفضل الذين يُنقلون للجيل التالي بدون تعديل

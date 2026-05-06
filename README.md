<div align="center">
  <h1>🐴 Knight's Tour Problem Solver</h1>
  <p><strong>CS212 Artificial Intelligence — Spring 2025 | HNU University</strong></p>
  <p>A Python desktop application that solves the classic Knight's Tour chess problem using advanced AI algorithms with a fully interactive GUI.</p>
</div>

---

## 📑 جدول المحتويات (Table of Contents)
- [👥 تقسيم المهام وأعضاء الفريق](#-تقسيم-المهام-وأعضاء-الفريق-team-tasks-distribution)
- [📖 الشرح الشامل للمشروع](#-الشرح-الشامل-للمشروع-comprehensive-project-explanation)
  - [الخوارزميات (Algorithms)](#-أولاً-الخوارزميات-algorithms-folder)
  - [واجهة المستخدم (GUI)](#-ثانياً-واجهة-المستخدم-gui-folder)
- [🗂️ هيكل المشروع (Project Structure)](#-هيكل-المشروع-project-structure)
- [🚀 كيفية التشغيل (How to Run)](#-كيفية-التشغيل-how-to-run)
- [🎮 طريقة الاستخدام (How to Use)](#-طريقة-الاستخدام-how-to-use)

---

## 👥 تقسيم المهام وأعضاء الفريق (Team Tasks Distribution)

تم تقسيم الفريق إلى مجموعتين لضمان التركيز وتسهيل المذاكرة والمناقشة:

| 🧠 مجموعة الخوارزميات (Algorithms Group) | 🖥️ مجموعة واجهة المستخدم (GUI Group) |
| :--- | :--- |
| **مسؤوليات:** الذكاء الاصطناعي، طرق الحل، المنطق الرياضي | **مسؤوليات:** الواجهة الرسومية، التفاعل، عرض الحلول بصرياً |
| 1. **Ahmed Salman Hameed** *(Team Leader)* | 1. **Youssef Safwat Arnest** |
| 2. **Kareem Ayman Bakre** | 2. **Youssef Mohamed Mohamed** |
| 3. **Abdelrahman Mohamed Khairy** | 3. **Youssef Ramadan AbdelZaher** |
| 4. **Haya Mahmoud Mohamed** | 4. **Abdelrahman Mohamed Sayed** |
| | 5. **Mahmoud Mohamed Adwi** |

---

## 📖 الشرح الشامل للمشروع (Comprehensive Project Explanation)

هذا الجزء هو المرجع الأساسي لكل أعضاء الفريق لفهم ترابط المشروع بالكامل.

### 💡 فكرة المشروع
المشروع يحل مشكلة **"مسار الحصان" (Knight's Tour)**. المطلوب هو أن يتحرك حصان الشطرنج ليزور كل مربع على الرقعة (مثلاً 8x8) **مرة واحدة فقط** دون أي تكرار أو خروج عن حدود الرقعة.

### 🧠 أولاً: الخوارزميات (Algorithms Folder)
يحتوي على العقل المفكر للمشروع، ويتكون من 3 ملفات أساسية:

- 📄 **`moves.py` (قواعد الرقعة):** يحدد الحركات المتاحة للحصان بشكل `L` ويتأكد من صحتها. يحتوي على دالة `degree` لحساب الحركات المستقبلية المتاحة (أساس قاعدة Warnsdorff).
- 📄 **`backtracking.py` (خوارزمية التراجع):** تجربة المسارات خطوة بخطوة. مدعومة بـ **Warnsdorff's Heuristic** لاختيار المربع ذو الحركات المستقبلية الأقل، مما يسرع الحل بشكل هائل.
- 📄 **`genetic.py` (الخوارزمية الجينية):** محاكاة للتطور. تبدأ بمسارات عشوائية (Population)، تختار الأفضل (Tournament Selection)، وتحدث طفرات (Mutation) للوصول للحل الأمثل.

### 🖥️ ثانياً: واجهة المستخدم (GUI Folder)
مبني بمكتبة `tkinter` ومقسم بنظام الـ Mixins:

- 📄 **`app.py` (الإطار الرئيسي):** يجمع مكونات الواجهة ويقسم الشاشة للوحة التحكم والرقعة.
- 📄 **`controls.py` (لوحة التحكم):** أزرار التحكم، اختيار الخوارزمية، تغيير الحجم، وعرض الإحصائيات (الوقت ونسبة التغطية).
- 📄 **`board.py` (رقعة الشطرنج):** رسم الرقعة، تلقي ضغطات الماوس لتحديد نقطة البداية، ورسم حركة الحصان (Animation) خطوة بخطوة.
- 📄 **`solver.py` (التشغيل في الخلفية):** يستخدم `Threads` لتشغيل الخوارزميات في الخلفية لمنع تجمد الواجهة (Freezing) أثناء التفكير.

### ⚙️ ثالثاً: الإعدادات والتشغيل
- 📄 **`main.py`:** نقطة البداية (Entry Point) لتشغيل التطبيق.
- 📄 **`constants.py`:** الثوابت والألوان الخاصة بالتصميم الموحد.

---

## 🗂️ هيكل المشروع (Project Structure)

```text
knights_tour_project/
├── main.py                   # نقطة تشغيل المشروع الأساسية
├── constants.py              # ثوابت الألوان والإعدادات العامة
├── algorithms/               # 🧠 فولدر الخوارزميات (للمجموعة الأولى)
│   ├── moves.py              # حساب حركات الحصان المتاحة
│   ├── backtracking.py       # خوارزمية الـ Backtracking
│   └── genetic.py            # الخوارزمية الجينية
├── gui/                      # 🖥️ فولدر واجهة المستخدم (للمجموعة الثانية)
│   ├── app.py                # الواجهة الرئيسية
│   ├── board.py              # رقعة الشطرنج والجرافيكس
│   ├── controls.py           # لوحة التحكم والأزرار
│   └── solver.py             # الـ Threading والتشغيل في الخلفية
└── team_tasks/               # 📚 شروحات المذاكرة الخاصة بكل عضو في الفريق
```

---

## 🚀 كيفية التشغيل (How to Run)

### Requirements (المتطلبات)
- Python 3.9+
- No external packages needed — only the standard library (`tkinter`, `random`, `time`, `threading`)

### Run Command (أمر التشغيل)
```bash
python main.py
```

> **Development Platform:**
> - **GUI Library:** `tkinter` (built-in)
> - **IDE:** VS Code / PyCharm
> - **OS:** Windows / Linux / macOS

---

## 🎮 طريقة الاستخدام (How to Use)

1. 📏 **تحديد الحجم:** استخدم شريط التمرير (Slider) لاختيار حجم الرقعة (من 5 إلى 12).
2. 🎯 **نقطة البداية:** اضغط بالماوس على أي مربع في الرقعة لاختياره كنقطة بداية للحصان.
3. 🧠 **اختيار الخوارزمية:** اختر إما خوارزمية التراجع (Backtracking) أو الخوارزمية الجينية (Genetic).
4. ⚙️ **إعدادات الجينات (اختياري):** في حالة اختيار Genetic، يمكنك تعديل حجم الجيل (Population) وعدد الأجيال (Generations).
5. ▶️ **التشغيل:** اضغط على زر **SOLVE** وشاهد الحصان وهو يحل الرقعة.
6. 🔄 **إعادة التشغيل:** بعد انتهاء الحل، يمكنك الضغط على **Replay Animation** لمشاهدة الحركة مرة أخرى.

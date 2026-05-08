# شرح ملف `main.py` (نقطة البداية للمشروع)

هذا الملف هو **نقطة الدخول (Entry Point)** للمشروع بالكامل. عندما نريد تشغيل البرنامج، نقوم بتشغيل هذا الملف فقط. وظيفته الأساسية هي استدعاء واجهة المستخدم وتجهيز الألوان (الثيم) ثم تشغيل نافذة البرنامج.

إليك شرح الكود سطراً بسطر:

---

### 1. استدعاء المكتبات والملفات (Imports)

```python
import tkinter as tk
from tkinter import ttk
from constants import (SURFACE, SURFACE2, BORDER, ACCENT)
from gui import KnightsTourApp
```
- **`import tkinter as tk`**: نستدعي مكتبة `tkinter` وهي المكتبة الافتراضية في بايثون لإنشاء واجهات المستخدم الرسومية (GUI). نعطيها اسماً مختصراً `tk` لسهولة الاستخدام.
- **`from tkinter import ttk`**: نستدعي `ttk` وهي إضافة داخل `tkinter` توفر لنا أدوات (Widgets) ذات شكل أحدث ومحسّن (مثل شريط التقدم ProgressBar والمؤشر Scale).
- **`from constants import ...`**: نستورد الألوان التي سنستخدمها في الواجهة من ملف `constants.py` لضمان توحيد الألوان في كل البرنامج.
- **`from gui import KnightsTourApp`**: نستدعي الكلاس `KnightsTourApp` من مجلد `gui`، وهو الكلاس الذي يحتوي على كل واجهة البرنامج والتطبيقات.

---

### 2. دالة تطبيق الألوان `apply_theme`

```python
def apply_theme(app: KnightsTourApp) -> None:
```
- هذه الدالة تأخذ كائن البرنامج `app` وتقوم بتطبيق "ثيم" (Theme) معين عليه حتى تتناسق الألوان ويكون شكل البرنامج احترافياً (Dark Mode).

```python
    style = ttk.Style(app)
    style.theme_use("clam")
```
- **`style = ttk.Style(app)`**: ننشئ كائن `Style` للتحكم في شكل أدوات الـ `ttk`.
- **`style.theme_use("clam")`**: نستخدم ثيم اسمه `"clam"`، وهو ثيم مسطح (Flat Design) يأتي مع بايثون، ويسهل تغيير ألوانه لتناسب الثيم الداكن الذي نريده.

```python
    style.configure("TScale",
                    background=SURFACE,
                    troughcolor=SURFACE2,
                    sliderlength=16)
```
- هنا نقوم بتغيير شكل الـ **`Scale`** (مؤشر السرعة الموجود في الواجهة):
  - `background`: لون الخلفية الأساسية.
  - `troughcolor`: لون المجرى الذي يتحرك فيه المؤشر.
  - `sliderlength`: طول زر المؤشر نفسه (16 بيكسل).

```python
    style.configure("Horizontal.TProgressbar",
                    troughcolor=SURFACE2,
                    background=ACCENT,
                    bordercolor=BORDER,
                    lightcolor=ACCENT,
                    darkcolor=ACCENT)
```
- هنا نغير شكل **`ProgressBar`** (شريط التحميل الذي يظهر عند تشغيل الخوارزمية الجينية):
  - نجعل لونه (ACCENT) ولون خلفيته متناسقاً مع ألوان التطبيق.

---

### 3. نقطة البداية (تشغيل البرنامج)

```python
if __name__ == "__main__":
```
- هذا السطر مهم جداً في بايثون. معناه: "إذا تم تشغيل هذا الملف مباشرة (وليس استدعاؤه كـ Import في ملف آخر)، قم بتنفيذ الأكواد التي تحت هذا السطر".

```python
    app = KnightsTourApp()
```
- ننشئ نسخة (Object) من كلاس `KnightsTourApp`. هذه الخطوة تقوم حرفياً بإنشاء وبناء نافذة البرنامج بكل ما فيها من أزرار ورقعة الشطرنج.

```python
    apply_theme(app)
```
- نستدعي الدالة التي شرحناها بالأعلى لتلوين الـ ProgressBar والـ Scale وتطبيق الثيم الداكن على التطبيق الجديد.

```python
    app.mainloop()
```
- **`app.mainloop()`**: هذه الدالة هي المحرك الأساسي لأي واجهة مستخدم. هي عبارة عن "حلقة لا نهائية" (Infinite Loop) تُبقي نافذة البرنامج مفتوحة وتنتظر من المستخدم أن يفعل شيئاً (يضغط زر، يغير حجم الرقعة، إلخ). بدون هذا السطر، سيفتح البرنامج ويغلق فوراً في لمح البصر.

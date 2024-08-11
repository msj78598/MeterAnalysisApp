import pandas as pd
import gradio as gr

def process_file(file, min_average):
    # قراءة ملف الاكسل
    df = pd.read_excel(file)

    # التحقق من الشروط (إذا كانت إحدى القيم تساوي صفرًا بينما القيمتين الأخريين أو أحدهما أكبر من صفر)
    anomaly = df[
        ((df['A1'] == 0) & ((df['A2'] > 0) | (df['A3'] > 0))) |
        ((df['A2'] == 0) & ((df['A1'] > 0) | (df['A3'] > 0))) |
        ((df['A3'] == 0) & ((df['A1'] > 0) | (df['A2'] > 0)))
    ]

    # حساب متوسط القيم A1, A2, A3
    anomaly['متوسط'] = anomaly[['A1', 'A2', 'A3']].mean(axis=1)

    # تطبيق الفلتر: عرض الحالات التي يكون فيها المتوسط أعلى من الحد الأدنى المحدد
    anomaly = anomaly[anomaly['متوسط'] >= min_average]

    # ترتيب الحالات بناءً على قيمة المتوسط من الأكبر إلى الأصغر
    anomaly = anomaly.sort_values(by='متوسط', ascending=False)

    # حساب عدد الحالات المكتشفة
    num_cases = len(anomaly)

    # حفظ النتائج في ملف اكسل جديد
    output_file = "anomalies_filtered.xlsx"
    anomaly.to_excel(output_file, index=False)

    return anomaly, output_file, num_cases

# إعداد واجهة المستخدم
interface = gr.Interface(
    fn=process_file,
    inputs=[
        gr.File(label="ارفع ملف الاكسل الخاص بالعدادات"),
        gr.Number(label="حدد الحد الأدنى لقيمة المتوسط", value=0)
    ],
    outputs=[
        gr.DataFrame(label="العدادات ذات القيم الغير طبيعية مرتبة حسب المتوسط"),
        gr.File(label="تحميل الملف"),
        gr.Number(label="عدد الحالات المكتشفة", interactive=False)
    ],
    title="تحليل أحمال العدادات لاكتشاف حالات الفاقد",
    description="ارفع ملف الاكسل الذي يحتوي على رقم الساعة والامبير ليتم تحليلها وتحديد الحالات"
)

# تشغيل التطبيق
interface.launch(share=True)

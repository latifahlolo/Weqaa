import streamlit as st
import google.generativeai as genai
import json
import re  # استيراد مكتبة التعبيرات النمطية

# 🔑 إعداد مفتاح Google Gemini API
genai.configure(api_key="AIzaSyBdIOwS9L2zx090u7HI_i6JyDUPWP1OTvc")  # استبدل بمفتاحك الصحيح

def solve_database_issue(issue_description):
    """
    🎯 مساعد شخصي لحل مشاكل الموظفين في قاعدة البيانات
    """
    prompt = f"""
    🎯 **مهمتك كمساعد ذكاء اصطناعي:**
    أنت مساعد موظفي مركز وقاء في حل المشاكل المتعلقة بقاعدة البيانات. 

    ✅ **وصف المشكلة:**  
    {issue_description}
    
    🔹 **تعليمات صارمة:**
    1️⃣ **افهم المشكلة بدقة وحدد السبب الأساسي لها.**  
    2️⃣ **قم بتحليل المشكلة واقترح حلاً مناسبًا يتماشى مع طبيعة الخطأ أو الحاجة.**  
    3️⃣ **قدم نصيحة لتجنب حدوث المشكلة مستقبلاً.**  
    4️⃣ **قم بإضافة خطوات تنفيذ الحل بشكل واضح وبترتيب منطقي يساعد الموظف في الحل.**  
    5️⃣ **لا تقدم أي معلومات غير ذات صلة. يجب أن يكون الإخراج بصيغة JSON فقط.**
    
    🔍 **مثال على الإخراج الصحيح:**  
    ```json
    {{
        "problem_analysis": "المشكلة تتعلق بعدم العثور على حقل معين في الجداول، وقد يكون السبب أن الحقل غير موجود أو أن هناك خطأ في الاستعلام.",
        "suggested_solution": "تحقق من أسماء الحقول المتاحة في الجداول عبر فحص بنية قاعدة البيانات، وإذا لم يكن الحقل موجودًا، فقم بإضافته.",
        "prevention_tip": "تأكد من توثيق أسماء الحقول في مستند مرجعي، وتوحيد التسمية عند إنشاء الجداول لتجنب الالتباس.",
        "solution_steps": [
            "افتح أداة إدارة قاعدة البيانات (مثل SQL Server Management Studio أو phpMyAdmin).",
            "قم بتنفيذ الاستعلام التالي للتحقق من وجود الحقل: `SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'اسم_الجدول';`",
            "إذا لم يكن الحقل موجودًا، استخدم الأمر التالي لإضافته: `ALTER TABLE اسم_الجدول ADD اسم_الحقل نوع_البيانات;`",
            "احفظ التغييرات وأعد تشغيل أي عمليات تعتمد على هذا الحقل لضمان عملها بشكل صحيح."
        ]
    }}
    ```

    ❌ **لا تخرج أي شيء خارج JSON!**
    """

    try:
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2
            )
        )

        response_text = response.text.strip()

        # 🔍 **محاولة استخراج JSON من النص باستخدام التعبيرات النمطية (Regex)**
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)  # تحويل النص إلى JSON
        
        return {"error": "⚠️ النموذج لم يرجع استجابة بصيغة JSON، حاول مجددًا."}

    except Exception as e:
        return {"error": f"❌ حدث خطأ أثناء معالجة المشكلة: {str(e)}"}

# 📌 **واجهة Streamlit**
st.title("🛠️ مساعدك الذكي لحل مشاكل قاعدة البيانات")

st.write("🚀 أدخل وصف المشكلة التي تواجهها في قاعدة البيانات وسيساعدك مساعدك الذكي في تقديم حلول عملية بخطوات تنفيذ واضحة")

# ✍️ إدخال وصف المشكلة من المستخدم
issue_description = st.text_area("✍️ أدخل المشكلة هنا:", height=150)

if st.button("🔍 حل المشكلة"):
    if issue_description.strip():
        st.write("🔄 **جارٍ تحليل المشكلة...**")

        result = solve_database_issue(issue_description)  # تشغيل تحليل المشكلة

        # 🔍 **عرض النتيجة الأولية لفحص أي خطأ**
        st.write("🔍 النتيجة الأولية:", result)

        st.subheader("🔹 الحل المقترح:")
        st.json(result)  # عرض النتيجة بصيغة JSON

        if "solution_steps" in result:
            st.subheader("📝 خطوات التنفيذ:")
            for idx, step in enumerate(result["solution_steps"], 1):
                st.write(f"{idx}. {step}")
    else:
        st.warning("⚠️ الرجاء إدخال وصف المشكلة قبل طلب الحل!")

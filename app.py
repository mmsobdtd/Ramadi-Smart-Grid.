import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. إعدادات الصفحة لتناسب التابلت والموبايل
st.set_page_config(
    page_title="Ramadi Smart Grid - Mohammed Nabeel",
    page_icon="⚡",
    layout="wide"
)

# تحسين المظهر بالتنسيق العربي
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-testid="stMetricValue"] { font-size: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ نظام التوأم الرقمي لمراقبة محولات الرمادي")
st.write("مشروع هندسي مقترح لتحليل الحالة الفنية للمحولات باستخدام الذكاء الاصطناعي")

# 2. لوحة التحكم الجانبية (Sidebar)
st.sidebar.header("🕹️ لوحة محاكاة الظروف")
selected_area = st.sidebar.selectbox(
    "اختر منطقة الدراسة في الرمادي:",
    ["حي الملعب", "شارع المستودع", "منطقة التأميم", "حي المعلمين", "الجزيرة"]
)

ambient_temp = st.sidebar.slider("درجة حرارة الجو الخارجية (°C)", 10, 55, 42)
transformer_rating = 1000 # kVA (قيمة افتراضية للمحولة)

# 3. توليد بيانات المحاكاة (بدون أخطاء التاريخ)
# سنقوم بتوليد 24 ساعة كقائمة نصوص لتجنب مشاكل مكتبة Pandas
hours = [f"{i:02d}:00" for i in range(24)]
# محاكاة نمط الحمل في الرمادي (يزداد في الظهيرة)
np.random.seed(42)
base_load = 300 + 400 * np.sin(np.linspace(0, np.pi, 24))**2 
noise = np.random.normal(0, 15, 24)
load_profile = (base_load + noise).clip(min=100)

# 4. الحسابات الهندسية (Core Engineering Logic)
# التيار الحالي (آخر قيمة في المحاكاة)
current_load_amp = load_profile[-1]

# معادلة حرارة الملفات (Simplified Hotspot Temperature Model)
# Ths = Tamb + (Rise * (Load/Rated)^2)
hotspot_temp = ambient_temp + (50 * (current_load_amp / 600)**2)

# حساب مؤشر الصحة (Health Index)
# يعتمد على الحرارة والحمل الزائد
thermal_penalty = max(0, (hotspot_temp - 90) * 1.5) if hotspot_temp > 90 else 0
load_penalty = max(0, (current_load_amp - 500) * 0.1) if current_load_amp > 500 else 0
health_index = max(0, 100 - thermal_penalty - load_penalty)

# 5. عرض النتائج (Dashboard Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("المنطقة المختارة", selected_area)
col2.metric("الحمل الحالي", f"{current_load_amp:.1f} A")
col3.metric("حرارة المحولة", f"{hotspot_temp:.1f} °C")
col4.metric("مؤشر الصحة (HI)", f"{health_index:.1f}%")

st.markdown("---")

# 6. الرسم البياني للأحمال
st.subheader("📊 تحليل منحنى الحمل اليومي (Load Profile)")
df = pd.DataFrame({'الساعة': hours, 'الحمل (أمبير)': load_profile})
fig = px.area(df, x='الساعة', y='الحمل (أمبير)', 
              title=f"تذبذب الطاقة في {selected_area}",
              color_discrete_sequence=['#FF4B4B'])
st.plotly_chart(fig, use_container_width=True)

# 7. قسم التشخيص التنبؤي (Predictive Diagnostics)
st.subheader("🔍 تقرير التشخيص التنبؤي")
c1, c2 = st.columns(2)

with c1:
    if health_index > 80:
        st.success("✅ الحالة ممتازة: المحولة تعمل ضمن النطاق التصميمي الآمن.")
    elif health_index > 50:
        st.warning("⚠️ حالة متوسطة: يوصى بجدولة فحص دوري للزيت والتبريد.")
    else:
        st.error("🚨 حالة حرجة: خطر الاحتراق مرتفع! النظام يوصي بتخفيف الأحمال فوراً.")

with c2:
    st.info(f"**توصية النظام:** بناءً على حرارة الجو في الرمادي ({ambient_temp}°C)، المحولة تفقد من عمرها الافتراضي بمعدل {1.5 if hotspot_temp > 95 else 1.0}x أسرع من الطبيعي.")

# 8. زر التحكم عن بعد
if st.button("🔴 تنفيذ فصل اضطراري (Emergency Trip)"):
    st.critical("تم إرسال إشارة الفصل إلى القاطع الرئيسي لمحولة " + selected_area)
    

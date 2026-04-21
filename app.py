import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="Ramadi Smart Grid", layout="wide")

st.title("⚡ نظام مراقبة محولات الرمادي الذكي")
st.markdown("---")

# لوحة التحكم الجانبية
st.sidebar.header("⚙️ إعدادات المحاكاة")
area = st.sidebar.selectbox("اختر المنطقة في الرمادي", ["حي الملعب", "شارع المستودع", "التأميم", "حي الأندلس"])
ambient_temp = st.sidebar.slider("درجة حرارة الجو الآن (°C)", 15, 55, 45)

# توليد بيانات محاكاة (Simulation)
np.random.seed(42)
times = pd.date_range(start="2026-04-21 00:00", periods=24, freq='H')
# محاكاة حمل كهربائي يزداد في الظهيرة
load_data = [200 + 300 * np.sin((i-6)*np.pi/12)**2 + np.random.randint(-20, 20) for i in range(24)]

df = pd.DataFrame({'Time': times, 'Load (Amper)': load_data})

# حساب مؤشر الصحة (Health Index) بناءً على معادلة هندسية
current_load = load_data[-1] # آخر قيمة
internal_temp = ambient_temp + (current_load**2 / 5000)
health_index = max(0, 100 - (internal_temp * 0.4) - (max(0, current_load-400) * 0.3))

# عرض المؤشرات الرئيسية
col1, col2, col3 = st.columns(3)
col1.metric("الحمل الحالي في " + area, f"{current_load:.1f} A")
col2.metric("الحرارة المقدرة للملفات", f"{internal_temp:.1f} °C")
col3.metric("مؤشر صحة المحولة", f"{health_index:.1f}%")

# رسم بياني تفاعلي
st.subheader("📊 مخطط الأحمال خلال 24 ساعة")
fig = px.line(df, x='Time', y='Load (Amper)', title=f"استهلاك الطاقة في منطقة {area}")
st.plotly_chart(fig, use_container_width=True)

# نظام التنبيه الذكي (Decision Support System)
st.subheader("🛡️ حالة النظام والقرارات")
if health_index < 40:
    st.error("🚨 خطر مرتفع! النظام يقترح فصل المحولة تلقائياً لمنع الاحتراق.")
    if st.button("تفعيل الفصل الاضطراري (Trip)"):
        st.write("✅ تم إرسال أمر الفصل إلى القاطع بنجاح.")
elif health_index < 70:
    st.warning("⚠️ تنبيه: المحولة تحت ضغط حراري عالي. يرجى موازنة الأحمال.")
else:
    st.success("✅ النظام يعمل بكفاءة عالية.")
  

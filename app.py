import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="Ramadi Grid Defender AI", layout="wide", initial_sidebar_state="expanded")

# CSS لتنسيق الواجهة كأنها نظام تشغيل عسكري
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    direction: rtl; text-align: right;
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ منظومة 'درع الشبكة' الذكية - إصدار الرمادي 2026")
st.write("الجيل القادم من إدارة الشبكات: كشف التجاوزات، التنبؤ بالأعطال، والإدارة الذاتية.")

# --- لوحة التحكم الجانبية المتقدمة ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2991/2991163.png", width=100)
st.sidebar.header("⚡ التحكم بالمنظومة")
mode = st.sidebar.radio("اختر وضع التشغيل:", ["الوضع الطبيعي", "محاكاة تجاوز حرج", "هجوم سيبراني على العدادات"])
grid_stability = st.sidebar.slider("استقرارية التردد (Hz)", 49.0, 51.0, 50.0)

# --- محرك التحليل الجنائي (Forensics Engine) ---
def run_grid_analysis(mode):
    # محاكاة بيانات 24 ساعة
    hours = [f"{i:02d}:00" for i in range(24)]
    official_load = 200 + 100 * np.sin(np.linspace(0, np.pi, 24)) + np.random.normal(0, 5, 24)
    
    if mode == "محاكاة تجاوز حرج":
        actual_load = official_load + 150 + np.random.normal(0, 10, 24)
        theft_detected = True
        risk_level = "High"
    elif mode == "هجوم سيبراني على العدادات":
        actual_load = official_load + 20 # فرق بسيط يصعب كشفه
        official_load = official_load - 50 # العداد "يكذب" ويقلل القراءة
        theft_detected = True
        risk_level = "Cyber Alert"
    else:
        actual_load = official_load + 10
        theft_detected = False
        risk_level = "Low"
    
    return hours, official_load, actual_load, theft_detected, risk_level

hours, official, actual, detected, risk = run_grid_analysis(mode)

# --- عرض المؤشرات الاستراتيجية ---
cols = st.columns(4)
diff = actual[-1] - official[-1]
loss_cost = diff * 0.15 # فرضية سعر الكيلوواط

cols[0].metric("إجمالي الفقد (أمبير)", f"{diff:.1f} A", delta="تجاوز!" if detected else "طبيعي", delta_color="inverse")
cols[1].metric("الخسارة المالية اللحظية", f"{loss_cost:.2f} $")
# معادلة عمر المحولة الافتراضي (Simplified IEEE)
transformer_life = max(0, 100 - (diff * 0.5) - (20 if risk == "High" else 0))
cols[2].metric("صحة قلب المحولة", f"{transformer_life}%")
cols[3].metric("مستوى الأمان السيبراني", "98%" if mode != "هجوم سيبراني على العدادات" else "45% ⚠️")

st.markdown("---")

# --- الرسوم البيانية المتقدمة ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 مقارنة الأحمال: الرسمي vs الفعلي")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=official, name="القراءات الرسمية (عدادات)", fill='tozeroy', line=dict(color='#00CC96')))
    fig.add_trace(go.Scatter(x=hours, y=actual, name="الحمل الفعلي (المحولة)", line=dict(color='#FF4B4B', dash='dot')))
    fig.update_layout(template="plotly_dark", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🎯 تحليل مكان التجاوز (AI)")
    # محاكاة لتحديد الموقع بناءً على ممانعة الشبكة
    zones = ["زقاق 1", "زقاق 2", "زقاق 3", "زقاق 4"]
    theft_prob = [10, 85, 15, 5] if detected else [5, 5, 5, 5]
    fig_bar = px.bar(x=zones, y=theft_prob, labels={'x':'الزقاق', 'y':'احتمالية التجاوز %'}, color=theft_prob, color_continuous_scale='Reds')
    fig_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- ميزة التنبؤ وحماية الشبكة ---
st.subheader("🤖 قرارات الذكاء الاصطناعي لحماية الشبكة")
if detected:
    with st.expander("⚠️ تحليل التهديد والإجراء المقترح", expanded=True):
        st.write(f"**نوع التجاوز:** {'تلاعب ببروتوكول البيانات' if mode == 'هجوم سيبراني على العدادات' else 'ربط فيزيائي مباشر (شنكال)'}")
        st.write(f"**الموقع الدقيق:** تم رصد تشوه في الموجة الحاملة للبيانات بين العقدة B و C في {zones[1]}.")
        st.write(f"**الإجراء التلقائي:** تم إرسال أمر برمجياً للعدادات في {zones[1]} لزيادة تردد أخذ العينات (Sampling Rate) لمحاصرة المتجاوز.")
        if st.button("تفعيل موازنة الأحمال (Load Balancing)"):
            st.warning("جاري تقليل قدرة السحب للأجهزة غير الضرورية في المنطقة لإنقاذ المحولة من الانفجار...")
else:
    st.success("✅ الشبكة مستقرة. لا توجد أنماط مشبوهة في استهلاك البيانات أو الطاقة.")

# --- قسم الأبحاث (For the Paper) ---
st.markdown("---")
st.info("💡 **ملاحظة بحثية:** هذا النظام يستخدم تقنية 'Network Slicing' لضمان وصول بيانات الطوارئ حتى في حالات الازدحام الشديد للشبكة في مدينة الرمادي.")

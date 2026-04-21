import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import find_peaks

# 1. إعدادات الواجهة (رتم سريع وتصميم احترافي)
st.set_page_config(page_title="Ramadi Grid Radar", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ نظام رادار كشف التجاوزات الذكي - مدينة الرمادي")
st.write("تحليل ممانعة الشبكة وبصمة الأجهزة (Advanced Grid Forensics)")

# 2. لوحة التحكم بالمحاكاة (Sidebar)
st.sidebar.header("🕹️ التحكم في السيناريو")
scenario = st.sidebar.selectbox("حالة الشبكة:", ["عمل طبيعي", "تجاوز (شنكال ميكانيكي)", "تجاوز ذكي (إنفيرتر)"])
tap_distance = st.sidebar.slider("مسافة التجاوز التقديرية (متر)", 0, 100, 45) if scenario != "عمل طبيعي" else 0

# 3. محرك المحاكاة (The Engineering Engine)
# توليد إشارة "السونار" PLC Ping
t = np.linspace(0, 0.02, 1000) # موجة واحدة 50Hz
signal = np.sin(2 * np.pi * 50 * t)

# إضافة تشويه (Reflection) بناءً على المسافة في حال وجود تجاوز
if "تجاوز" in scenario:
    # محاكاة انعكاس الإشارة (Impedance Mismatch)
    reflection = 0.3 * np.sin(2 * np.pi * 50 * (t - (tap_distance/300))) 
    signal = signal + reflection
    
    # إضافة توافقيات في حال كان التجاوز لجهاز إنفيرتر
    if "إنفيرتر" in scenario:
        harmonics = 0.15 * np.sin(2 * np.pi * 150 * t) + 0.1 * np.sin(2 * np.pi * 250 * t)
        signal += harmonics

# 4. تحليل البيانات (Network Analysis)
# حساب نسبة التشوه الكلي (THD)
thd = np.sqrt(np.sum(signal**2) - np.sum(np.sin(2 * np.pi * 50 * t)**2)) / np.sum(np.sin(2 * np.pi * 50 * t)**2) * 100

# 5. عرض النتائج (Dashboard)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("حالة الربط الفيزيائي", "مستقرة" if scenario == "عمل طبيعي" else "تداخل إشارة (Reflection)")
with col2:
    status_color = "green" if thd < 5 else "red"
    st.metric("نسبة التشوه (THD)", f"{thd:.2f}%", delta="-طبيعي" if thd < 5 else "تجاوز مكتشف", delta_color="inverse")
with col3:
    location = "لا يوجد" if tap_distance == 0 else f"بعد {tap_distance} متر"
    st.metric("موقع التجاوز المحتمل", location)

st.markdown("---")

# 6. الرسوم البيانية (Visualizing the Invisible)
c1, c2 = st.columns(2)

with c1:
    st.subheader("📉 تحليل شكل موجة التيار (Waveform)")
    fig_wave = go.Figure()
    fig_wave.add_trace(go.Scatter(y=signal, name="الإشارة المستلمة", line=dict(color='#FF4B4B')))
    fig_wave.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_wave, use_container_width=True)

with c2:
    st.subheader("📊 التحليل الترددي (Spectrum)")
    # حساب FFT لإظهار البصمة الترددية
    fft_res = np.abs(np.fft.fft(signal))[:100]
    fig_fft = go.Figure(go.Bar(y=fft_res, marker_color='#00CC96'))
    fig_fft.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_fft, use_container_width=True)

# 7. التقرير الجنائي للشبكة (Network Forensics)
st.subheader("🔍 التقرير الذكي للنظام")
if scenario == "عمل طبيعي":
    st.success("✅ جميع القراءات مطابقة للعدادات الرسمية في الرمادي. لا يوجد ضياع غير فني.")
elif scenario == "تجاوز (شنكال ميكانيكي)":
    st.error(f"🚨 اكتشاف ربط غير قانوني! انعكاس الإشارة يشير لوجود نقطة سحب بين العمود 3 والعمود 4 (تقريباً عند متر {tap_distance}).")
else:
    st.error("🚨 اكتشاف تجاوز 'ذكي'! البصمة الترددية تشير لتشغيل (جهاز إنفيرتر - سبلت) خارج نطاق العداد.")
    st.info("💡 نصيحة المهندس: هذا النوع من التجاوز يرفع حرارة المحولة بنسبة 20% أسرع من الأحمال العادية.")

# 8. خريطة تفاعلية بسيطة (Mockup)
st.subheader("📍 خريطة الزقاق المستهدف")
map_data = pd.DataFrame({
    'lat': [33.4209, 33.4215],
    'lon': [43.3031, 43.3040],
    'name': ['المحولة الرئيسية', 'منطقة التجاوز المكتشفة']
})
st.map(map_data)

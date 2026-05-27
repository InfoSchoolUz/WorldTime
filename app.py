import streamlit as st
import datetime
import time
import pytz

# Sahifa sozlamalari (Keng ekran rejimi)
st.set_page_config(layout="wide", page_title="Universal Digital-7 Time Network")

# 1. Digital-7 Shriftini ulash va UI Dizayni (CSS)
st.markdown(
    """
    <style>
    /* Digital-7 shriftini tashqi CDN tarmoqdan yuklab olamiz */
    @import url('https://fonts.cdnfonts.com/css/digital-7');
    
    /* Chap panel (Sidebar) uchun uslublar */
    .sidebar-text {
        font-family: 'Digital-7', monospace; /* Standartlar ham elektron shriftda */
        font-size: 20px; /* Digital-7 shrifti uchun mos o'lcham */
        color: #00FF66; /* Neon yashil */
        background-color: #111111;
        padding: 4px 10px;
        border-radius: 5px;
        margin-bottom: 12px;
        border-left: 4px solid #ff9800;
        letter-spacing: 2px;
    }
    .sidebar-title {
        font-weight: bold;
        color: #ffffff;
        margin-top: 12px;
        font-size: 13px;
        letter-spacing: 1px;
    }

    /* Asosiy ekran (Dashboard) uchun uslublar */
    .dashboard-card {
        background-color: #050505;
        border: 2px solid #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.9);
    }
    .city-lbl {
        color: #a0aec0;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: sans-serif;
    }
    
    /* AYNAN DIGITAL-7 CLOCK KLASSI */
    .digital-clock {
        font-family: 'Digital-7', sans-serif; /* Original Elektron Shrift */
        color: #00E6FF; /* Neon Moviy */
        font-size: 65px; /* Shrift ko'rinishi uchun o'lcham kattalashtirildi */
        letter-spacing: 3px;
        margin: 5px 0;
        text-shadow: 0 0 15px rgba(0, 230, 255, 0.7);
    }
    .ms-text {
        font-size: 40px; /* Millisoniyalar ham Digital-7 da, faqat kichikroq */
        color: #0088cc; 
    }
    .date-lbl {
        color: #4a5568;
        font-size: 13px;
        font-weight: 500;
        font-family: sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. CHAP PANEL (Sidebar) - 10 ta Vaqt Standarti Menyusi
st.sidebar.markdown("## 🛰️ Vaqt Standartlari")
st.sidebar.markdown("---")

sb_placeholders = {}
standards = [
    "1. UTC (Coordinated Universal Time)", 
    "2. GMT (Greenwich Mean Time)", 
    "3. TAI (International Atomic Time)", 
    "4. UNIX Timestamp (Epoch Time)", 
    "5. GPS Time (Global Positioning)", 
    "6. UT1 (Astronomical Time)", 
    "7. TT (Terrestrial Time)", 
    "8. Galileo Time (GST)", 
    "9. GLONASS Time (Russian)", 
    "10. BeiDou Time (BDS)"
]

for std in standards:
    st.sidebar.markdown(f"<div class='sidebar-title'>{std}</div>", unsafe_allow_html=True)
    sb_placeholders[std] = st.sidebar.empty()


# 3. ASOSIY DASHBOARD - 8 ta Davlat/Shahar Ro'yxati
st.title("🎯 Global Real-Time Clock Dashboard")
st.write("Dunyoning 8 ta strategik nuqtasidagi jonli vaqt ko'rsatkichlari (Digital-7 formatida):")

cities = {
    "Toshkent 🇺🇿": "Asia/Tashkent",
    "London 🇬🇧": "Europe/London",
    "Nyu-York 🇺🇸": "America/New_York",
    "Tokio 🇯🇵": "Asia/Tokyo",
    "Makka 🇸🇦": "Asia/Riyadh",
    "Moskva 🇷🇺": "Europe/Moscow",
    "Pekin 🇨🇳": "Asia/Shanghai",
    "Sidney 🇦🇺": "Australia/Sydney"
}

# 8 ta davlatni ekranga 4 tadan qilib 2 qatorga joylashtiramiz
row1_cols = st.columns(4)
row2_cols = st.columns(4)
all_columns = row1_cols + row2_cols
main_placeholders = []

for idx, (city_name, _) in enumerate(cities.items()):
    with all_columns[idx]:
        main_placeholders.append(st.empty())


# 4. DINAMIK YANGILANISH TSIKLI
while True:
    now_utc = datetime.datetime.now(pytz.utc)
    unix_time = time.time()
    
    # --- 10 ta Standart uchun aniq ilmiy hisob-kitoblar ---
    tai_time = now_utc + datetime.timedelta(seconds=37) 
    gps_time = now_utc + datetime.timedelta(seconds=18) 
    ut1_time = now_utc - datetime.timedelta(seconds=0.27) 
    tt_time = tai_time + datetime.timedelta(seconds=32.184) 
    gst_time = tai_time - datetime.timedelta(seconds=19) 
    bds_time = now_utc + datetime.timedelta(hours=8)

    # Millisoniyali format funksiyasi
    def fmt(dt):
        return dt.strftime("%H:%M:%S.%f")[:-3]

    # Chap panelni Digital-7 shriftida yangilash
    sb_placeholders[standards[0]].markdown(f"<div class='sidebar-text'>{fmt(now_utc)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[1]].markdown(f"<div class='sidebar-text'>{now_utc.strftime('%H:%M:%S')}.000</div>", unsafe_allow_html=True)
    sb_placeholders[standards[2]].markdown(f"<div class='sidebar-text'>{fmt(tai_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[3]].markdown(f"<div class='sidebar-text'>{str(unix_time)[:10]}.{str(unix_time)[11:14]}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[4]].markdown(f"<div class='sidebar-text'>{fmt(gps_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[5]].markdown(f"<div class='sidebar-text'>{fmt(ut1_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[6]].markdown(f"<div class='sidebar-text'>{fmt(tt_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[7]].markdown(f"<div class='sidebar-text'>{fmt(gst_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[8]].markdown(f"<div class='sidebar-text'>{fmt(now_utc)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[9]].markdown(f"<div class='sidebar-text'>{fmt(bds_time)}</div>", unsafe_allow_html=True)

    # --- Asosiy ekrandagi 8 ta soatni yangilash ---
    for idx, (city_name, tz_string) in enumerate(cities.items()):
        tz = pytz.timezone(tz_string)
        city_time = datetime.datetime.now(tz)
        
        hms = city_time.strftime("%H:%M:%S")
        ms = city_time.strftime(".%f")[:-3]
        date_str = city_time.strftime("%A, %d-%b %Y")
        
        html_card = f"""
        <div class="dashboard-card">
            <div class="city-lbl">{city_name}</div>
            <div class="digital-clock">{hms}<span class="ms-text">{ms}</span></div>
            <div class="date-lbl">{date_str}</div>
        </div>
        """
        main_placeholders[idx].markdown(html_card, unsafe_allow_html=True)
        
    # Silliqlikni ta'minlash uchun kichik uyqu (50 millisoniya)
    time.sleep(0.05)
    

import streamlit as st
import datetime
import time
import pytz

# Sahifa sozlamalari (Keng ekran rejimi va qorong'u mavzu asosi)
st.set_page_config(layout="wide", page_title="Universal Time Network")

# 1. Mukammal CSS UI (Digital Shrift va Neon Panellar)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
    /* Chap panel (Sidebar) uchun uslublar */
    .sidebar-text {
        font-family: monospace;
        font-size: 13px;
        color: #00FF66; /* Standartlar yashil neon */
        background-color: #111111;
        padding: 8px 12px;
        border-radius: 5px;
        margin-bottom: 12px;
        border-left: 3px solid #ff9800;
        box-shadow: inset 0 0 5px rgba(0,255,102,0.1);
    }
    .sidebar-title {
        font-weight: bold;
        color: #ffffff;
        margin-top: 15px;
        font-size: 13px;
        letter-spacing: 1px;
    }

    /* Asosiy ekran (Dashboard) uchun uslublar */
    .dashboard-card {
        background-color: #0a0a0c;
        border: 1px solid #1f1f2e;
        border-radius: 12px;
        padding: 22px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.7);
        transition: transform 0.3s;
    }
    .city-lbl {
        color: #a0aec0;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    .digital-clock {
        font-family: 'Orbitron', sans-serif;
        color: #00E6FF; /* Dashboard neon moviy rang */
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 12px 0;
        text-shadow: 0 0 15px rgba(0, 230, 255, 0.6);
    }
    .ms-text {
        font-size: 26px;
        color: #0088cc; /* Millisoniyalar biroz quyuqroq */
    }
    .date-lbl {
        color: #4a5568;
        font-size: 13px;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. CHAP PANEL (Sidebar) - 10 ta Haqiqiy Vaqt Standarti Menyusi
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
st.write("Dunyoning 8 ta strategik nuqtasidagi jonli vaqt ko'rsatkichlari:")

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


# 4. YUQORI CHASTOTALI YANGILANISH TSIKLI (High-frequency Loop)
while True:
    now_utc = datetime.datetime.now(pytz.utc)
    unix_time = time.time()
    
    # --- 10 ta Standart uchun aniq ilmiy hisob-kitoblar ---
    # TAI UTC dan 37 soniya oldinda
    tai_time = now_utc + datetime.timedelta(seconds=37) 
    # GPS UTC dan 18 soniya oldinda
    gps_time = now_utc + datetime.timedelta(seconds=18) 
    # UT1 Yer aylanishiga qarab UTC dan millisoniyalarga farq qiladi (taxminiy -0.27s)
    ut1_time = now_utc - datetime.timedelta(seconds=0.27) 
    # Terrestrial Time: TT = TAI + 32.184s
    tt_time = tai_time + datetime.timedelta(seconds=32.184) 
    # Galileo vaqti TAI ga juda yaqin (lekin GPS bilan sinxron siljiydi)
    gst_time = tai_time - datetime.timedelta(seconds=19) 
    # Pekin vaqti (BDS BeiDou uchun asosiy vaqt standarti UTC+8)
    bds_time = now_utc + datetime.timedelta(hours=8)

    # Millisoniyalarni (.%f) chiroyli matn formatiga o'tkazish funksiyasi
    def fmt(dt):
        return dt.strftime("%H:%M:%S.%f")[:-3]

    # Chap panelni millisoniyada yangilash
    sb_placeholders[standards[0]].markdown(f"<div class='sidebar-text'>{fmt(now_utc)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[1]].markdown(f"<div class='sidebar-text'>{now_utc.strftime('%H:%M:%S')} (Standart)</div>", unsafe_allow_html=True)
    sb_placeholders[standards[2]].markdown(f"<div class='sidebar-text'>{fmt(tai_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[3]].markdown(f"<div class='sidebar-text'>{str(unix_time)[:14]} s</div>", unsafe_allow_html=True)
    sb_placeholders[standards[4]].markdown(f"<div class='sidebar-text'>{fmt(gps_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[5]].markdown(f"<div class='sidebar-text'>{fmt(ut1_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[6]].markdown(f"<div class='sidebar-text'>{fmt(tt_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[7]].markdown(f"<div class='sidebar-text'>{fmt(gst_time)}</div>", unsafe_allow_html=True)
    sb_placeholders[standards[8]].markdown(f"<div class='sidebar-text'>{fmt(now_utc)} (UTC+0 tied)</div>", unsafe_allow_html=True)
    sb_placeholders[standards[9]].markdown(f"<div class='sidebar-text'>{fmt(bds_time)}</div>", unsafe_allow_html=True)

    # --- Asosiy ekran soatlarini (8 ta davlat) yangilash ---
    for idx, (city_name, tz_string) in enumerate(cities.items()):
        tz = pytz.timezone(tz_string)
        city_time = datetime.datetime.now(tz)
        
        # Soat : Daqiqa : Soniya
        hms = city_time.strftime("%H:%M:%S")
        # Millisoniya (.123)
        ms = city_time.strftime(".%f")[:-3]
        # Hafta kuni va Sana
        date_str = city_time.strftime("%A, %d-%b %Y")
        
        html_card = f"""
        <div class="dashboard-card">
            <div class="city-lbl">{city_name}</div>
            <div class="digital-clock">{hms}<span class="ms-text">{ms}</span></div>
            <div class="date-lbl">{date_str}</div>
        </div>
        """
        main_placeholders[idx].markdown(html_card, unsafe_allow_html=True)
        
    # Tsikl tezligi (50 millisoniya uyqu) - silliq animatsiya kafolati
    time.sleep(0.05)
  

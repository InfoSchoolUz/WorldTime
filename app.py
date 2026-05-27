import streamlit as st
import datetime
import time
import pytz
import base64

# Sahifa sozlamalari
st.set_page_config(layout="wide", page_title="Universal Time Converter")

# 1. Mahalliy font faylini Base64 formatiga o'tkazish funksiyasi
def get_font_base64(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode()

try:
    font_base64 = get_font_base64("digital-7.ttf")
    font_style = f"""
    @font-face {{
        font-family: 'Digital-7';
        src: url(data:font/ttf;charset=utf-8;base64,{font_base64}) format('truetype');
    }}
    """
except FileNotFoundError:
    font_style = ""
    st.warning("⚠️ 'digital-7.ttf' fayli topilmadi! Iltimos, faylni loyiha papkasiga tashlang.")

# 2. CSS UI (Tugmali menyu va raqamli displey dizayni)
st.markdown(
    f"""
    <style>
    {font_style}

    /* Streamlit radio tugmalarini chiroyli bosiladigan tugmali menyuga aylantirish */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {{
        flex-direction: column;
        gap: 10px;
    }}
    
    div[data-testid="stSidebarUserContent"] label[data-testid="stWidgetLabel"] {{
        color: #111111 !important;
        font-weight: bold;
        font-size: 16px;
    }}

    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {{
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        width: 100%;
        transition: all 0.2s ease;
        cursor: pointer;
    }}

    /* Sifatli bosilish effekti va radio nuqtachasini yashirish */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {{
        color: #1f2937 !important;
        font-weight: 600 !important;
    }}
    
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[role="img"] {{
        display: none !important; /* Standart dumaloq nuqtani yashiramiz */
    }}

    /* Tugma tanlangandagi (Active) holat dizayni */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-shadow="true"] {{
        background-color: #ff9800 !important; /* To'q sariq aktiv rang */
        border-color: #e68a00 !important;
    }}
    
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-shadow="true"] div[data-testid="stMarkdownContainer"] {{
        color: #ffffff !important; /* Aktiv tugma matni oq rangda */
    }}

    /* Asosiy ekran (Dashboard) kartalari */
    .dashboard-card {{
        background-color: #050505;
        border: 2px solid #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.9);
    }}
    .city-lbl {{
        color: #a0aec0;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: sans-serif;
    }}
    
    /* DIGITAL-7 SOAT KLASSI */
    .digital-clock {{
        font-family: 'Digital-7', sans-serif; 
        color: #00E6FF; 
        font-size: 65px; 
        letter-spacing: 2px;
        margin: 5px 0;
        text-shadow: 0 0 15px rgba(0, 230, 255, 0.7);
    }}
    .ms-text {{
        font-size: 40px; 
        color: #0088cc; 
    }}
    .date-lbl {{
        color: #4a5568;
        font-size: 13px;
        font-weight: 500;
        font-family: sans-serif;
    }}
    
    .info-box {{
        background-color: #111;
        border-left: 4px solid #ff9800;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 25px;
        color: #ccc;
        font-size: 14px;
        font-family: sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. CHAP PANEL (Sidebar) - Tugmali Menyu (Radio button o'zgartirildi)
st.sidebar.markdown("## 🛰️ Boshqaruv Pulti")

standards_list = [
    "🚀 UTC Standarti", 
    "🌍 GMT Standarti", 
    "⚛️ TAI (Atom Vaqti)", 
    "💻 UNIX Timestamp", 
    "🛰️ GPS Vaqti", 
    "🔭 UT1 (Astronomik)", 
    "🌐 TT (Yer Vaqti)", 
    "🇪🇺 Galileo (GST)", 
    "🇷🇺 GLONASS Vaqti", 
    "🇨🇳 BeiDou (BDS)"
]

selected_standard = st.sidebar.radio("Vaqt standartini tanlang:", standards_list)

standard_descriptions = {
    "🚀 UTC Standarti": "Bosh xalqaro vaqt standarti. Atom soatlari va Yer aylanishi muvozanati.",
    "🌍 GMT Standarti": "Grinvich meridianidagi geografik asosiy vaqt. UTC bilan deyarli bir xil.",
    "⚛️ TAI (Atom Vaqti)": "Sof atom soatlari vaqti. Yer aylanishiga moslashmaydi, UTC'dan 37 soniya oldinda.",
    "💻 UNIX Timestamp": "1970-yildan beri o'tgan jami soniyalar (Barcha shaharlarda kompyuter soniyasi ko'rsatiladi).",
    "🛰️ GPS Vaqti": "Navigatsiya sun'iy yo'ldoshlari vaqti. Kabisa soniyalarisiz, UTC'dan 18 soniya oldinda.",
    "🔭 UT1 (Astronomik)": "Yerning o'z o'qi atrofida haqiqiy aylanishiga asoslangan astronomik vaqt.",
    "🌐 TT (Yer Vaqti)": "Astronomik hisoblar uchun Yer vaqti. TAI standartidan qat'iy 32.184 soniya oldinda.",
    "🇪🇺 Galileo (GST)": "Yevropa Ittifoqi sun'iy yo'ldosh tizimi vaqti. TAI vaqtiga asoslangan.",
    "🇷🇺 GLONASS Vaqti": "Rossiya navigatsiya vaqti. UTC bilan doimiy sinxron holatda yuradi.",
    "🇨🇳 BeiDou (BDS)": "Xitoy navigatsiya vaqti. Pekin standartiga bog'langan bo'lib, UTC'dan 8 soat oldinda."
}

# 4. ASOSIY DASHBOARD
st.title("🎯 Global Real-Time Clock Dashboard")
st.markdown(f"""
<div class="info-box">
    <strong>Faol Tizim:</strong> {selected_standard}<br>
    <span style="color: #888;">{standard_descriptions[selected_standard]}</span>
</div>
""", unsafe_allow_html=True)

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

row1_cols = st.columns(4)
row2_cols = st.columns(4)
all_columns = row1_cols + row2_cols
main_placeholders = []

for idx, _ in enumerate(cities.items()):
    with all_columns[idx]:
        main_placeholders.append(st.empty())

# 5. YANGILANISH TSIKLI
while True:
    now_utc = datetime.datetime.now(pytz.utc)
    unix_base = time.time()
    
    if "UTC" in selected_standard:
        base_time = now_utc
    elif "GMT" in selected_standard:
        base_time = now_utc
    elif "TAI" in selected_standard:
        base_time = now_utc + datetime.timedelta(seconds=37)
    elif "GPS" in selected_standard:
        base_time = now_utc + datetime.timedelta(seconds=18)
    elif "UT1" in selected_standard:
        base_time = now_utc - datetime.timedelta(seconds=0.27)
    elif "TT" in selected_standard:
        base_time = now_utc + datetime.timedelta(seconds=37 + 32.184)
    elif "Galileo" in selected_standard:
        base_time = now_utc + datetime.timedelta(seconds=37 - 19)
    elif "GLONASS" in selected_standard:
        base_time = now_utc
    elif "BeiDou" in selected_standard:
        base_time = now_utc + datetime.timedelta(hours=8)
    elif "UNIX" in selected_standard:
        base_time = None

    for idx, (city_name, tz_string) in enumerate(cities.items()):
        tz = pytz.timezone(tz_string)
        city_local = datetime.datetime.now(tz)
        utc_offset = city_local.utcoffset() 
        
        if "UNIX" in selected_standard:
            hms = str(int(unix_base))[-6:]
            ms = f".{str(unix_base).split('.')[1][:3]}"
            date_str = "Unix Epoch Seconds"
        else:
            final_city_time = base_time + utc_offset
            hms = final_city_time.strftime("%H:%M:%S")
            ms = final_city_time.strftime(".%f")[:-3]
            date_str = city_local.strftime("%A, %d-%b %Y")

        html_card = f"""
        <div class="dashboard-card">
            <div class="city-lbl">{city_name}</div>
            <div class="digital-clock">{hms}<span class="ms-text">{ms}</span></div>
            <div class="date-lbl">{date_str}</div>
        </div>
        """
        main_placeholders[idx].markdown(html_card, unsafe_allow_html=True)
        
    time.sleep(0.05)

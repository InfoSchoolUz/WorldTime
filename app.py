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

# 2. CSS UI (Raqamli displey dizayni)
st.markdown(
    f"""
    <style>
    {font_style}

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
        color: #00E6FF; /* Neon Moviy */
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
    
    /* Tanlangan standart haqida ma'lumot qutisi */
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

# 3. CHAP PANEL (Sidebar) - Radio Menyu variantlari
st.sidebar.markdown("## 🛰️ Vaqt Standartini Tanlang")
st.sidebar.markdown("Dashboarddagi barcha soatlar tanlangan standart vaqtiga moslab hisoblanadi.")

standards_list = [
    "UTC (Coordinated Universal Time)", 
    "GMT (Greenwich Mean Time)", 
    "TAI (International Atomic Time)", 
    "UNIX Timestamp", 
    "GPS Time (Global Positioning)", 
    "UT1 (Astronomical Time)", 
    "TT (Terrestrial Time)", 
    "Galileo Time (GST)", 
    "GLONASS Time", 
    "BeiDou Time (BDS)"
]

# Chap paneldagi interaktiv menyu
selected_standard = st.sidebar.radio("Mavjud standartlar:", standards_list)

# Har bir standart uchun qisqacha izohlar lug'ati
standard_descriptions = {
    "UTC (Coordinated Universal Time)": "Bosh xalqaro vaqt standarti. Atom soatlari va Yer aylanishi muvozanati.",
    "GMT (Greenwich Mean Time)": "Grinvich meridianidagi geografik asosiy vaqt. UTC bilan deyarli bir xil.",
    "TAI (International Atomic Time)": "Sof atom soatlari vaqti. Yer aylanishiga moslashmaydi, UTC'dan 37 soniya oldinda.",
    "UNIX Timestamp": "1970-yildan beri o'tgan jami soniyalar (Barcha shaharlarda kompyuter soniyasi ko'rsatiladi).",
    "GPS Time (Global Positioning)": "Navigatsiya sun'iy yo'ldoshlari vaqti. Kabisa soniyalarisiz, UTC'dan 18 soniya oldinda.",
    "UT1 (Astronomical Time)": "Yerning o'z o'qi atrofida haqiqiy aylanishiga asoslangan astronomik vaqt.",
    "TT (Terrestrial Time)": "Astronomik hisoblar uchun Yer vaqti. TAI standartidan qat'iy 32.184 soniya oldinda.",
    "Galileo Time (GST)": "Yevropa Ittifoqi sun'iy yo'ldosh tizimi vaqti. TAI asosida ishlaydi.",
    "GLONASS Time": "Rossiya navigatsiya vaqti. UTC bilan doimiy sinxron holatda yuradi.",
    "BeiDou Time (BDS)": "Xitoy navigatsiya vaqti. Pekin standartiga bog'langan bo'lib, UTC'dan 8 soat oldinda."
}

# 4. ASOSIY DASHBOARD - Sarlavha va Izoh
st.title("🎯 Global Real-Time Clock Dashboard")
st.markdown(f"""
<div class="info-box">
    <strong>Joriy rejim:</strong> {selected_standard}<br>
    <span style="color: #888;">{standard_descriptions[selected_standard]}</span>
</div>
""", unsafe_allow_html=True)

# 8 ta davlat/shahar ro'yxati va ularning standart UTC offset farqlari (soat hisobida)
# Chunki foydalanuvchi standartni o'zgartirganda, shaharlar o'sha yangi asosga nisbatan o'z farqini saqlab qolishi kerak.
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

# 4x2 simmetrik kataklar yaratish
row1_cols = st.columns(4)
row2_cols = st.columns(4)
all_columns = row1_cols + row2_cols
main_placeholders = []

for idx, _ in enumerate(cities.items()):
    with all_columns[idx]:
        main_placeholders.append(st.empty())

# 5. YUQORI CHASTOTALI DINAMIK HISOB-KITOB TSIKLI
while True:
    now_utc = datetime.datetime.now(pytz.utc)
    unix_base = time.time()
    
    # Tanlangan menyuga qarab asosiy "tayanch" vaqtni aniqlaymiz (UTCga nisbatan farqi)
    if selected_standard == "UTC (Coordinated Universal Time)":
        base_time = now_utc
    elif selected_standard == "GMT (Greenwich Mean Time)":
        base_time = now_utc # Millisoniyasiz standart rejim deb qaraladi
    elif selected_standard == "TAI (International Atomic Time)":
        base_time = now_utc + datetime.timedelta(seconds=37)
    elif selected_standard == "GPS Time (Global Positioning)":
        base_time = now_utc + datetime.timedelta(seconds=18)
    elif selected_standard == "UT1 (Astronomical Time)":
        base_time = now_utc - datetime.timedelta(seconds=0.27)
    elif selected_standard == "TT (Terrestrial Time)":
        base_time = now_utc + datetime.timedelta(seconds=37 + 32.184)
    elif selected_standard == "Galileo Time (GST)":
        base_time = now_utc + datetime.timedelta(seconds=37 - 19)
    elif selected_standard == "GLONASS Time":
        base_time = now_utc
    elif selected_standard == "BeiDou Time (BDS)":
        base_time = now_utc + datetime.timedelta(hours=8)
    elif selected_standard == "UNIX Timestamp":
        base_time = None # Maxsus rejim

    # Shaharlarni yangilash
    for idx, (city_name, tz_string) in enumerate(cities.items()):
        tz = pytz.timezone(tz_string)
        
        # Shaharning UTCga nisbatan hozirgi farqini olamiz (yozgi/qishki vaqtni hisobga olgan holda)
        city_local = datetime.datetime.now(tz)
        utc_offset = city_local.utcoffset() 
        
        if selected_standard == "UNIX Timestamp":
            # Unix vaqtida hamma joyda bir xil soniya aylanadi
            hms = str(int(unix_base))[-6:] # Oxirgi 6 ta raqami chiroyli sig'ishi uchun
            ms = f".{str(unix_base).split('.')[1][:3]}"
            date_str = "Unix Soniya ko'rsatkichi"
        else:
            # Tanlangan tayanch vaqtga shaharning shaxsiy vaqt farqini qo'shamiz
            final_city_time = base_time + utc_offset
            
            hms = final_city_time.strftime("%H:%M:%S")
            ms = final_city_time.strftime(".%f")[:-3]
            date_str = city_local.strftime("%A, %d-%b %Y") # Kalendar o'zgarmaydi

        html_card = f"""
        <div class="dashboard-card">
            <div class="city-lbl">{city_name}</div>
            <div class="digital-clock">{hms}<span class="ms-text">{ms}</span></div>
            <div class="date-lbl">{date_str}</div>
        </div>
        """
        main_placeholders[idx].markdown(html_card, unsafe_allow_html=True)
        
    time.sleep(0.05)
    

import streamlit as st
import os
import base64
import urllib.parse

st.set_page_config(page_title="Wadi Degla - Performance Analysis", layout="wide")

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ==========================
# 1. قاعدة بيانات اللاعبين (روابط يوتيوب)
# ==========================
# هنا بتكتب اسم اللاعب ورابط الفيديو (غير المدرج) الخاص به
squad_data = {
    "attackers": {
        "Ahmed Farouk": "https://www.youtube.com/watch?v=XXXXXXXXXXX",
        "Ahmed": "https://youtu.be/YYYYYYYYYYY"
    },
    "midfielders": {
        "Mohamed": "https://youtu.be/ZZZZZZZZZZZ"
    },
    "defenders": {
        "Ali": "https://youtu.be/WWWWWWWWWWW"
    },
    "bench": {
        "Hassan": "https://youtu.be/VVVVVVVVVVV"
    }
}

# ==========================
# 2. تصميم الـ Dashboard الاحترافي (CSS)
# ==========================
custom_css = """
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #121212; }
    
    .navbar {
        background-color: #1e1e1e;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #333;
        margin-top: -60px;
        margin-bottom: 20px;
    }
    .navbar-title { color: #ffffff; font-family: sans-serif; font-size: 18px; font-weight: 600; }
    .logo-img { height: 35px; object-fit: contain; }
    
    .dashboard-card {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #2a2a2a;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .section-title {
        color: #a0a0a0; font-size: 14px; text-transform: uppercase;
        letter-spacing: 1.5px; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;
    }
    
    div[data-testid="stVideo"] { border-radius: 4px; border: 1px solid #333; background-color: #000; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
os.makedirs("assets", exist_ok=True)

# ==========================
# 3. بناء الـ Navbar
# ==========================
logo1_html = f'<img src="data:image/png;base64,{get_image_base64("assets/logo1.png")}" class="logo-img">' if os.path.exists("assets/logo1.png") else ''
logo2_html = f'<img src="data:image/png;base64,{get_image_base64("assets/logo2.png")}" class="logo-img">' if os.path.exists("assets/logo2.png") else ''

navbar_html = f"""
<div class="navbar">
    <div>{logo1_html}</div>
    <div class="navbar-title">WADI DEGLA FC - PERFORMANCE ANALYSIS</div>
    <div>{logo2_html}</div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# ==========================
# 4. تخطيط الشاشة وتفعيل مشغل الفيديو
# ==========================
col_video, col_squad = st.columns([2, 3]) 

# ----- قراءة الرابط عند الضغط -----
if "player" in st.query_params and "pos" in st.query_params:
    player_name = st.query_params["player"]
    pos = st.query_params["pos"]
    if pos in squad_data and player_name in squad_data[pos]:
        st.session_state.current_video = squad_data[pos][player_name]
        st.session_state.current_name = player_name
elif 'current_video' not in st.session_state:
    st.session_state.current_video = None
    st.session_state.current_name = None

# ----- عمود الفيديو -----
with col_video:
    st.markdown('<div class="dashboard-card"><div class="section-title">VIDEO PLAYER</div>', unsafe_allow_html=True)
    
    if st.session_state.current_video:
        # ستريملت يدعم تشغيل روابط يوتيوب تلقائياً
        st.video(st.session_state.current_video)
        st.markdown(f"<p style='color: #4CAF50; font-size:14px; margin-top:10px;'>▶ Playing: {st.session_state.current_name}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #666; text-align:center; padding: 50px 0;'>Select a player to load video</p>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# 5. عمود التشكيل ورسم الأيقونات
# ==========================
def render_squad_line(position_key, title):
    players = squad_data.get(position_key, {})
    images_dir = os.path.join("images", position_key)
    os.makedirs(images_dir, exist_ok=True)
    
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    
    if not players:
        st.markdown(f"<p style='color: #444; font-size:12px;'>No players found in {title}</p>", unsafe_allow_html=True)
        return
        
    cols = st.columns(len(players))
    for index, (player_name, youtube_url) in enumerate(players.items()):
        img_jpg = os.path.join(images_dir, f"{player_name}.jpg")
        img_png = os.path.join(images_dir, f"{player_name}.png")
        
        img_base64 = get_image_base64(img_jpg) if os.path.exists(img_jpg) else (get_image_base64(img_png) if os.path.exists(img_png) else None)
            
        with cols[index]:
            # تجهيز الرابط التفاعلي باسم اللاعب ومركزه
            safe_player_name = urllib.parse.quote(player_name)
            href_url = f"/?player={safe_player_name}&pos={position_key}"
            
            img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #444; object-fit: cover;">' if img_base64 else f'<div style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #444; background-color: #222;"></div>'
            
            html_code = f"""
            <a href="{href_url}" target="_self" style="text-decoration: none; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom:15px;">
                {img_html}
                <span style="color: #ccc; font-size: 11px; margin-top: 5px; text-transform: uppercase;">{player_name}</span>
            </a>
            """
            st.markdown(html_code, unsafe_allow_html=True)

with col_squad:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_squad_line("attackers", "ATTACKERS")
    render_squad_line("midfielders", "MIDFIELDERS")
    render_squad_line("defenders", "DEFENDERS")
    render_squad_line("bench", "BENCH")
    st.markdown('</div>', unsafe_allow_html=True)

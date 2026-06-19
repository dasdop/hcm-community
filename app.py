import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai  # <- 대문자 Google을 소문자 google로 수정 완료!

# --- 제미니 API 설정 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

# ==========================================
# Grab Style Custom CSS
# ==========================================
def local_css():
    st.markdown("""
        <style>
        .stApp { background-color: #F7F9FC; }
        .main-header {
            background-color: #00B14F;
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-header h1 { color: white !important; font-weight: 800; }
        .section-title {
            color: #1C1C1C; font-size: 1.5rem; font-weight: 700;
            margin-top: 2rem; margin-bottom: 1rem;
            border-left: 5px solid #00B14F; padding-left: 10px;
        }
        .grab-card {
            background-color: white; padding: 1.5rem; border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="HCM Grab Community", page_icon="🇻🇳", layout="wide")
local_css()

# 메인 헤더
st.markdown("""
    <div class="main-header">
        <h1>🇻🇳 호치민 한인 통합 커뮤니티</h1>
        <p>Grab처럼 편리한 정보와 똑똑한 제미니 AI 가이드를 만나보세요.</p>
    </div>
""", unsafe_allow_html=True)

# 상단 탭 구성
tab1, tab2, tab3 = st.tabs(["🗺️ 주변 추천 시설", "🤖 AI 호치민 가이드", "💬 교민 광장"])

# ==========================================
# 탭 1: 추천 시설
# ==========================================
with tab1:
    st.markdown('<div class="section-title">🗺️ 주변 추천 한인 시설</div>', unsafe_allow_html=True)
    facility_data = [
        {"name": "명동칼국수", "category": "식당", "area": "7군 푸미흥", "address": "Sky Garden", "lat": 10.7314, "lon": 106.7055, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "강남 바베큐", "category": "식당", "area": "7군 푸미흥", "address": "Hung Vuong", "lat": 10.7290, "lon": 106.7060, "rating": "⭐⭐⭐⭐"},
        {"name": "서울 헤어살롱", "category": "미용실", "area": "7군 푸미흥", "address": "Mi Khanh", "lat": 10.7305, "lon": 106.7040, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "스타 어학원", "category": "학원", "area": "7군 푸미흥", "address": "Happy Valley", "lat": 10.7285, "lon": 106.7020, "rating": "⭐⭐⭐⭐"},
        {"name": "타오디엔 K-식당", "category": "식당", "area": "2군 타오디엔", "address": "Thao Dien", "lat": 10.8040, "lon": 106.7380, "rating": "⭐⭐⭐⭐⭐"}
    ]
    df = pd.DataFrame(facility_data)
    
    search_area = st.multiselect("지역 선택", df['area'].unique(), default=df['area'].unique())
    search_category = st.multiselect("카테고리 선택", df['category'].unique(), default=df['category'].unique())
    filtered_df = df[(df['area'].isin(search_area)) & (df['category'].isin(search_category))]
    
    st.map(filtered_df, zoom=12)
    
    cols = st.columns(3)
    for i, row in filtered_df.iterrows():
        with cols[i % 3]:
            st.markdown(f"""
                <div class="grab-card">
                    <h4>{row['name']}</h4>
                    <p><b>{row['category']}</b> | {row['area']}</p>
                    <p>📍 {row['address']}</p>
                    <p>⭐ {row['rating']}</p>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 탭 2: 제미니 AI 호치민 가이드
# ==========================================
with tab2:
    st.markdown('<div class="section-title">🤖 제미니 AI 챗봇 가이드</div>', unsafe_allow_html=True)
    
    if model is None:
        st.warning("⚠️ 제미니 API 키가 설정되지 않았습니다. 스트림릿 클라우드의 Secrets에 키를 등록해 주세요.")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        user_question = st.text_input("AI에게 질문하기:", placeholder="예: 푸미흥 근처 맛집이나 가볼 만한 곳 추천해줘")
        
        if st.button("질문 보내기"):
            if user_question:
                with st.spinner("제미니가 생각 중입니다..."):
                    try:
                        prompt = f"너는 베트남 호치민 한인 커뮤니티의 친절한 가이드야. 한국인 교민이나 여행객의 질문에 친절하고 상세하게 답변해줘. 질문: {user_question}"
                        response = model.generate_content(prompt)
                        st.session_state.chat_history.append(("User", user_question))
                        st.session_state.chat_history.append(("AI", response.text))
                    except Exception as e:
                        st.error(f"에러가 발생했습니다: {e}")
                        
        for role, text in reversed(st.session_state.chat_history):
            if role == "User":
                st.markdown(f"**👤 나:** {text}")
            else:
                st.markdown(f"**🤖 제미니:** {text}")
                st.markdown("---")

# ==========================================
# 탭 3: 교민 광장
# ==========================================
with tab3:
    st.markdown('<div class="section-title">💬 실시간 교민 광장</div>', unsafe_allow_html=True)
    
    if 'posts' not in st.session_state:
        st.session_state.posts = [
            {"user": "호치민라이프", "text": "푸미흥 스카이가든 근처 맛집 추천해주실 분 계신가요?", "time": "5분 전"},
            {"user": "타오디엔주민", "text": "오늘 그랩푸드 배달이 평소보다 많이 늦네요. 참고하세요!", "time": "12분 전"}
        ]

    with st.container():
        c1, c2 = st.columns([4, 1])
        with c1:
            new_post_text = st.text_input("지금 어떤 정보가 필요하신가요?", placeholder=" Grab food 추천, 날씨, 질문 등...", key="community_input")
        with c2:
            if st.button("등록", use_container_width=True, key="community_btn"):
                if new_post_text:
                    new_post = {"user": "익명교민", "text": new_post_text, "time": "방금 전"}
                    st.session_state.posts.insert(0, new_post)
                    st.rerun()

    for post in st.session_state.posts:
        st.markdown(f"""
            <div class="grab-card" style="padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #00B14F;">
                <b>👤 {post['user']}</b> <span style="color: #999; font-size: 0.8rem;">({post['time']})</span>
                <p style="margin-top: 0.5rem; margin-bottom: 0;">{post['text']}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #BBB;">
        © 2026 HCM Korean Grab Style Community. 🇻🇳
    </div>
""", unsafe_allow_html=True)

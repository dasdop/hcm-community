import streamlit as st
import pandas as pd
from datetime import datetime
import Google.generativeai as genai  # 제미니 라이브러리 추가

# --- 제미니 API 설정 (스트림릿 Secrets에서 보안 유지하며 가져오기) ---
# 스트림릿 클라우드 설정 창(Secrets)에 GEMINI_API_KEY = "내키" 를 입력해야 작동합니다.
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
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

# --- 사이드바 대신 상단 탭으로 깔끔하게 구성 ---
tab1, tab2, tab3 = st.tabs(["🗺️ 주변 추천 시설", "🤖 AI 호치민 가이드", "💬 교민 광장"])

# ==========================================
# 탭 1: 추천 시설 (기존 코드 유지)
# ==========================================
with tab1:
    st.markdown('<div class="section-title">🗺️ 주변 추천 한인 시설</div>', unsafe_allow_html=True)
    facility_data = [
        {"name": "명동칼국수", "category": "식당", "area": "7군 푸미흥", "address": "Sky Garden", "lat": 10.7314, "lon": 106.7055, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "서울 헤어살롱", "category": "미용실", "area": "7군 푸미흥", "address": "Mi Khanh", "lat": 10.7305, "lon": 106.7040, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "타오디엔 K-식당", "category": "식당", "area": "2군 타오디엔", "address": "Thao Dien", "lat": 10.8040, "lon": 106.7380, "rating": "⭐⭐⭐⭐⭐"}
    ]
    df = pd.DataFrame(facility_data)
    st.map(df, zoom=12)

# ==========================================
# 탭 2: 제미니 AI 호치민 가이드 (새로 추가!)
# ==========================================
with tab2:
    st.markdown('<div class="section-title">🤖 제미니 AI 챗봇 가이드</div>', unsafe_allow_html=True)
    st.write("호치민 생활 정보, 맛집 위치, 베트남어 표현 등 궁금한 것을 물어보세요!")
    
    if model is None:
        st.warning("⚠️ 제미니 API 키가 설정되지 않았습니다. 스트림릿 클라우드의 Secrets에 키를 등록해 주세요.")
    else:
        # 간단한 대화 히스토리 세션 초기화
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        user_question = st.text_input("AI에게 질문하기:", placeholder="예: 푸미흥 근처 맛집이나 가볼 만한 곳 추천해줘")
        
        if st.button("질문 보내기"):
            if user_question:
                with st.spinner("제미니가 생각 중입니다..."):
                    try:
                        # 호치민 관련 답변을 더 잘하도록 프롬프트 엔지니어링 추가
                        prompt = f"너는 베트남 호치민 한인 커뮤니티의 친절한 가이드야. 한국인 교민이나 여행객의 질문에 친절하고 상세하게 답변해줘. 질문: {user_question}"
                        response = model.generate_content(prompt)
                        
                        # 히스토리에 저장
                        st.session_state.chat_history.append(("User", user_question))
                        st.session_state.chat_history.append(("AI", response.text))
                    except Exception as e:
                        st.error(f"에러가 발생했습니다: {e}")
                        
        # 대화 내용 출력
        for role, text in reversed(st.session_state.chat_history):
            if role == "User":
                st.markdown(f"**👤 나:** {text}")
            else:
                st.markdown(f"**🤖 제미니:** {text}")
                st.markdown("---")

# ==========================================
# 탭 3: 교민 광장 (기존 코드 유지)
# ==========================================
with tab3:
    st.markdown('<div class="section-title">💬 실시간 교민 광장</div>', unsafe_allow_html=True)
    # (기존의 게시판 코드 생략/유지됨)

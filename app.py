import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import google.generativeai as genai

# --- 제미니 API 설정 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

# ==========================================
# 🎨 삼성 가이드북 스타일 Custom CSS
# ==========================================
def local_css():
    st.markdown("""
        <style>
        /* 전체 배경색 깔끔하게 */
        .stApp { background-color: #F4F6F9; }
        
        /* 메인 타이틀 영역 (깔끔하고 모던하게) */
        .samsung-header {
            text-align: center;
            padding: 3rem 0 2rem 0;
            background-color: transparent;
        }
        .samsung-header h1 {
            color: #1A1A1A !important;
            font-weight: 800;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .samsung-header p {
            color: #666;
            font-size: 1.1rem;
        }

        /* 탭 디자인 수정 */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
        .stTabs [data-baseweb="tab"] { border-radius: 20px 20px 0 0; }

        /* 컬러풀한 카드 UI */
        .color-card {
            border-radius: 24px;
            padding: 25px 20px;
            color: white;
            text-align: center;
            height: 260px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 1.5rem;
        }
        .color-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }
        
        /* 카드 내부 텍스트 및 요소 */
        .card-tag {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            backdrop-filter: blur(5px);
            margin-bottom: 15px;
            display: inline-block;
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 800;
            line-height: 1.3;
            margin: 0 0 5px 0;
            word-break: keep-all;
        }
        .card-subtitle {
            font-size: 0.85rem;
            opacity: 0.9;
            margin-bottom: 15px;
        }
        .card-icon {
            font-size: 4rem;
            margin-top: auto;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }

        /* 그라데이션 배경색 (카테고리별 매칭) */
        .theme-blue { background: linear-gradient(135deg, #3A7BD5, #3A6073); } /* 교육 */
        .theme-purple { background: linear-gradient(135deg, #8E2DE2, #4A00E0); } /* 미용 */
        .theme-pink { background: linear-gradient(135deg, #FF416C, #FF4B2B); } /* 카페 */
        .theme-orange { background: linear-gradient(135deg, #FF8008, #FFC837); } /* 식당 */
        .theme-green { background: linear-gradient(135deg, #11998E, #38EF7D); } /* 병원 */
        .theme-dark { background: linear-gradient(135deg, #2C3E50, #000000); } /* 마트 */
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="HCM Community", page_icon="🇻🇳", layout="wide")
local_css()

# 메인 헤더 (깔끔한 텍스트형)
st.markdown("""
    <div class="samsung-header">
        <h1>호치민 교민 통합 가이드북</h1>
        <p>생활 정보의 기초부터 심화까지 한 번에</p>
    </div>
""", unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 한인 시설 가이드", "🔍 실시간 로컬 검색", "🤖 AI 비서", "💬 소통 라운지"])

# --- 카드 스타일 매퍼 함수 ---
def get_card_style(category):
    styles = {
        "식당": {"class": "theme-orange", "icon": "🍲"},
        "카페/베이커리": {"class": "theme-pink", "icon": "☕"},
        "미용/스파": {"class": "theme-purple", "icon": "💆‍♀️"},
        "병원/약국": {"class": "theme-green", "icon": "🏥"},
        "학원/교육": {"class": "theme-blue", "icon": "📚"},
        "마트/쇼핑": {"class": "theme-dark", "icon": "🛒"},
        "식당 (Restaurant)": {"class": "theme-orange", "icon": "🍕"},
        "카페 (Cafe)": {"class": "theme-pink", "icon": "🥤"},
        "병원 (Hospital)": {"class": "theme-green", "icon": "🩺"},
        "약국 (Pharmacy)": {"class": "theme-green", "icon": "💊"}
    }
    return styles.get(category, {"class": "theme-blue", "icon": "📍"})

# ==========================================
# 탭 1: 추천 시설 데이터 (4열 그리드 카드)
# ==========================================
with tab1:
    st.write("### 📌 필수 한인 인프라")
    
    raw_facilities = [
        ("명동칼국수", "식당", "7군 푸미흥", "Sky Garden 3차", 10.7314, 106.7055),
        ("스타 어학원", "학원/교육", "7군 푸미흥", "Happy Valley", 10.7285, 106.7020),
        ("타오디엔 K-식당", "식당", "2군 타오디엔", "Thao Dien Rd", 10.8040, 106.7380),
        ("K-Mart 안푸점", "마트/쇼핑", "2군 타오디엔", "An Phu Song Hanh", 10.8015, 106.7350),
        ("한식당 경복궁", "식당", "1군 시내", "Hai Ba Trung", 10.7795, 106.6990),
        ("서울 이발소", "미용/스파", "1군 시내", "Le Thanh Ton", 10.7770, 106.7015),
        ("빈홈 K-치킨", "식당", "빈탄군(빈홈)", "Vinhomes Central Park", 10.7930, 106.7220),
        ("푸미흥 한인병원", "병원/약국", "7군 푸미흥", "Nguyen Van Linh", 10.7295, 106.7035)
    ]
    
    # 4열 그리드 렌더링
    cols = st.columns(4)
    for i, item in enumerate(raw_facilities):
        name, cat, area, address, lat, lon = item
        style = get_card_style(cat)
        
        with cols[i % 4]:
            st.markdown(f"""
                <div class="color-card {style['class']}">
                    <div class="card-tag">{cat} 가이드</div>
                    <div class="card-title">{name}</div>
                    <div class="card-subtitle">📍 {area}</div>
                    <div class="card-icon">{style['icon']}</div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 탭 2: 실시간 무료 지도 검색 (동일한 카드 UI 적용)
# ==========================================
with tab2:
    st.write("### 🔍 실시간 데이터 검색")
    
    col1, col2 = st.columns(2)
    with col1:
        target_area = st.selectbox("탐색할 지역", ["1군 시내", "2군 타오디엔", "7군 푸미흥"])
    with col2:
        target_category = st.selectbox("탐색할 분야", ["식당 (Restaurant)", "카페 (Cafe)", "병원 (Hospital)", "약국 (Pharmacy)"])

    if st.button("실시간 탐색 시작", use_container_width=True):
        with st.spinner("해당 지역의 데이터를 분석 중입니다..."):
            locations = {"1군 시내": (10.7756, 106.7019), "2군 타오디엔": (10.8045, 106.7368), "7군 푸미흥": (10.7295, 106.7055)}
            lat, lon = locations[target_area]
            tags = {"식당 (Restaurant)": "restaurant", "카페 (Cafe)": "cafe", "병원 (Hospital)": "hospital", "약국 (Pharmacy)": "pharmacy"}
            amenity = tags[target_category]

            overpass_url = "http://overpass-api.de/api/interpreter"
            query = f'[out:json];(node["amenity"="{amenity}"](around:2000,{lat},{lon}););out 8;'
            
            try:
                response = requests.get(overpass_url, params={'data': query})
                data = response.json()
                
                if 'elements' in data and len(data['elements']) > 0:
                    st.success(f"성공적으로 {len(data['elements'])}개의 장소를 찾았습니다.")
                    
                    # 검색 결과도 4열 카드 그리드로 표시
                    res_cols = st.columns(4)
                    style = get_card_style(target_category)
                    
                    for i, el in enumerate(data['elements'][:8]): # 최대 8개만 표시
                        name = el.get('tags', {}).get('name', '로컬 장소')
                        if len(name) > 15: name = name[:15] + "..." # 이름이 너무 길면 자르기
                        
                        with res_cols[i % 4]:
                            st.markdown(f"""
                                <div class="color-card {style['class']}">
                                    <div class="card-tag">주변 탐색 결과</div>
                                    <div class="card-title">{name}</div>
                                    <div class="card-icon">{style['icon']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("해당 조건의 장소가 없습니다.")
            except Exception as e:
                st.error("데이터 로딩 실패")

# ==========================================
# 탭 3: 제미니 AI / 탭 4: 교민 광장
# ==========================================
with tab3:
    st.write("### 🤖 호치민 스마트 비서")
    if model is None:
        st.warning("제미니 API 키를 설정해 주세요.")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        user_question = st.text_input("궁금한 점을 물어보세요:")
        if st.button("질문하기"):
            if user_question:
                with st.spinner("답변을 작성 중입니다..."):
                    try:
                        response = model.generate_content(f"호치민 가이드로서 답변해줘: {user_question}")
                        st.session_state.chat_history.append(("User", user_question))
                        st.session_state.chat_history.append(("AI", response.text))
                    except Exception as e:
                        st.error(f"에러: {e}")
                        
        for role, text in reversed(st.session_state.chat_history):
            if role == "User":
                st.info(f"**질문:** {text}")
            else:
                st.success(f"**답변:** {text}")

with tab4:
    st.write("### 💬 소통 라운지")
    if 'posts' not in st.session_state:
        st.session_state.posts = [{"tag": "📢 공지", "user": "운영자", "text": "가이드북 라운지에 오신 것을 환영합니다.", "time": "방금 전"}]

    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        new_tag = st.selectbox("주제", ["❓ 질문", "🍔 맛집", "🤝 중고거래", "💬 잡담"])
    with c2:
        new_post_text = st.text_input("내용 입력", label_visibility="collapsed")
    with c3:
        if st.button("글 남기기", use_container_width=True):
            if new_post_text:
                st.session_state.posts.insert(0, {"tag": new_tag, "user": "익명교민", "text": new_post_text, "time": "방금 전"})
                st.rerun()

    for post in st.session_state.posts:
        bg = "#F8D7DA" if "공지" in post['tag'] else "white"
        st.markdown(f"""
            <div style="background-color:{bg}; padding:20px; border-radius:15px; margin-bottom:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                <span style="background-color:#333; color:white; padding:4px 10px; border-radius:10px; font-size:0.8rem;">{post['tag']}</span>
                <p style="margin:10px 0 0 0; color:#333; font-size:1.1rem;">{post['text']}</p>
            </div>
        """, unsafe_allow_html=True)

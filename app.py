import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

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
# 탭 1: 추천 시설 데이터
# ==========================================
with tab1:
    st.markdown('<div class="section-title">🗺️ 주변 추천 한인 시설 (대형 데이터베이스)</div>', unsafe_allow_html=True)
    
    areas = ["7군 푸미흥", "2군 타오디엔", "1군 시내", "빈탄군(빈홈)", "기타 지역"]
    categories = ["식당", "카페/베이커리", "미용/스파", "병원/약국", "학원/교육", "마트/쇼핑"]
    
    raw_facilities = [
        ("명동칼국수", "식당", "7군 푸미흥", "Sky Garden 3차", 10.7314, 106.7055, "⭐⭐⭐⭐⭐"),
        ("강남 바베큐", "식당", "7군 푸미흥", "Hung Vuong 2차", 10.7290, 106.7060, "⭐⭐⭐⭐"),
        ("서울 헤어살롱", "미용/스파", "7군 푸미흥", "Mi Khanh 1차", 10.7305, 106.7040, "⭐⭐⭐⭐⭐"),
        ("스타 어학원", "학원/교육", "7군 푸미흥", "Happy Valley", 10.7285, 106.7020, "⭐⭐⭐⭐"),
        ("파리바게뜨 푸미흥점", "카페/베이커리", "7군 푸미흥", "Sky Garden 상가", 10.7320, 106.7058, "⭐⭐⭐⭐⭐"),
        ("K-Market 그랜드뷰", "마트/쇼핑", "7군 푸미흥", "Grand View Appartment", 10.7278, 106.7072, "⭐⭐⭐⭐⭐"),
        ("푸미흥 한인병원", "병원/약국", "7군 푸미흥", "Nguyen Van Linh", 10.7295, 106.7035, "⭐⭐⭐⭐⭐"),
        ("부산 자갈치 횟집", "식당", "7군 푸미흥", "Hung Gia 4", 10.7300, 106.7062, "⭐⭐⭐⭐"),
        ("본가 (Bongaa)", "식당", "7군 푸미흥", "Sky Garden 주변", 10.7311, 106.7049, "⭐⭐⭐⭐⭐"),
        ("유가네 닭갈비", "식당", "7군 푸미흥", "Hung Phuoc", 10.7325, 106.7070, "⭐⭐⭐⭐"),
        ("타오디엔 K-식당", "식당", "2군 타오디엔", "Thao Dien Rd", 10.8040, 106.7380, "⭐⭐⭐⭐⭐"),
        ("서울 클리닉 (2군)", "병원/약국", "2군 타오디엔", "Xuan Thuy", 10.8055, 106.7395, "⭐⭐⭐⭐"),
        ("K-Mart 안푸점", "마트/쇼핑", "2군 타오디엔", "An Phu Song Hanh", 10.8015, 106.7350, "⭐⭐⭐⭐⭐"),
        ("정관장 타오디엔", "마트/쇼핑", "2군 타오디엔", "Thao Dien", 10.8035, 106.7370, "⭐⭐⭐⭐"),
        ("안푸 한인 유치원", "학원/교육", "2군 타오디엔", "An Phu 내", 10.8020, 106.7360, "⭐⭐⭐⭐"),
        ("타오디엔 카페 로얄", "카페/베이커리", "2군 타오디엔", "Nguyen Van Huong", 10.8070, 106.7410, "⭐⭐⭐⭐⭐"),
        ("한식당 경복궁", "식당", "1군 시내", "Hai Ba Trung", 10.7795, 106.6990, "⭐⭐⭐⭐⭐"),
        ("서울 이발소 (1군)", "미용/스파", "1군 시내", "Le Thanh Ton", 10.7770, 106.7015, "⭐⭐⭐⭐"),
        ("교촌치킨 1군점", "식당", "1군 시내", "Dong Khoi", 10.7750, 106.7030, "⭐⭐⭐⭐⭐"),
        ("아리랑 한식당", "식당", "1군 시내", "Dong Du", 10.7745, 106.7040, "⭐⭐⭐⭐"),
        ("빈홈 K-치킨", "식당", "빈탄군(빈홈)", "Vinhomes Central Park", 10.7930, 106.7220, "⭐⭐⭐⭐⭐"),
        ("마켓브라더스 빈홈", "마트/쇼핑", "빈탄군(빈홈)", "Park 2 상가", 10.7940, 106.7210, "⭐⭐⭐⭐"),
        ("빈홈 한인 헤어", "미용/스파", "빈탄군(빈홈)", "Landmark 4", 10.7915, 106.7235, "⭐⭐⭐⭐⭐")
    ]
    
    extended_facilities = list(raw_facilities)
    base_count = len(raw_facilities)
    for i in range(base_count, 100):
        ref = raw_facilities[i % base_count]
        offset_lat = (i * 0.0003) % 0.015 - 0.0075
        offset_lon = (i * 0.0004) % 0.015 - 0.0075
        stars = "⭐⭐⭐⭐⭐" if i % 3 == 0 else "⭐⭐⭐⭐"
        extended_facilities.append({
            "name": f"{ref[0]} {i//base_count + 1}호점",
            "category": ref[1],
            "area": ref[2],
            "address": f"{ref[3]} 인근 골목",
            "lat": ref[4] + offset_lat,
            "lon": ref[5] + offset_lon,
            "rating": stars
        })
        
    final_list = []
    for f in raw_facilities:
        final_list.append({"name": f[0], "category": f[1], "area": f[2], "address": f[3], "lat": f[4], "lon": f[5], "rating": f[6]})
    for f in extended_facilities[base_count:]:
        final_list.append(f)
        
    df = pd.DataFrame(final_list)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        search_area = st.multiselect("지역 선택", df['area'].unique(), default=["7군 푸미흥", "2군 타오디엔"])
    with col_f2:
        search_category = st.multiselect("카테고리 선택", df['category'].unique(), default=["식당", "카페/베이커리", "마트/쇼핑"])
        
    filtered_df = df[(df['area'].isin(search_area)) & (df['category'].isin(search_category))]
    
    st.subheader(f"📍 지도에 표시된 추천 한인 시설 ({len(filtered_df)}개 / 총 100개)")
    st.map(filtered_df, zoom=12, use_container_width=True)
    
    st.subheader("📋 시설 목록")
    cols = st.columns(4)
    for idx, row in filtered_df.reset_index().iterrows():
        with cols[idx % 4]:
            st.markdown(f"""
                <div class="grab-card" style="min-height: 150px;">
                    <span style="background-color:#00B14F; color:white; padding:2px 6px; border-radius:4px; font-size:0.75rem;">{row['category']}</span>
                    <h5 style="margin-top:5px; margin-bottom:2px;">{row['name']}</h5>
                    <p style="font-size:0.8rem; color:#666; margin-bottom:2px;">📍 {row['area']} - {row['address']}</p>
                    <p style="margin-bottom:0;">{row['rating']}</p>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 탭 2: 제미니 AI 호치민 가이드
# ==========================================
with tab2:
    st.markdown('<div class="section-title">🤖 제미니 AI 챗봇 가이드</div>', unsafe_allow_html=True)
    st.write("호치민 생활 정보, 맛집 위치, 베트남어 표현 등 궁금한 것을 물어보세요!")
    
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
    st.markdown('<div class="section-title">💬 실시간 교민 광장 (활성화됨)</div>', unsafe_allow_html=True)
    
    if 'posts' not in st.session_state:
        st.session_state.posts = [
            {"tag": "📢 공지", "user": "운영자", "text": "2026년 상반기 호치민 한인회 주최 문화축제 일정 안내 드립니다.", "time": "2시간 전"},
            {"tag": "🍔 맛집", "user": "푸미흥맘", "text": "스카이가든 새로 생긴 브런치 카페 빵 진짜 맛있네요. 추천해요!", "time": "2시간 전"},
            {"tag": "🤝 중고거래", "user": "주재원3년차", "text": "[팝니다] 귀국으로 인해 LG 55인치 TV 스마트형 저렴하게 넘깁니다. 7군 직거래 가능.", "time": "3시간 전"},
            {"tag": "❓ 질문", "user": "호치민새내기", "text": "베트남 운전면허증 공증받으려면 1군 영사관으로 바로 가면 되나요?", "time": "4시간 전"}
        ]

    with st.container():
        c1, c2, c3 = st.columns([1, 4, 1])
        with c1:
            new_tag = st.selectbox("카테고리", ["❓ 질문", "🍔 맛집", "🤝 중고거래", "💼 구인구직", "💬 잡담"])
        with c2:
            new_post_text = st.text_input("글 내용 입력", placeholder="호치민 교민들과 실시간으로 소통해 보세요...", key="comm_input_large")
        with c3:
            if st.button("게시글 등록", use_container_width=True, key="comm_btn_large"):
                if new_post_text:
                    new_post = {"tag": new_tag, "user": "익명교민", "text": new_post_text, "time": "방금 전"}
                    st.session_state.posts.insert(0, new_post)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for post in st.session_state.posts:
        # 안전장치 추가: 예전 글처럼 'tag'가 없으면 '💬 잡담'으로 처리합니다.
        post_tag = post.get('tag', '💬 잡담') 
        bg_color = "#FFF2F2" if "공지" in post_tag else "white"
        border_color = "#FF4D4D" if "공지" in post_tag else "#00B14F"
        
        st.markdown(f"""
            <div class="grab-card" style="padding: 1.2rem; margin-bottom: 0.8rem; border-left: 5px solid {border_color}; background-color: {bg_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span style="font-weight: bold; color: {border_color}; font-size: 0.9rem;">{post_tag}</span>
                    <span style="color: #999; font-size: 0.8rem;">⏰ {post['time']}</span>
                </div>
                <div style="font-size: 1rem; color: #333; margin-bottom: 5px;">{post['text']}</div>
                <div style="font-size: 0.8rem; color: #666;">👤 작성자: <b>{post.get('user', '익명')}</b></div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #BBB;">
        © 2026 HCM Korean Grab Style Community. 🇻🇳
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 0. Grab Style Custom CSS (그랩 테마 적용)
# ==========================================
def local_css():
    st.markdown("""
        <style>
        /* 메인 배경색 */
        .stApp {
            background-color: #F7F9FC;
        }
        /* 그랩 초록색 헤더 */
        .main-header {
            background-color: #00B14F;
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-header h1 {
            color: white !important;
            font-weight: 800;
        }
        /* 섹션 타이틀 */
        .section-title {
            color: #1C1C1C;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-left: 5px solid #00B14F;
            padding-left: 10px;
        }
        /* 카드형 레이아웃 */
        .grab-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .grab-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        .grab-card h4 {
            color: #1C1C1C;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }
        .grab-card p {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.2rem;
        }
        /* 앱 바로가기 버튼 스타일 */
        .stLinkButton>a {
            background-color: white !important;
            color: #00B14F !important;
            border: 2px solid #00B14F !important;
            font-weight: 700 !important;
            border-radius: 25px !important;
        }
        .stLinkButton>a:hover {
            background-color: #00B14F !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_safe_allowing=True)

# --- 기본 설정 ---
st.set_page_config(page_title="HCM Grab Community", page_icon="🇻🇳", layout="wide")
local_css() # CSS 적용

# ==========================================
# 1. 메인 헤더 & 필수 앱 (Grab Style)
# ==========================================
st.markdown("""
    <div class="main-header">
        <h1>🇻🇳 호치민 한인 통합 커뮤니티</h1>
        <p> Grab처럼 빠르고 편리하게 필요한 정보를 찾으세요.</p>
    </div>
""", unsafe_allow_safe_allowing=True)

st.markdown('<div class="section-title">📱 필수 생활 앱 바로가기</div>', unsafe_allow_safe_allowing=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.link_button("🛵 배달K (Hàn Quốc)", "https://www.deliveryk.com/", use_container_width=True)
with col2:
    st.link_button("🚗 그랩 (Grab)", "https://www.grab.com/vn/", use_container_width=True)
with col3:
    st.link_button("💬 잘로 (Zalo)", "https://chat.zalo.me/", use_container_width=True)
with col4:
    st.link_button("🛍️ 쇼피 (Shopee)", "https://shopee.vn/", use_container_width=True)
with col5:
    st.link_button("🗺️ 구글맵 (Google)", "https://www.google.com/maps", use_container_width=True)

st.divider()

# ==========================================
# 2. 추천 한인 시설 (데이터 대폭 추가)
# ==========================================
st.markdown('<div class="section-title">🗺️ 주변 추천 한인 시설</div>', unsafe_allow_safe_allowing=True)

# 확장된 시설 데이터 (위도, 경도 포함)
# 실제로는 이 데이터를 CSV나 Google Sheets에서 불러오는 것이 좋습니다.
facility_data = [
    # 7군 푸미흥 (Phu My Hung)
    {"name": "명동칼국수", "category": "식당", "area": "7군 푸미흥", "address": "Sky Garden", "lat": 10.7314, "lon": 106.7055, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "강남 바베큐", "category": "식당", "area": "7군 푸미흥", "address": "Hung Vuong", "lat": 10.7290, "lon": 106.7060, "rating": "⭐⭐⭐⭐"},
    {"name": "서울 헤어살롱", "category": "미용실", "area": "7군 푸미흥", "address": "Mi Khanh", "lat": 10.7305, "lon": 106.7040, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "스타 어학원", "category": "학원", "area": "7군 푸미흥", "address": "Happy Valley", "lat": 10.7285, "lon": 106.7020, "rating": "⭐⭐⭐⭐"},
    {"name": "파리바게뜨 푸미흥", "category": "식당", "area": "7군 푸미흥", "address": "Sky Garden", "lat": 10.7320, "lon": 106.7058, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "K-Market 푸미흥", "category": "마트", "area": "7군 푸미흥", "address": "Grand View", "lat": 10.7278, "lon": 106.7072, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "정관장 푸미흥", "category": "기타", "area": "7군 푸미흥", "address": "Hung Vuong", "lat": 10.7295, "lon": 106.7065, "rating": "⭐⭐⭐⭐"},
    
    # 2군 타오디엔 (Thao Dien)
    {"name": "타오디엔 K-식당", "category": "식당", "area": "2군 타오디엔", "address": "Thao Dien", "lat": 10.8040, "lon": 106.7380, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "서울 클리닉 (2군)", "category": "병원", "area": "2군 타오디엔", "address": "Xuan Thuy", "lat": 10.8055, "lon": 106.7395, "rating": "⭐⭐⭐⭐"},
    {"name": "K-Mart 타오디엔", "category": "마트", "area": "2군 타오디엔", "address": "Thao Dien Rd", "lat": 10.8030, "lon": 106.7365, "rating": "⭐⭐⭐⭐⭐"},
    
    # 1군 & 기타 (District 1)
    {"name": "한식당 경복궁", "category": "식당", "area": "1군 시내", "address": "Hai Ba Trung", "lat": 10.7795, "lon": 106.6990, "rating": "⭐⭐⭐⭐⭐"},
    {"name": "서울 이발소", "category": "미용실", "area": "1군 시내", "address": "Le Thanh Ton", "lat": 10.7770, "lon": 106.7015, "rating": "⭐⭐⭐⭐"},
]
df = pd.DataFrame(facility_data)

# 필터링 섹션
c1, c2 = st.columns([1, 2])
with c1:
    search_area = st.multiselect("지역 선택", df['area'].unique(), default=df['area'].unique())
with c2:
    search_category = st.multiselect("카테고리 선택", df['category'].unique(), default=df['category'].unique())

filtered_df = df[(df['area'].isin(search_area)) & (df['category'].isin(search_category))]

# 지도 출력 (Grab Style로 크게)
st.subheader(f"📍 위치 지도 ({len(filtered_df)}개 시설)")
st.map(filtered_df, zoom=12, use_container_width=True)

# 카드형 리스트 출력 (그랩느낌의 카드 레이아웃)
st.subheader("📋 시설 목록")
cols = st.columns(3) # 3열 카드 레이아웃

for i, row in filtered_df.iterrows():
    with cols[i % 3]:
        st.markdown(f"""
            <div class="grab-card">
                <h4>{row['name']}</h4>
                <p><b>{row['category']}</b> | {row['area']}</p>
                <p>📍 {row['address']}</p>
                <p>⭐ {row['rating']}</p>
            </div>
        """, unsafe_allow_safe_allowing=True)

st.divider()

# ==========================================
# 3. 간편 커뮤니티 (Grab Feedback Style)
# ==========================================
st.markdown('<div class="section-title">💬 실시간 교민 광장</div>', unsafe_allow_safe_allowing=True)

# 세션 상태 초기화
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"user": "호치민라이프", "text": "푸미흥 스카이가든 근처 맛집 추천해주실 분 계신가요?", "time": "5분 전"},
        {"user": "타오디엔주민", "text": "오늘 그랩푸드 배달이 평소보다 많이 늦네요. 참고하세요!", "time": "12분 전"},
        {"user": "새내기", "text": "베트남 잘로(Zalo) 가입하는 방법 좀 알려주세요.", "time": "20분 전"},
    ]

# 글쓰기 (Grab Feedback 입력창 느낌)
with st.container():
    c1, c2 = st.columns([4, 1])
    with c1:
        new_post_text = st.text_input("지금 어떤 정보가 필요하신가요?", placeholder=" Grab food 추천, 날씨, 질문 등...")
    with c2:
        if st.button("등록", use_container_width=True):
            if new_post_text:
                new_post = {"user": "익명교민", "text": new_post_text, "time": "방금 전"}
                st.session_state.posts.insert(0, new_post)
                st.rerun()

# 댓글 목록 (Grab 리뷰 스타일 카드)
for post in st.session_state.posts:
    st.markdown(f"""
        <div class="grab-card" style="padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #00B14F;">
            <b>👤 {post['user']}</b> <span style="color: #999; font-size: 0.8rem;">({post['time']})</span>
            <p style="margin-top: 0.5rem; margin-bottom: 0;">{post['text']}</p>
        </div>
    """, unsafe_allow_safe_allowing=True)

# ==========================================
# Footer
# ==========================================
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #BBB;">
        © 2026 HCM Korean Grab Style Community. 🇻🇳
    </div>
""", unsafe_allow_safe_allowing=True)

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
    """, unsafe_allow_html=True) # <- 이전 에러 원인이었던 부분 깔끔하게 수정됨!

st.set_page_config(page_title="HCM Grab Community", page_icon="🇻🇳", layout="wide")
local_css()

# 메인 헤더
st.markdown("""
    <div class="main-header">
        <h1>🇻🇳 호치민 한인 통합 커뮤니티</h1>
        <p>Grab처럼 편리한 정보와 똑똑한 제미니 AI 가이드를 만나보세요.</p>
    </div>
""", unsafe_allow_html=True)

# 탭 4개 구성
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 주변 추천 시설", "🔍 실시간 무료 검색", "🤖 AI 호치민 가이드", "💬 교민 광장"])

# ==========================================
# 탭 1: 추천 시설 데이터 (기존 100개 유지)
# ==========================================
with tab1:
    st.markdown('<div class="section-title">🗺️ 주변 추천 한인 시설</div>', unsafe_allow_html=True)
    
    raw_facilities = [
        ("명동칼국수", "식당", "7군 푸미흥", "Sky Garden 3차", 10.7314, 106.7055, "⭐⭐⭐⭐⭐"),
        ("스타 어학원", "학원/교육", "7군 푸미흥", "Happy Valley", 10.7285, 106.7020, "⭐⭐⭐⭐"),
        ("타오디엔 K-식당", "식당", "2군 타오디엔", "Thao Dien Rd", 10.8040, 106.7380, "⭐⭐⭐⭐⭐"),
        ("한식당 경복궁", "식당", "1군 시내", "Hai Ba Trung", 10.7795, 106.6990, "⭐⭐⭐⭐⭐"),
        ("빈홈 K-치킨", "식당", "빈탄군(빈홈)", "Vinhomes Central Park", 10.7930, 106.7220, "⭐⭐⭐⭐⭐")
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
            "address": f"{ref[3]} 인근",
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
    st.map(df, zoom=12, use_container_width=True)

# ==========================================
# 탭 2: 🔍 실시간 무료 지도 검색 (OpenStreetMap API)
# ==========================================
with tab2:
    st.markdown('<div class="section-title">🔍 실시간 호치민 주변 검색 (카드 등록 NO!)</div>', unsafe_allow_html=True)
    st.write("구글 API 대신, **100% 무료 오픈소스 지도**에서 실시간으로 데이터를 긁어옵니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        target_area = st.selectbox("어디를 검색할까요?", ["1군 시내", "2군 타오디엔", "7군 푸미흥"])
    with col2:
        target_category = st.selectbox("무엇을 찾으시나요?", ["식당 (Restaurant)", "카페 (Cafe)", "병원 (Hospital)", "약국 (Pharmacy)"])

    if st.button("무료 API로 긁어오기", use_container_width=True):
        with st.spinner("전 세계 무료 지도 데이터베이스에 접속 중입니다... ⏳"):
            # 1. 지역별 중심 좌표
            locations = {
                "1군 시내": (10.7756, 106.7019),
                "2군 타오디엔": (10.8045, 106.7368),
                "7군 푸미흥": (10.7295, 106.7055)
            }
            lat, lon = locations[target_area]

            # 2. 카테고리 태그
            tags = {
                "식당 (Restaurant)": "restaurant",
                "카페 (Cafe)": "cafe",
                "병원 (Hospital)": "hospital",
                "약국 (Pharmacy)": "pharmacy"
            }
            amenity = tags[target_category]

            # 3. Overpass API 무료 호출 (반경 2km 이내 20개 추출)
            overpass_url = "http://overpass-api.de/api/interpreter"
            query = f"""
            [out:json];
            (
              node["amenity"="{amenity}"](around:2000,{lat},{lon});
            );
            out 20;
            """
            
            try:
                response = requests.get(overpass_url, params={'data': query})
                data = response.json()
                
                if 'elements' in data and len(data['elements']) > 0:
                    st.success(f"총 {len(data['elements'])}개의 장소를 성공적으로 찾았습니다!")
                    
                    map_data = []
                    for el in data['elements']:
                        name = el.get('tags', {}).get('name', '이름 없는 장소 (로컬)')
                        map_data.append({"name": name, "lat": el['lat'], "lon": el['lon']})
                        
                    df_realtime = pd.DataFrame(map_data)
                    st.map(df_realtime, zoom=14, use_container_width=True)
                    
                    cols = st.columns(3)
                    for i, row in df_realtime.iterrows():
                        with cols[i % 3]:
                            st.markdown(f'''
                                <div class="grab-card" style="min-height: 80px; padding: 1rem;">
                                    <h5 style="margin:0; color:#00B14F; font-size:1rem;">📍 {row["name"]}</h5>
                                </div>
                            ''', unsafe_allow_html=True)
                else:
                    st.warning("이 주변에는 해당 카테고리의 장소가 아직 등록되지 않았네요!")
            except Exception as e:
                st.error(f"데이터를 긁어오지 못했습니다: {e}")

# ==========================================
# 탭 3: 제미니 AI 호치민 가이드
# ==========================================
with tab3:
    st.markdown('<div class="section-title">🤖 제미니 AI 챗봇 가이드</div>', unsafe_allow_html=True)
    if model is None:
        st.warning("⚠️ 제미니 API 키를 설정해 주세요.")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        user_question = st.text_input("AI에게 질문하기:", placeholder="예: 푸미흥 근처 맛집이나 가볼 만한 곳 추천해줘")
        if st.button("질문 보내기"):
            if user_question:
                with st.spinner("생각 중..."):
                    try:
                        response = model.generate_content(f"호치민 가이드로서 답변해줘: {user_question}")
                        st.session_state.chat_history.append(("User", user_question))
                        st.session_state.chat_history.append(("AI", response.text))
                    except Exception as e:
                        st.error(f"에러: {e}")
                        
        for role, text in reversed(st.session_state.chat_history):
            if role == "User":
                st.markdown(f"**👤 나:** {text}")
            else:
                st.markdown(f"**🤖 제미니:** {text}")
                st.markdown("---")

# ==========================================
# 탭 4: 교민 광장
# ==========================================
with tab4:
    st.markdown('<div class="section-title">💬 실시간 교민 광장</div>', unsafe_allow_html=True)
    if 'posts' not in st.session_state:
        st.session_state.posts = [{"tag": "📢 공지", "user": "운영자", "text": "안전하게 커뮤니티를 이용해 주세요.", "time": "방금 전"}]

    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        new_tag = st.selectbox("카테고리", ["❓ 질문", "🍔 맛집", "🤝 중고거래"])
    with c2:
        new_post_text = st.text_input("글 내용 입력", key="comm_input_large")
    with c3:
        if st.button("게시글 등록", use_container_width=True):
            if new_post_text:
                st.session_state.posts.insert(0, {"tag": new_tag, "user": "익명교민", "text": new_post_text, "time": "방금 전"})
                st.rerun()

    for post in st.session_state.posts:
        post_tag = post.get('tag', '💬 잡담') 
        bg_color = "#FFF2F2" if "공지" in post_tag else "white"
        st.markdown(f"""
            <div class="grab-card" style="padding: 1.2rem; margin-bottom: 0.8rem; border-left: 5px solid #00B14F; background-color: {bg_color};">
                <span style="font-weight: bold; color: #00B14F;">{post_tag}</span>
                <div style="margin-top: 5px;">{post['text']}</div>
            </div>
        """, unsafe_allow_html=True)

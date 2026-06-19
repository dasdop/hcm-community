import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="호치민 한인 커뮤니티", page_icon="🇻🇳", layout="wide")

# --- 세션 상태 초기화 (게시판 데이터 임시 저장용) ---
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"id": 1, "title": "푸미흥 맛집 추천해주세요!", "author": "호치민초보", "content": "이번에 주재원으로 왔는데 맛집 공유 부탁드립니다.", "date": "2026-06-19"}
    ]

# --- 사이드바 메뉴 ---
st.sidebar.title("🇻🇳 HCM 커뮤니티")
menu = st.sidebar.radio("메뉴를 선택하세요", ["🏠 홈 & 필수 앱", "🗺️ 추천 한인 시설", "💬 자유 게시판"])

# ==========================================
# 1. 홈 & 필수 앱 바로가기 화면
# ==========================================
if menu == "🏠 홈 & 필수 앱":
    st.title("🇻🇳 호치민 한인 통합 시스템에 오신 것을 환영합니다!")
    st.markdown("베트남 호치민 생활에 필요한 모든 정보를 한 곳에서 확인하세요.")
    
    st.divider()
    
    st.subheader("📱 베트남 생활 필수 앱/사이트 바로가기")
    st.markdown("버튼을 누르면 해당 사이트로 바로 이동합니다.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("🛵 배달K (한식 배달)", "https://www.deliveryk.com/", use_container_width=True)
    with col2:
        st.link_button("🚗 그랩 (Grab)", "https://www.grab.com/vn/", use_container_width=True)
    with col3:
        st.link_button("💬 잘로 (Zalo 메신저)", "https://chat.zalo.me/", use_container_width=True)
    with col4:
        st.link_button("🛒 쇼피 (Shopee 쇼핑)", "https://shopee.vn/", use_container_width=True)

# ==========================================
# 2. 추천 한인 시설 (지도 + 목록)
# ==========================================
elif menu == "🗺️ 추천 한인 시설":
    st.title("🗺️ 호치민 추천 한인 시설")
    st.markdown("푸미흥(7군) 및 타오디엔(2군) 중심의 한인 시설 위치입니다.")
    
    # 카테고리 선택
    category = st.selectbox("카테고리를 선택하세요", ["전체", "식당", "미용실", "학원"])
    
    # 샘플 데이터 (위도 lat, 경도 lon 정보가 있어야 지도에 표시됩니다)
    facility_data = [
        {"name": "명동칼국수", "category": "식당", "address": "푸미흥 스카이가든", "lat": 10.7314, "lon": 106.7055},
        {"name": "강남 바베큐", "category": "식당", "address": "푸미흥 흥브엉", "lat": 10.7290, "lon": 106.7060},
        {"name": "서울 헤어살롱", "category": "미용실", "address": "푸미흥 미칸", "lat": 10.7305, "lon": 106.7040},
        {"name": "스타 어학원", "category": "학원", "address": "푸미흥 해피밸리", "lat": 10.7285, "lon": 106.7020},
        {"name": "타오디엔 K-식당", "category": "식당", "address": "타오디엔 2군", "lat": 10.8040, "lon": 106.7380},
    ]
    
    df = pd.DataFrame(facility_data)
    
    # 필터링 로직
    if category != "전체":
        df = df[df['category'] == category]
    
    # 지도 출력
    st.subheader("📍 위치 지도")
    st.map(df)
    
    # 리스트 출력
    st.subheader("📋 시설 목록")
    st.dataframe(df[['name', 'category', 'address']], use_container_width=True)

# ==========================================
# 3. 자유 게시판 (커뮤니티 기능)
# ==========================================
elif menu == "💬 자유 게시판":
    st.title("💬 교민 자유 게시판")
    st.markdown("호치민 생활 정보, 질문, 중고 거래 등을 자유롭게 나눠보세요.")
    
    # 글쓰기 폼
    with st.expander("📝 새 글 작성하기"):
        with st.form("new_post_form"):
            new_title = st.text_input("제목")
            new_author = st.text_input("작성자 (닉네임)")
            new_content = st.text_area("내용")
            submit_btn = st.form_submit_button("등록")
            
            if submit_btn:
                if new_title and new_author and new_content:
                    new_post = {
                        "id": len(st.session_state.posts) + 1,
                        "title": new_title,
                        "author": new_author,
                        "content": new_content,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.posts.insert(0, new_post) # 최신 글을 위로
                    st.success("게시글이 등록되었습니다!")
                    st.rerun()
                else:
                    st.error("제목, 작성자, 내용을 모두 입력해주세요.")
    
    st.divider()
    
    # 게시글 목록 출력
    for post in st.session_state.posts:
        with st.container():
            st.subheader(post['title'])
            st.caption(f"작성자: {post['author']} | 작성일: {post['date']}")
            st.write(post['content'])
            st.markdown("---")

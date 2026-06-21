import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_local_directory_data(url):
    # 1. 사람인 척 위장하기 (웹사이트가 로봇인 줄 알고 차단하는 것을 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("웹사이트에 접속 중입니다...")
    response = requests.get(url, headers=headers)
    
    # 접속 성공(200)일 때만 실행
    if response.status_code == 200:
        # 2. 웹페이지의 HTML 전체 긁어오기
        soup = BeautifulSoup(response.text, 'html.parser')
        
        extracted_data = []
        
        # 3. 원하는 정보 찾기 (여기가 제일 중요합니다!)
        # 주의: 아래 'div.store-item', 'h3.title' 등은 예시입니다. 
        # 실제 긁어올 사이트의 구조에 맞게 수정해야 합니다.
        store_list = soup.select('div.store-item') # 업소 목록을 감싸는 태그 찾기
        
        for store in store_list:
            try:
                # 각 업소에서 이름, 전화번호, 주소 뽑아내기
                name = store.select_one('h3.title').text.strip()
                phone = store.select_one('span.phone').text.strip()
                address = store.select_one('div.address').text.strip()
                
                extracted_data.append({
                    "업소명": name,
                    "전화번호": phone,
                    "주소": address
                })
            except AttributeError:
                # 정보가 누락된 업소는 건너뛰기
                continue
                
        # 4. 엑셀처럼 예쁜 데이터프레임으로 만들기
        df = pd.DataFrame(extracted_data)
        return df
    else:
        print(f"접속 실패: {response.status_code}")
        return None

# ==========================================
# 실행 테스트 (원하는 사이트 주소로 바꿔서 테스트하세요)
# ==========================================
target_url = "https://www.vnkorlife.com/neighborbusiness" # 긁어오고 싶은 실제 주소 입력
result_df = get_local_directory_data(target_url)

if result_df is not None:
    print(result_df)
    # 엑셀 파일로 바로 저장하고 싶다면 아래 주석을 푸세요!
    # result_df.to_csv("hochiminh_restaurants.csv", index=False, encoding="utf-8-sig")

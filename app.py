import streamlit as st
import gspread
import datetime
import os
import json

# --- 1. 페이지 설정 및 구글 시트 연동 ---
st.set_page_config(page_title="사전 설문", layout="centered")

try:
    # 로컬(PC) vs Streamlit Cloud(배포) 인증 분기
    credentials_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "google-credentials.json")

    if os.path.exists(credentials_path):
        gc = gspread.service_account(filename=credentials_path)
    else:
        creds_dict = st.secrets["gcp_service_account"]
        gc = gspread.service_account_from_dict(creds_dict)

    # (중요) 새로 만든 '사전 설문' 시트 이름을 입력합니다.
    GOOGLE_SHEET_NAME = "(DWG) 사전 설문 응답" 
    sheet = gc.open(GOOGLE_SHEET_NAME).sheet1

except Exception as e:
    st.error("구글 시트 연결에 실패했습니다. Streamlit Secrets 또는 시트 이름을 확인하세요.")
    st.error(f"오류: {e}")
    st.stop()

# --- [수정됨] 2. 설문지 헤더 ---
st.title("📝 [사전 설문] 행동강령 워크샵")
st.info("안녕하세요! 더 나은 소통 방식을 만들기 위한 **익명 설문**입니다. 여러분의 솔직한 의견은 워크샵의 핵심 '주제'로 활용됩니다.")

# --- 3. 설문 폼 (st.form) ---
with st.form(key="survey_form"):

    # --- [수정됨] 1. 컨테이너로 그룹화 ---
    st.header("1. 현재 소통 방식 진단")
    with st.container(border=True):
        q1_score = st.slider(
            "Q1. 현재 우리 조직(또는 팀)의 전반적인 소통 점수를 매긴다면 몇 점입니까?",
            min_value=1, max_value=10, value=5, help="(1점: 매우 불만족 ~ 10점: 매우 만족)"
        )
        
        q2_problems_options = [
            "업무 요청 방식이 불명확함 (배경, 마감일 공유 부족)",
            "피드백을 거의 받지 못함 (또는 너무 늦게 받음)",
            "회의가 너무 많고 비효율적임",
            "타 부서(팀)와의 협업이 원활하지 않음",
            "중요한 정보가 제때 공유되지 않음 (나만 모름)",
            "솔직한 의견을 말하기 어려움 (심리적 안전감 부족)"
        ]
        q2_problems = st.multiselect(
            "Q2. 현재 소통 방식에서 가장 '답답함'을 느끼는 부분은 무엇입니까? (중복 선택 가능)",
            q2_problems_options
        )
        q2_etc = st.text_input("Q2의 기타 의견:", placeholder="기타 의견이 있다면 입력해 주세요.")

        q3_reason_options = [
            "내 의견이 무시당할 것 같아서",
            "의견을 말해도 바뀌는 것이 없어서",
            "리더(상사)가 불편해할 것 같아서",
            "반대 의견을 말했다가 불이익을 받을까 봐",
            "잘 몰라서 (정보가 부족해서)",
            "해당 없음 / 솔직하게 말할 수 있음"
        ]
        q3_reason = st.radio(
            "Q3. '솔직한 의견을 말하기 어렵다'고 느끼신다면, 가장 큰 이유는 무엇입니까?",
            q3_reason_options, index=5 # '해당 없음'을 기본값으로
        )
        q3_etc = st.text_input("Q3의 기타 의견:", placeholder="기타 의견이 있다면 입력해 주세요.")

    # --- [수정됨] 2. 컨테이너로 그룹화 ---
    st.header("2. 워크샵 주제 및 사례 수집")
    with st.container(border=True):
        q4_topics_options = [
            "비효율적인 회의 방식 개선 (회의 시간, 방식 등)",
            "명확한 보고 및 빠른 피드백 (상하 소통)",
            "원활한 협업 요청 및 응답 (수평 소통)",
            "불명확한 업무 범위(R&R) 문제",
            "솔직한 의견을 주고받는 문화 (심리적 안전감)"
        ]
        q4_topics = st.multiselect(
            "Q4. 이번 워크샵에서 가장 비중 있게 다루었으면 하는 '주제'는 무엇입니까? (중복 선택 가능)",
            q4_topics_options
        )
        q4_etc = st.text_input("Q4의 기타 의견:", placeholder="기타 주제가 있다면 입력해 주세요.")

        q5_case = st.text_area(
            "Q5. 롤 플레잉으로 다루었으면 하는 구체적인 상황(갈등 사례)을 알려주세요.",
            placeholder="예: A팀에 자료를 요청했는데 3일째 답이 없었다 / 팀장님이 회의 직전에 보고서를 수정하라고 했다...",
            height=150
        )

        q6_habit = st.text_input(
            "Q6. 우리 조직이 반드시 고쳤으면 하는 '최악의 소통 습관'이 있다면 1가지만 적어주세요.",
            placeholder="예: 슬랙에 멘션(@) 없이 그냥 말하기 / 회의 시간에 아무도 의견 안 내기..."
        )
    
    # --- [수정됨] 3. 컨테이너로 그룹화 ---
    st.header("3. 워크샵을 통해 기대하는 것")
    with st.container(border=True):
        q7_expect = st.text_input(
            "Q7. '우리만의 행동강령'을 만든다면, 어떤 내용이 꼭 포함되어야 할까요?",
            placeholder="예: 회의는 30분 안에 끝낸다 / 모든 요청은 24시간 내 응답한다..."
        )

    st.divider()

    # --- 제출 버튼 ---
    submitted = st.form_submit_button("🚀 설문 제출하기", type="primary", use_container_width=True)

# --- 4. 제출 로직 ---
if submitted:
    try:
        # [1단계]에서 만든 11개 열 순서와 정확히 일치해야 함
        new_row = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            q1_score,
            str(q2_problems), # 리스트를 문자열로 저장
            q2_etc,
            q3_reason,
            q3_etc,
            str(q4_topics), # 리스트를 문자열로 저장
            q4_etc,
            q5_case,
            q6_habit,
            q7_expect
        ]
        
        # 구글 시트에 데이터 추가
        sheet.append_row(new_row)
        
        # 제출 완료 화면 보여주기
        st.success("✅ 설문이 성공적으로 제출되었습니다. 워크샵에서 뵙겠습니다!")
        st.balloons()

    except Exception as e:
        st.error(f"제출 중 오류가 발생했습니다: {e}")
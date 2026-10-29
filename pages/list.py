
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="자동 플래너",
    page_icon="📝",
    layout="wide"
)

st.title("📝 나의 자동 플래너")
st.write("캘린더에 입력한 일정으로 자동 생성된 플래너입니다.")

# main.py에서 저장한 일정 불러오기
events = st.session_state.get("events", [])

if not events:
    st.warning("등록된 일정이 없습니다. 캘린더에서 일정을 먼저 추가해 주세요.")

    if st.button("📅 캘린더로 돌아가기"):
        st.switch_page("main.py")

    st.stop()

# 날짜순 정렬
events = sorted(
    events,
    key=lambda event: (event["date"], event["start"])
)

# 플래너 날짜 범위
event_dates = [
    date.fromisoformat(event["date"])
    for event in events
]

min_date = min(event_dates)
max_date = max(event_dates)

st.subheader("📆 일정별 플래너")

# 일정이 있는 날짜만 표시
for current_date in sorted(set(event_dates)):
    day_events = [
        event for event in events
        if event["date"] == current_date.isoformat()
    ]

    st.markdown(
        f"### {current_date.strftime('%Y년 %m월 %d일 (%a)')}"
    )

    for event in day_events:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(
                f"**{event['start']}**"
            )
            st.caption(f"~ {event['end']}")

        with col2:
            with st.container(border=True):
                st.markdown(f"#### {event['title']}")

                if event["memo"]:
                    st.write(event["memo"])

    st.divider()

# 전체 일정 요약
st.subheader("📊 플래너 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 일정", f"{len(events)}개")

with col2:
    st.metric("일정이 있는 날짜", f"{len(set(event_dates))}일")

with col3:
    st.metric(
        "가장 빠른 일정",
        min(event["start"] for event in events)
    )

# 원래 캘린더로 돌아가기
if st.button("📅 캘린더로 돌아가기"):
    st.switch_page("main.py")


import streamlit as st
from datetime import date, time

st.set_page_config(
    page_title="나의 플래너",
    page_icon="📅",
    layout="wide"
)

# 일정 데이터 초기화
if "events" not in st.session_state:
    st.session_state.events = []

st.title("📅 나의 캘린더")
st.write("날짜를 선택하고 일정을 입력해 보세요.")

# 날짜 선택
selected_date = st.date_input(
    "일정 날짜 선택",
    value=date.today(),
    key="selected_date"
)

st.divider()

# 일정 입력
st.subheader("✏️ 일정 추가")

with st.form("event_form", clear_on_submit=True):
    title = st.text_input(
        "일정 제목",
        placeholder="예: 수학 문제집 풀기"
    )

    col1, col2 = st.columns(2)

    with col1:
        start_time = st.time_input(
            "시작 시간",
            value=time(9, 0)
        )

    with col2:
        end_time = st.time_input(
            "종료 시간",
            value=time(10, 0)
        )

    memo = st.text_area(
        "메모",
        placeholder="추가로 기록할 내용을 입력하세요."
    )

    submitted = st.form_submit_button(
        "일정 저장",
        use_container_width=True
    )

    if submitted:
        if not title.strip():
            st.error("일정 제목을 입력해 주세요.")
        elif end_time <= start_time:
            st.error("종료 시간은 시작 시간보다 늦어야 합니다.")
        else:
            st.session_state.events.append({
                "id": str(
                    len(st.session_state.events) + 1
                ),
                "date": selected_date.isoformat(),
                "title": title.strip(),
                "start": start_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M"),
                "memo": memo.strip()
            })

            st.success("일정이 저장되었습니다!")

st.divider()

# 선택한 날짜의 일정 표시
st.subheader(f"📌 {selected_date.strftime('%Y년 %m월 %d일')} 일정")

daily_events = [
    event for event in st.session_state.events
    if event["date"] == selected_date.isoformat()
]

daily_events.sort(key=lambda event: event["start"])

if daily_events:
    for event in daily_events:
        with st.container(border=True):
            st.markdown(
                f"**{event['start']} ~ {event['end']}**"
            )
            st.write(event["title"])

            if event["memo"]:
                st.caption(event["memo"])

            if st.button(
                "일정 삭제",
                key=f"delete_{event['id']}"
            ):
                st.session_state.events.remove(event)
                st.rerun()
else:
    st.info("이 날짜에는 등록된 일정이 없습니다.")

st.divider()

# 전체 일정 확인
with st.expander("📋 전체 일정 보기"):
    all_events = sorted(
        st.session_state.events,
        key=lambda event: (event["date"], event["start"])
    )

    if all_events:
        for event in all_events:
            st.write(
                f"📅 {event['date']} | "
                f"{event['start']}~{event['end']} | "
                f"{event['title']}"
            )
    else:
        st.write("저장된 일정이 없습니다.")

# 플래너 페이지 이동
if st.button(
    "✨ 자동 플래너 만들기",
    type="primary",
    use_container_width=True
):
    if st.session_state.events:
        st.switch_page("pages/list.py")
    else:
        st.warning("먼저 일정을 하나 이상 등록해 주세요.")

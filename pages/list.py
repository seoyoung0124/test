
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="Main List",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# 디자인
# -------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    h1, h2, h3, p, label {
        color: #222222;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e8e8e8;
        border-radius: 12px;
    }

    div.stButton > button {
        border: none;
        background: transparent;
        color: #222222;
        font-size: 24px;
    }

    div.stButton > button:hover {
        background: #f5f5f5;
        color: #111111;
    }

    div[data-testid="stCheckbox"] {
        padding-top: 4px;
        padding-bottom: 4px;
    }

    hr {
        border-color: #eeeeee;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 일정 데이터
# -------------------------
if "events" not in st.session_state:
    st.session_state.events = []

events = st.session_state.events

# 날짜별로 정렬
events.sort(
    key=lambda e: (e["date"], e["start"])
)

# 최초 플래너 날짜 설정
if "planner_date" not in st.session_state:
    if events:
        st.session_state.planner_date = date.fromisoformat(
            events[0]["date"]
        )
    else:
        st.session_state.planner_date = date.today()

if "completed_events" not in st.session_state:
    st.session_state.completed_events = set()

# -------------------------
# 전체 화면 구성
# -------------------------
left, main = st.columns([1.1, 4.9], gap="large")

# 왼쪽 메뉴
with left:
    st.write("")
    st.markdown("## Main")
    st.markdown("## List")

    st.divider()

    st.caption("MY PLANNER")
    st.write("하루의 일정을")
    st.write("차근차근 완성해 보세요.")

    st.write("")

    if st.button("＋ 일정 추가", use_container_width=True):
        st.switch_page("main.py")

# 가운데 플래너
with main:
    st.write("")

    # 날짜 이동 버튼
    prev_col, date_col, next_col = st.columns(
        [1, 5, 1],
        vertical_alignment="center"
    )

    with prev_col:
        if st.button("‹", key="prev_day", use_container_width=True):
            st.session_state.planner_date -= timedelta(days=1)
            st.rerun()

    with date_col:
        current_date = st.session_state.planner_date

        st.markdown(
            f"<div style='text-align:center;'>"
            f"<span style='font-size:12px; color:#999999;"
            f"letter-spacing:2px;'>DAILY PLANNER</span>"
            f"<h2 style='margin-top:8px; font-size:26px;'>"
            f"{current_date.strftime('%Y.%m.%d')}</h2>"
            f"<span style='color:#888888;'>"
            f"{current_date.strftime('%A')}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    with next_col:
        if st.button("›", key="next_day", use_container_width=True):
            st.session_state.planner_date += timedelta(days=1)
            st.rerun()

    st.write("")

    # 해당 날짜 일정만 가져오기
    day_events = [
        event for event in events
        if event["date"] == current_date.isoformat()
    ]

    # 플래너 카드
    with st.container(border=True):
        st.markdown("##### TODAY'S SCHEDULE")
        st.caption(f"총 {len(day_events)}개의 일정")

        st.divider()

        if day_events:
            for event in day_events:
                event_key = f"{event['date']}_{event['id']}"
                is_done = event_key in st.session_state.completed_events

                task_col, time_col = st.columns([4, 1])

                with task_col:
                    checked = st.checkbox(
                        event["title"],
                        value=is_done,
                        key=f"check_{event_key}"
                    )

                    if checked:
                        st.session_state.completed_events.add(event_key)
                    else:
                        st.session_state.completed_events.discard(event_key)

                    if event.get("memo"):
                        st.caption(event["memo"])

                with time_col:
                    st.markdown(
                        f"<div style='text-align:right;"
                        f"font-size:12px;color:#888888;"
                        f"padding-top:8px;'>"
                        f"{event['start']}<br>~ {event['end']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                st.divider()

            completed_count = sum(
                1 for event in day_events
                if f"{event['date']}_{event['id']}"
                in st.session_state.completed_events
            )

            st.caption(
                f"완료한 일정 {completed_count} / {len(day_events)}"
            )

            st.progress(completed_count / len(day_events))

        else:
            st.markdown(
                "<div style='text-align:center;padding:35px 5px;'>"
                "<p style='font-size:30px;'>☁️</p>"
                "<p style='color:#888888;'>"
                "이 날짜에는 등록된 일정이 없어요.</p>"
                "</div>",
                unsafe_allow_html=True
            )

    st.write("")

    # 날짜 바로 선택
    with st.expander("날짜 바로 선택하기"):
        picked_date = st.date_input(
            "플래너 날짜",
            value=current_date,
            key="date_picker"
        )

        if st.button("이 날짜 보기", use_container_width=True):
            st.session_state.planner_date = picked_date
            st.rerun()

    st.write("")

    if st.button("← 캘린더로 돌아가기", use_container_width=True):
        st.switch_page("main.py")

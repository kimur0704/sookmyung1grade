import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="스마트 도서관 좌석 추천", page_icon="📚", layout="wide")
st.title("📚 스마트 도서관 좌석 추천 시스템")

# ------------------------
# 1. 조건 입력
# ------------------------
task = st.selectbox("오늘 할 일", ["과제", "줌 회의", "독서", "스터디"])
noise = st.radio("소음 허용 여부", ["O", "X"])
typing = st.radio("노트북 사용 (타자)", ["O", "X"])
food = st.radio("취식 여부", ["O", "X"])
people = st.selectbox("희망 인원 수", [1, 2, 4, 6])

# ------------------------
# 2. 도서관 DB
# ------------------------
SEATS = {
    "1층 신한로비": {"소음": "O", "타이핑": "O", "취식": "O", "인원": "무관", "좌표": (2, 1)},
    "1층 세계여성문학관": {"소음": "X", "타이핑": "X", "취식": "X", "인원": "1", "좌표": (4, 1)},
    "2층 DICA 플라자": {"소음": "O", "타이핑": "O", "취식": "X", "인원": "1~2", "좌표": (2, 2)},
    "2층 SMART 플라자": {"소음": "O", "타이핑": "O", "취식": "X", "인원": "1~2", "좌표": (4, 2)},
    "3층 자료실 A": {"소음": "X", "타이핑": "O", "취식": "X", "인원": "무관", "좌표": (2, 3)},
    "4층 대학원열람실": {"소음": "X", "타이핑": "X", "취식": "X", "인원": "무관", "좌표": (4, 3)},
    "5층 C.C 플라자": {"소음": "O", "타이핑": "O", "취식": "O", "인원": "무관", "좌표": (2, 4)},
    "6층 S4 열람실": {"소음": "X", "타이핑": "O", "취식": "X", "인원": "무관", "좌표": (4, 4)}
}

# ------------------------
# 3. 추천 알고리즘 (점수 계산)
# ------------------------
results = []
for seat, cond in SEATS.items():
    score = 0
    if cond["소음"] == noise: score += 1
    if cond["타이핑"] == typing: score += 1
    if cond["취식"] == food: score += 1
    if cond["인원"] == "무관" or str(people) in cond["인원"]: score += 1
    results.append((seat, score, cond["좌표"]))

# 점수순 정렬
results = sorted(results, key=lambda x: x[1], reverse=True)

# ------------------------
# 4. 시각화
# ------------------------
if st.button("✨ 최적 좌석 추천받기"):
    fig = go.Figure()

    # 전체 공간 표시 (회색 점)
    for seat, score, (x, y) in results:
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(size=20, color="lightgray"),
            text=[seat],
            textposition="bottom center",
            showlegend=False
        ))

    # 상위 3개 추천 좌석 색상 표시
    colors = ["red", "orange", "green"]
    labels = ["1순위", "2순위", "3순위"]

    for i, (seat, score, (x, y)) in enumerate(results[:3]):
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(size=25, color=colors[i]),
            text=[labels[i]],
            textposition="top center",
            name=f"{labels[i]}: {seat}"
        ))

    fig.update_layout(
        title="📍 도서관 공간 추천 (예시)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------
    # 5. 예약 기능
    # ------------------------
    choice = st.selectbox("예약할 좌석을 선택하세요", [r[0] for r in results[:3]])
    if st.button("좌석 예약"):
        st.success(f"{choice} 예약 완료 ✅")
import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 처음에 한 번만 실행하여 session_state에 match 초기화
if 'match' not in st.session_state:
    st.session_state.match = []

if 'mb' not in st.session_state:
    st.session_state.mb = []

if 'mv' not in st.session_state:
    st.session_state.mv = -1

# session_state의 match를 mat으로 축약하여 사용
mat = st.session_state.match
mb = st.session_state.mb
mv = st.session_state.mv

dclass = ['1반', '2반', '3반', '4반']

def home():
    global mv, mat, mb
    lenm = len(mat)
    st.info("**:rainbow[환영합니다.]**")
    selected_date = st.date_input("추가할 날짜를 선택하세요", datetime.today())
    selected_class1 = st.selectbox(
        '왼쪽에 표시됩니다',
        dclass,
        index=None,
        placeholder="왼쪽에 표시됩니다"
    )
    selected_class2 = st.selectbox(
        '오른쪽에 표시됩니다',
        dclass,
        index=None,
        placeholder="오른쪽에 표시됩니다"
    )
    omg = st.button('adf')
    if omg:
        mat.append([selected_date.month, selected_date.day, selected_class1, -1, -1, selected_class2])
        # st.session_state.match = mat  # 업데이트된 mat를 session_state에 저장
        st.experimental_rerun()  # 페이지를 다시 로드하여 UI를 업데이트
    st.divider()
    mb = []
    for i in range(lenm):
        if mat[i][3] == -1 and mat[i][4] == -1:
            mb.append(st.checkbox(f"{mat[i][0]}/{mat[i][1]} {mat[i][2]}  경기전  {mat[i][5]}", key=f"checkbox_{i}"))
        else:
            mb.append(st.checkbox(f"{mat[i][0]}/{mat[i][1]} {mat[i][2]}  {mat[i][3]} : {mat[i][4]}  {mat[i][5]}",C))
    if mb.count(True) > 1:
        st.warning('1개만 선택해주세요.')
    if mb != [False] * len(mb):
        for i in range(len(mb)):
            if mb[i]:
                mv = i

def welcome():
    st.balloons()

# 사이드바 구성
st.sidebar.title("DFA")
st.sidebar.radio(
    "**Select:**",
    ["**:rainbow[Home]**", "**free fall**", "**uniform linear motion**", "**projectile motion**"],
    captions=["about app", "자유 낙하", "등속 직선 운동", "포물선 운동"],
    key="kind_of_motion", on_change=welcome
)

# 선택한 동작(도움말 또는 시뮬레이션) 실행
if st.session_state["kind_of_motion"] == "**:rainbow[Home]**":
    home()
elif st.session_state["kind_of_motion"] == "**free fall**":
    st.info('hello2')
elif st.session_state["kind_of_motion"] == "**uniform linear motion**":
    st.info('hello3')
elif st.session_state["kind_of_motion"] == "**projectile motion**":
    st.info('hello4')

# 업데이트된 mb와 mv를 session_state에 다시 저장
st.session_state.mb = mb
st.session_state.mv = mv

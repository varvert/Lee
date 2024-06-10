import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 처음에 한 번만 실행하여 session_state에 match 초기화
if 'match' not in st.session_state:
    st.session_state.match = []

if 'mb' not in st.session_state:
    st.session_state.mb = [] # left list, right list, goal list, pp1, pp2

if 'mv' not in st.session_state:
    st.session_state.mv = -1
if 'tm' not in st.session_state:
    st.session_state.tm ={'1반':[],'2반':[],'3반':[],'4반':[]}
if 'mg' not in st.session_state:
    st.session_state.mg =[]
if 'fpl' not in st.session_state:
    st.session_state.fpl =[]
if 'pc' not in st.session_state:
    st.session_state.pc ={}
# session_state의 match를 mat으로 축약하여 사용
mat = st.session_state.match
mb = st.session_state.mb
mv = st.session_state.mv
tm=st.session_state.tm
mg=st.session_state.mg
fpl=st.session_state.fpl
pc=st.session_state.pc
dclass = ['1반', '2반', '3반', '4반']

def home():
    global mv
    lenm = len(mat)
    st.title("**:rainbow[환영합니다.]**")
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
    col1, col2 = st.columns(2)
    with col1:
        addb = st.button('add')
    if addb:
        mat.append([selected_date.month, selected_date.day, selected_class1,
                    -1,-1, selected_class2,0,0])
        # st.session_state.match = mat  # 업데이트된 mat를 session_state에 저장
        mb.append([])
        fpl.append([[],[],[],[]])
        st.experimental_rerun()  # 페이지를 다시 로드하여 UI를 업데이트
    with col2:
        delb = st.button('del')
    if delb:
        for i in range(lenm):
            if mat[i][0]==selected_date.month and mat[i][1]==selected_date.day and mat[i][2]==selected_class1 and mat[i][5]== selected_class2:
                del mat[i]
                del mb[i]
                del fpl[i]
                st.experimental_rerun()  # 페이지를 다시 로드하여 UI를 업데이트
    st.divider()
    mb1 = []
    for i in range(lenm):
        if mat[i][3] == -1 and mat[i][4] == -1:
            mb1.append(st.checkbox(f"{mat[i][0]}/{mat[i][1]} {mat[i][2]}  경기전  {mat[i][5]}", key=f"checkbox_{i}"))
        else:
            mb1.append(st.checkbox(f"{mat[i][0]}/{mat[i][1]} {mat[i][2]}  {mat[i][3]} : {mat[i][4]}  {mat[i][5]}"))
    if mb1.count(True) > 1:
        mb1[0]=False
        st.warning('1개만 선택해주세요.')
    if mb1 != [False] * len(mb1):
        for i in range(len(mb1)):
            if mb1[i]:
                mv = i
def seematch():
    global mv
    if mv==-1:
        st.warning('경기를 선택해주세요')
    else:
        m,d,t1,g1,g2,t2=mat[mv][0:6]
        st.title(f'{m}/{d} 경기 결과')
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.write('')
        with col2:
            st.title(f'{t1}')
            if g1 != -1:
                st.title(g1)
        with col3:
            st.title('|')
            if g1 !=-1:
                st.title(':')
        with col4:
            st.title(t2)
            if g2!= -1:
                st.title(g2)
        with col5:
            st.write('')
        col1,col2,col3= st.columns(3)
        with col1:
            st.write('')
        with col2:
            if g1 == g2 == -1:
                st.title('경기전')
        with col3:
            st.write('')

        tabc=st.tabs(['골정보 보기','라인업 보기','응원하기'])
        with tabc[0]:
            col1,col2= st.columns(2)
            with col1:
                for i in range(len(mg)):
                    if mg[i][0]==mv and mg[i][1]==t1:
                        st.write(mg[i][2])
            with col2:
                for i in range(len(mg)):
                    if mg[i][0]==mv and mg[i][1]==t2:
                        st.write(mg[i][2])
        with tabc[1]:
            fos=st.selectbox('',['선발','교체'])
            col1,col2= st.columns(2)
            with col1:
                if fos=='선발':
                    st.title(f'{t1} 선발')
                    for i in range(len(fpl[mv][0])):
                        st.write(fpl[mv][0][i])
                elif fos=='교체':
                    st.title(f'{t1} 교체')
                    for i in range(len(fpl[mv][2])):
                        st.write(fpl[mv][2][i])
            with col2:
                if fos=='선발':
                    st.title(f'{t2} 선발')
                    for i in range(len(fpl[mv][1])):
                        st.write(fpl[mv][1][i])
                elif fos=='교체':
                    st.title(f'{t2} 교체')
                    for i in range(len(fpl[mv][3])):
                        st.write(fpl[mv][3][i])
        with tabc[2]:
            col1,col2= st.columns(2)
            with col1:
                st.title(f'{t1}')
                cheer=st.button('응원')
                if cheer:
                    mat[mv][6]+=1
                st.title(mat[mv][6])
            with col2:
                st.title(f'{t2}')
                cheer=st.button('응원 ')
                if cheer:
                    mat[mv][7]+=1
                st.title(mat[mv][7])

def changematch():
    global mv
    m, d, t1, g1, g2, t2 = mat[mv][0:6]
    tabc=st.tabs(['경기기록 변경','선수 추가'])
    with tabc[0]:
        if mv == -1:
            st.warning('경기를 선택해주세요')
        else:
            num1 = st.number_input('왼쪽 팀 점수를 입력하세요', value=mat[mv][3], key='num1')
            num2 = st.number_input('오른쪽 팀 점수를 입력하세요', value=mat[mv][4], key='num2')
            mat[mv][3] = num1
            mat[mv][4] = num2
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                fos=st.selectbox('',['선발','교체'])
                if fos=='선발':
                    st.title('왼쪽팀 선발')
                    lfp=st.selectbox(f'{t1}선발',tm[t1])
                    col3,col4 = st.columns(2)
                    with col3:
                        ad=st.button('추가')
                        if ad:
                            fpl[mv][0].append(lfp)
                    with col4:
                        db=st.button('제거 ')
                        if db:
                            if lfp in fpl[mv][0]:
                                fpl[mv][0].remove(lfp)
                elif fos=='교체':
                    st.title('왼쪽팀 교체')
                    lfp=st.selectbox(f'{t1}교체',tm[t1])
                    col3,col4 = st.columns(2)
                    with col3:
                        ad=st.button('추가  ')
                        if ad:
                            fpl[mv][2].append(lfp)
                    with col4:
                        db=st.button('제거   ')
                        if db:
                            if lfp in fpl[mv][2]:
                                fpl[mv][2].remove(lfp)
            with col2:
                fos1 = st.selectbox('', ['선발 ', '교체 '])
                if fos1 == '선발 ':
                    st.title('오른쪽팀 선발')
                    lfp=st.selectbox(f'{t2}선발',tm[t2])
                    col3,col4 = st.columns(2)
                    with col3:
                        ad=st.button('추가 ')
                        if ad:
                            fpl[mv][1].append(lfp)
                    with col4:
                        db=st.button('제거  ')
                        if db:
                            if lfp in fpl[mv][1]:
                                fpl[mv][1].remove(lfp)
                elif fos1=='교체 ':
                    st.title('오른쪽팀 교체')
                    lfp=st.selectbox(f'{t2}교체',tm[t2])
                    col3,col4 = st.columns(2)
                    with col3:
                        ad=st.button('추가 ')
                        if ad:
                            fpl[mv][3].append(lfp)
                    with col4:
                        db=st.button('제거  ')
                        if db:
                            if lfp in fpl[mv][3]:
                                fpl[mv][3].remove(lfp)

            st.divider()
            gpb=st.selectbox('골넣은 선수의 반을 입력하세요',[t1,t2])
            gpn=st.selectbox('골넣은 선수의 이름을 입력하세요',tm[gpb])
            c1,c2=st.columns(2)
            with c1:
                ok=st.button('확인')
                if ok:
                    mg.append([mv,gpb,gpn])
            with c2:
                no=st.button('취소')
                if no:
                    if [mv,gpb,gpn] in mg:
                        mg.remove([mv,gpb,gpn])

    with tabc[1]:
        ban=st.selectbox('반을 선택하세요',dclass)
        name=st.text_input('이름을 입력하세요')
        col1,col2=st.columns(2)
        with col1:
            ok=st.button('확인 ')
            if ok:
                tm[ban].append(name)
                pc[tuple([ban,name])]=[]
                # st.experimental_rerun()
        with col2:
            de=st.button('제거')
            if de:
                if name in tm[ban]:
                    tm[ban].remove(name)
                del pc[tuple([ban,name])]
                for i in mg:
                    if i[1]==ban and i[2]==name:
                        mg.remove(i)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            col1.header('1반')
            tmd=pd.DataFrame(tm['1반'])
            st.dataframe(tmd,width=200)
        with col2:
            col2.header('2반')
            tmd=pd.DataFrame(tm['2반'])
            st.dataframe(tmd,width=200)
        with col3:
            col3.header('3반')
            tmd=pd.DataFrame(tm['3반'])
            st.dataframe(tmd,width=200)
        with col4:
            col4.header('4반')
            tmd=pd.DataFrame(tm['4반'])
            st.dataframe(tmd,width=200)
def cad():
    tabc=st.tabs(['이번 시즌 데이터 보기','선수 코멘트'])
    with tabc[0]:
        bgp={}
        for i in mg:
            if tuple(i[1:3]) in list(bgp.keys()):
                bgp[tuple(i[1:3])]+=1
            else:
                bgp[tuple(i[1:3])]=1
        sorted_bgp=dict(sorted(bgp.items(),key=lambda item:item[1],reverse=True))
        sorted_bgp_key=list(sorted_bgp.keys())
        st.write(random.choice(['**:green[현재 득점왕]**','**:red[현재 득점왕]**','**:rainbow[현재 득점왕]**']))
        if sorted_bgp_key !=[]:
            st.write(sorted_bgp_key[0][0]+' '+sorted_bgp_key[0][1])
            data={
                '반': [i[0] for i in sorted_bgp_key],
                '이름': [i[1] for i in sorted_bgp_key],
                '득점수': [sorted_bgp[i] for i in sorted_bgp_key]
            }
            df=pd.DataFrame(data)
            st.table(df)
        else:
            st.write('없음')
    with tabc[1]:
        ban=st.selectbox('반을 선택하세요',dclass)
        name=st.selectbox('이름을 선택하세요',tm[ban])
        st.write('')
        coment=st.text_input('코멘트를 달아주세요.')
        add=st.button('추가')
        st.write('')
        if add:
            pc[tuple([ban,name])].append(coment)
        if tuple([ban,name])in pc.keys():
            asd=pc[tuple([ban,name])]
            for i in asd:
                st.info(i)
def welcome():
    st.balloons()

# 사이드바 구성
st.sidebar.title("DFA")
st.sidebar.radio(
    "MENU",
    ["**:rainbow[Home]**", "**경기기록**", "**정보 수정**", "**선수 코멘트 및 데이터**"],
    captions=["", "", "", ""],
    key="DFA",
    # on_change=welcome

)

# 선택한 동작(도움말 또는 시뮬레이션) 실행
if st.session_state["DFA"] == "**:rainbow[Home]**":
    home()
elif st.session_state["DFA"] == "**경기기록**":
    seematch()
elif st.session_state["DFA"] == "**정보 수정**":
    changematch()
elif st.session_state["DFA"] == "**선수 코멘트 및 데이터**":
    cad()

# 업데이트된 mb와 mv를 session_state에 다시 저장
st.session_state.mb = mb
st.session_state.mv = mv
st.session_state.mg = mg
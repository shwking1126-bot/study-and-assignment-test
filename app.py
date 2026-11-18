import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='공부 과제 성향 테스트', page_icon='📚', layout='centered')

# 16가지 결과: 코드 -> (이름, 설명)
RESULTS = {
    'NSBI': ('자유로운 영혼의 천재 기획자', '적당한 소음이 있는 카페에서 마감 직전의 압박감을 에너지 삼아 기발한 아이디어를 쏟아냅니다. 남들의 간섭 없이 혼자서 전체 판을 짤 때 최고의 퍼포먼스를 냅니다.'),
    'NSBC': ('아이디어를 불태우는 열정적인 브레인스토머', '시끌벅적한 분위기 속에서 팀원들과 수다 떨듯 아이디어를 주고받으며 큰 그림을 그립니다. 데드라인이 다가올수록 초인적인 추진력을 발휘하는 분위기 메이커입니다.'),
    'NSDI': ('마감 1시간 전의 카공족 해결사', '카페 백색소음을 배경으로 막판 스퍼트를 올려 세세한 자료 조사와 문서 작업을 혼자서 뚝딱 해치웁니다. 발등에 불이 떨어져야 디테일이 살아나는 실전파입니다.'),
    'NSDC': ('위기 상황에서 빛나는 단기전 멀티플레이어', '급한 프로젝트나 시험 기간에 스터디 카페·라디오 등을 틀어놓고 동료들과 실시간으로 소통하며 빠진 부분을 꼼꼼히 채워 넣습니다. 위기 대처 능력이 뛰어납니다.'),
    'NMBI': ('카페에서 미래를 설계하는 꾸준한 전략가', '매일 단골 카페에 출석 도장을 찍으며 장기 프로젝트의 로드맵이나 공부 커리큘럼을 혼자서 차근차근 구상합니다. 조급해하지 않고 큰 방향성을 꾸준히 다듬어 갑니다.'),
    'NMBC': ('커피 한 잔과 함께 성장하는 네트워커', '스터디 모임이나 오픈 오피스에서 동료들과 주기적으로 진행 상황을 공유하며 큰 방향을 맞춰갑니다. 함께 대화하며 얻는 영감으로 꾸준히 전진하는 타입입니다.'),
    'NMDI': ('매일 조금씩 완성하는 카공족 성실러', '적당한 생활 소음이 있어야 오히려 집중이 잘 되며, 매일 정해진 분량의 공부나 업무 디테일을 혼자서 묵묵히 처리합니다. 겉보기엔 여유로워 보여도 속이 꽉 찬 실속파입니다.'),
    'NMDC': ('소통으로 디테일을 다듬는 오픈형 조율자', '개방된 공간에서 팀원들과 수시로 피드백을 주고받으며 실무의 작은 오류까지 꼼꼼하게 잡아냅니다. 꾸준한 커뮤니케이션으로 완성도를 높이는 협업의 윤활유입니다.'),
    'QSBI': ('고독한 밤의 혁신가, 새벽형 천재', '모두가 잠든 조용한 방에서 마감 직전 무서운 몰입력을 발휘합니다. 혼자서 남들이 생각하지 못한 창의적인 구조와 핵심 논리를 단숨에 세우는 승부사 기질이 있습니다.'),
    'QSBC': ('핵심만 짚어내는 단기전 전략 리더', '조용한 환경에서 혼자 큰 틀을 빠르게 잡은 뒤, 팀원들과 핵심 방향만 압축적으로 공유해 단기간에 프로젝트를 돌파합니다. 불필요한 잡담보다 효율적인 의사결정을 선호합니다.'),
    'QSDI': ('진공 상태의 완벽주의 벼락치기 장인', '노이즈 캔슬링 이어폰을 끼고 외부와 완전히 단절된 상태에서 막판 스퍼트를 올립니다. 짧은 시간 안에 방대한 암기나 꼼꼼한 데이터 정리를 혼자 해내는 초집중 타입입니다.'),
    'QSDC': ('조용히 판을 뒤집는 실무 해결사', '평온한 공간에서 혼자 치열하게 디테일을 파고든 뒤, 결정적인 순간에 팀원들과 조율해 결과물의 퀄리티를 확 끌어올립니다. 마감 직전 가장 믿음직한 구원투수입니다.'),
    'QMBI': ('조용한 서재의 마스터플래너', '방해받지 않는 공간에서 매일 일정 시간을 투자해 거시적인 계획과 장기 목표를 혼자 설계합니다. 한 번 세운 큰 그림을 끝까지 밀고 나가는 뚝심 있는 사색가입니다.'),
    'QMBC': ('깊이 있는 대화로 방향을 잡는 사색형 리더', '정돈된 환경에서 차분하게 전체 맥락을 짚어내고, 동료들과 정기적인 회의를 통해 팀이 올바른 방향으로 가고 있는지 꾸준히 점검하는 안정적인 조율자입니다.'),
    'QMDI': ('오차 제로에 도전하는 독서실 모범생', '완벽한 정적 속에서 매일 계획된 분량을 한 치의 오차도 없이 혼자 완수합니다. 꼼꼼한 필기, 체계적인 폴더 정리 등 성실함과 디테일의 끝판왕입니다.'),
    'QMDC': ('빈틈없는 체크리스트의 협업 수호자', '차분한 환경에서 세부 일정과 할 일을 매일 관리하며, 팀원들과 진행 상황을 꼼꼼히 공유해 프로젝트가 펑크 나지 않도록 지키는 가장 든든한 팀플레이어입니다.'),
}

# 각 문항의 axis는 첫 번째 성향 문자로 지정. 선택지는 첫 번째 성향부터 두 번째 성향 순서.
# slider는 1(왼쪽 성향 강함) ~ 5(오른쪽 성향 강함), 3은 중립.
QUESTIONS = [
    {'axis': 'N', 'kind': 'radio', 'title': '가장 집중이 잘 되는 장소는?', 'options': ['적당한 소음이 있는 카페', '아주 조용한 독서실']},
    {'axis': 'S', 'kind': 'radio', 'title': '과제 마감까지 일주일 남았다면?', 'options': ['마감이 가까워져야 집중력이 폭발한다', '매일 조금씩 나누어 진행한다']},
    {'axis': 'B', 'kind': 'radio', 'title': '새로운 과제를 받으면 가장 먼저 하는 일은?', 'options': ['주제와 전체 방향부터 구상한다', '세부 요구사항과 할 일부터 정리한다']},
    {'axis': 'I', 'kind': 'radio', 'title': '팀 과제에서 더 편한 방식은?', 'options': ['내 담당 부분을 혼자 책임지고 완성한다', '중간중간 팀원들과 자주 의견을 나눈다']},
    {'axis': 'N', 'kind': 'slider', 'title': '공부할 때 주변 소음에 대한 선호는?', 'left': '생활 소음이 있는 편이 좋다', 'right': '완전히 조용해야 좋다'},
    {'axis': 'S', 'kind': 'slider', 'title': '장기 과제를 진행할 때 나의 리듬은?', 'left': '막판 집중형', 'right': '매일 분할형'},
    {'axis': 'B', 'kind': 'slider', 'title': '보고서 작성에서 더 끌리는 단계는?', 'left': '핵심 아이디어와 구조 설계', 'right': '근거 수집과 세부 작성'},
    {'axis': 'I', 'kind': 'slider', 'title': '작업 중 피드백을 받는 방식은?', 'left': '완성한 뒤 한 번에 공유', 'right': '진행하면서 자주 공유'},
    {'axis': 'N', 'kind': 'radio', 'title': '오랜 시간 공부해야 할 때 선택할 공간은?', 'options': ['음악이나 사람 소리가 조금 있는 공간', '말소리가 거의 들리지 않는 공간']},
    {'axis': 'S', 'kind': 'radio', 'title': '시험 공부 계획에서 나와 더 가까운 모습은?', 'options': ['시험이 임박하면 몰입해서 끝낸다', '평소에 일정 분량씩 복습한다']},
]

AXES = [('N', 'Q', '작업환경', '카페·소음', '독서실·정적'),
        ('S', 'M', '진행방식', '마감 집중', '꾸준한 분할'),
        ('B', 'D', '사고흐름', '큰 그림', '세부 실행'),
        ('I', 'C', '협업태도', '혼자 책임', '소통·조율')]
SECOND = {'N': 'Q', 'S': 'M', 'B': 'D', 'I': 'C'}

st.markdown('''<style>
.stApp {background:linear-gradient(145deg,#faf7ff 0%,#f0e8ff 100%);color:#302344;}
.block-container {max-width:800px;padding-top:2rem;padding-bottom:4rem;}
h1,h2,h3 {color:#59318e!important;}
.hero {background:linear-gradient(120deg,#8558d9,#aa83ef);border-radius:22px;padding:28px;color:white;margin-bottom:20px;}
.hero h1 {color:white!important;font-size:2rem;margin:0 0 10px;}
.hero p {margin:0;color:#f8f2ff;}
.question-card {background:white;border:1px solid #e7dcfb;border-radius:16px;padding:18px 20px 4px;margin:18px 0 8px;box-shadow:0 5px 18px #6f4fa112;}
.question-card h3 {font-size:1.07rem;margin:0 0 8px;}
.result-card {background:white;border:2px solid #d6c2f9;border-radius:22px;padding:28px;margin:20px 0;box-shadow:0 8px 24px #6949a019;}
.result-code {font-size:2.4rem;font-weight:800;color:#7646c2;}
div.stButton > button[kind="primary"] {background:#8050cf;border-color:#8050cf;border-radius:12px;}
div.stButton > button {border-radius:12px;}
[data-testid="stProgressBar"] div[role="progressbar"] {background-color:#8d5cdd;}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📚 공부 과제 성향 테스트</h1><p>10개의 질문으로 알아보는 나만의 공부 스타일 · 16가지 유형</p></div>', unsafe_allow_html=True)

if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_result' not in st.session_state:
    st.session_state.show_result = False


def reset_test():
    st.session_state.answers = {}
    st.session_state.show_result = False
    # 위젯에 저장된 기존 선택값도 초기화
    for idx in range(len(QUESTIONS)):
        st.session_state.pop(f'q_{idx}', None)


def calculate_result(answers):
    # 라디오는 선택 방향에 2점, 슬라이더는 중립 기준 거리만큼 가중치 부여.
    # 중립 또는 완전 동점이면 첫 번째 코드(N/S/B/I)를 선택하는 명시적 규칙.
    scores = {letter: 0 for pair in SECOND.items() for letter in pair}
    for idx, answer in answers.items():
        question = QUESTIONS[idx]
        first = question['axis']
        second = SECOND[first]
        if question['kind'] == 'radio':
            scores[first if answer == 0 else second] += 2
        else:
            if answer < 3:
                scores[first] += 3 - answer
            elif answer > 3:
                scores[second] += answer - 3
    code = ''.join(a if scores[a] >= scores[b] else b for a, b, *_ in AXES)
    return code, scores


if not st.session_state.show_result:
    completed = len(st.session_state.answers)
    st.markdown(f'**응답 진행률: {completed} / {len(QUESTIONS)}문항**')
    st.progress(completed / len(QUESTIONS))
    st.caption('각 문항을 선택하면 자동 저장됩니다. 슬라이더는 움직여야 응답으로 인정됩니다.')

    for idx, q in enumerate(QUESTIONS):
        st.markdown(f'<div class="question-card"><h3>Q{idx+1}. {q["title"]}</h3></div>', unsafe_allow_html=True)
        key = f'q_{idx}'
        if q['kind'] == 'radio':
            # index=None으로 시작하여 응답하지 않은 질문을 구분
            choice = st.radio('답변 선택', q['options'], index=None, key=key, label_visibility='collapsed')
            if choice is not None:
                st.session_state.answers[idx] = q['options'].index(choice)
            else:
                st.session_state.answers.pop(idx, None)
        else:
            # Streamlit slider에는 미선택 상태가 없으므로 체크박스로 응답 여부를 구분
            enabled = st.checkbox('이 문항에 응답하기', key=f'enabled_{idx}', value=False)
            value = st.slider('성향 강도', 1, 5, 3, key=key, disabled=not enabled,
                              help='1: 왼쪽에 매우 가까움 / 3: 중립 / 5: 오른쪽에 매우 가까움')
            st.caption(f'**1** · {q["left"]}　↔　{q["right"]} · **5**')
            if enabled:
                st.session_state.answers[idx] = value
            else:
                st.session_state.answers.pop(idx, None)

    # 마지막 문항의 변경도 이 실행에서 계산되도록 실제 답변 상태를 사용
    completed = len(st.session_state.answers)
    st.progress(completed / len(QUESTIONS))
    st.caption(f'{completed} / {len(QUESTIONS)}문항 완료')
    if st.button('✨ 내 성향 결과 확인하기', type='primary', use_container_width=True,
                 disabled=completed != len(QUESTIONS)):
        st.session_state.show_result = True
        st.rerun()
else:
    code, scores = calculate_result(st.session_state.answers)
    name, description = RESULTS[code]
    st.markdown(f'<div class="result-card"><div class="result-code">{code}</div><h2>{name}</h2><p>{description}</p></div>', unsafe_allow_html=True)
    st.subheader('📊 나의 4가지 성향')

    # 각 축에서 양쪽 성향의 점수를 합계 100%로 환산하여 시각화
    labels, left_values, right_values, hover_left, hover_right = [], [], [], [], []
    for a, b, axis_name, a_name, b_name in AXES:
        total = scores[a] + scores[b]
        left_pct = round(100 * scores[a] / total) if total else 50
        labels.append(axis_name)
        left_values.append(left_pct)
        right_values.append(100 - left_pct)
        hover_left.append(f'{a} · {a_name}')
        hover_right.append(f'{b} · {b_name}')

    fig = go.Figure()
    fig.add_trace(go.Bar(name='첫 번째 성향 (N/S/B/I)', y=labels, x=left_values,
                         orientation='h', marker_color='#9567e8',
                         text=[f'{v}%' for v in left_values], textposition='inside',
                         customdata=hover_left, hovertemplate='%{customdata}: %{x}%<extra></extra>'))
    fig.add_trace(go.Bar(name='반대 성향 (Q/M/D/C)', y=labels, x=right_values,
                         orientation='h', marker_color='#d9c8f7',
                         text=[f'{v}%' for v in right_values], textposition='inside',
                         customdata=hover_right, hovertemplate='%{customdata}: %{x}%<extra></extra>'))
    fig.update_layout(barmode='stack', xaxis=dict(range=[0, 100], ticksuffix='%'),
                      yaxis=dict(autorange='reversed'), height=360,
                      margin=dict(l=10, r=10, t=20, b=10),
                      legend=dict(orientation='h', y=-0.25),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.caption('점수는 이 테스트의 응답을 기준으로 산출한 상대적 선호도이며, 심리학적 진단 결과가 아닙니다. 동점은 N/S/B/I로 분류합니다.')
    if st.button('🔄 다시 검사하기', use_container_width=True):
        reset_test()
        # 슬라이더 응답 활성화 체크박스도 초기화
        for idx, q in enumerate(QUESTIONS):
            if q['kind'] == 'slider':
                st.session_state.pop(f'enabled_{idx}', None)
        st.rerun()

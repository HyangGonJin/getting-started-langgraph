"""
가장 기본적인 LangGraph Agent 예제

이 예제는 LangGraph의 핵심 개념을 보여줍니다:
1. State (상태) - Agent가 유지하는 데이터
2. Node (노드) - 실행할 함수들
3. Graph (그래프) - 노드들의 흐름을 정의
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END, START


# 1. State 정의: Agent가 대화 중 유지할 상태
class AgentState(TypedDict):
    """Agent의 상태를 정의하는 클래스

    Attributes:
        messages: 대화 메시지 리스트 (딕셔너리 형태)
        user_name: 사용자 이름
        step_count: 실행된 단계 수
    """
    messages: list
    user_name: str
    step_count: int


# 2. Node 함수들 정의: 각 단계에서 실행될 함수
def greet_user(state: AgentState) -> AgentState:
    """사용자를 환영하는 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태
    """
    user_name = state.get("user_name", "사용자")
    greeting = f"안녕하세요, {user_name}님! LangGraph Agent입니다."

    print(f"[Greet Node] {greeting}")

    return {
        "messages": [{"role": "assistant", "content": greeting}],
        "step_count": state.get("step_count", 0) + 1
    }


def process_input(state: AgentState) -> AgentState:
    """사용자 입력을 처리하는 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태
    """
    messages = state.get("messages", [])
    last_message = messages[-1]["content"] if messages else ""

    response = f"'{last_message}'를 처리했습니다. 단계: {state.get('step_count', 0) + 1}"
    print(f"[Process Node] {response}")

    return {
        "messages": [{"role": "assistant", "content": response}],
        "step_count": state.get("step_count", 0) + 1
    }


def summarize(state: AgentState) -> AgentState:
    """대화를 요약하는 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태
    """
    step_count = state.get("step_count", 0)
    message_count = len(state.get("messages", []))

    summary = f"총 {step_count}단계를 실행했고, {message_count}개의 메시지가 있습니다."
    print(f"[Summary Node] {summary}")

    return {
        "messages": [{"role": "assistant", "content": summary}],
        "step_count": step_count + 1
    }


# 3. Graph 구성: 노드들을 연결
def create_basic_agent() -> StateGraph:
    """기본 Agent 그래프를 생성

    Returns:
        컴파일된 StateGraph
    """
    # StateGraph 생성
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("greet", greet_user)
    workflow.add_node("process", process_input)
    workflow.add_node("summarize", summarize)

    # 엣지(흐름) 정의
    workflow.add_edge(START, "greet")        # 시작 -> greet
    workflow.add_edge("greet", "process")    # greet -> process
    workflow.add_edge("process", "summarize") # process -> summarize
    workflow.add_edge("summarize", END)      # summarize -> 종료

    # 그래프 컴파일
    app = workflow.compile()

    return app


# 4. 실행 함수
def run_basic_agent(user_name: str = "테스터", user_input: str = "안녕하세요!") -> dict:
    """Agent를 실행하는 함수

    Args:
        user_name: 사용자 이름
        user_input: 사용자 입력 메시지

    Returns:
        최종 상태
    """
    print("\n" + "="*60)
    print("LangGraph 기본 Agent 실행")
    print("="*60 + "\n")

    # Agent 생성
    app = create_basic_agent()

    # 초기 상태 설정
    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "user_name": user_name,
        "step_count": 0
    }

    # Agent 실행
    final_state = app.invoke(initial_state)

    print("\n" + "="*60)
    print("실행 완료!")
    print("="*60 + "\n")

    return final_state


if __name__ == "__main__":
    
    # 예제 1: 그래프 구조 시각화
    print("\n" + "🎨"*30)
    print("예제 1: 그래프 구조 시각화")
    print("🎨"*30 + "\n")

    app = create_basic_agent()

    # 방법 2: Mermaid 다이어그램 (온라인/IDE에서 시각화 가능)
    print("\n[시각화] Mermaid 다이어그램:")
    print("-" * 60)
    try:
        from utils.visualization import print_mermaid_diagram
        print_mermaid_diagram(app)
    except ImportError:
        pass

    # 예제 2: Agent 실행
    print("\n" + "🤖"*30)
    print("예제 2: Agent 실행")
    print("🤖"*30 + "\n")

    result = run_basic_agent(
        user_name="홍길동",
        user_input="LangGraph를 배우고 싶습니다!"
    )

    print("\n[최종 상태]")
    print(f"총 단계 수: {result['step_count']}")
    print(f"메시지 수: {len(result['messages'])}")
    print("\n[모든 메시지]")
    for i, msg in enumerate(result['messages'], 1):
        print(f"{i}. [{msg['role']}] {msg['content']}")

    # # 예제 3: 그래프를 파일로 저장
    # print("\n" + "💾"*30)
    # print("예제 3: 그래프를 파일로 저장")
    # print("💾"*30 + "\n")
    #
    # try:
    #     from utils.visualization import save_mermaid_diagram
    #     save_mermaid_diagram(app, "reports/basic_agent_graph.md")
    #     print("✅ reports/basic_agent_graph.md 파일을 확인해보세요!")
    # except ImportError:
    #     print("시각화 유틸리티를 사용할 수 없습니다.")

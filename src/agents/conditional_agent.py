"""
조건부 분기를 사용하는 LangGraph Agent 예제

이 예제는 다음 개념을 보여줍니다:
1. Conditional Edge - 조건에 따라 다른 노드로 분기
2. 동적 흐름 제어
3. 다양한 처리 경로
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END, START


# State 정의
class ConditionalState(TypedDict):
    """조건부 Agent 상태

    Attributes:
        message: 사용자 메시지
        message_type: 메시지 타입 (greeting, question, command, unknown)
        response: Agent 응답
        processed: 처리 완료 여부
    """
    message: str
    message_type: str
    response: str
    processed: bool


# Node 함수들
def classify_message(state: ConditionalState) -> ConditionalState:
    """메시지 타입을 분류하는 노드

    Args:
        state: 현재 상태

    Returns:
        업데이트된 상태 (message_type이 설정됨)
    """
    message = state["message"].lower()

    # 간단한 규칙 기반 분류
    if any(greeting in message for greeting in ["안녕", "hello", "hi", "헬로"]):
        message_type = "greeting"
    elif any(q in message for q in ["?", "뭐", "무엇", "어떻게", "왜", "언제"]):
        message_type = "question"
    elif any(cmd in message for cmd in ["해줘", "실행", "시작", "멈춰", "중지"]):
        message_type = "command"
    else:
        message_type = "unknown"

    print(f"[Classify Node] 메시지 타입: {message_type}")

    return {
        "message_type": message_type
    }


def handle_greeting(state: ConditionalState) -> ConditionalState:
    """인사 메시지를 처리하는 노드

    Args:
        state: 현재 상태

    Returns:
        업데이트된 상태
    """
    response = "안녕하세요! 무엇을 도와드릴까요?"
    print(f"[Greeting Handler] {response}")

    return {
        "response": response,
        "processed": True
    }


def handle_question(state: ConditionalState) -> ConditionalState:
    """질문을 처리하는 노드

    Args:
        state: 현재 상태

    Returns:
        업데이트된 상태
    """
    response = f"'{state['message']}'에 대한 답변을 찾고 있습니다..."
    print(f"[Question Handler] {response}")

    return {
        "response": response,
        "processed": True
    }


def handle_command(state: ConditionalState) -> ConditionalState:
    """명령을 처리하는 노드

    Args:
        state: 현재 상태

    Returns:
        업데이트된 상태
    """
    response = f"명령을 실행합니다: {state['message']}"
    print(f"[Command Handler] {response}")

    return {
        "response": response,
        "processed": True
    }


def handle_unknown(state: ConditionalState) -> ConditionalState:
    """알 수 없는 메시지를 처리하는 노드

    Args:
        state: 현재 상태

    Returns:
        업데이트된 상태
    """
    response = "죄송합니다. 이해하지 못했습니다. 다시 말씀해 주시겠어요?"
    print(f"[Unknown Handler] {response}")

    return {
        "response": response,
        "processed": True
    }


# Conditional Edge 함수
def route_message(state: ConditionalState) -> Literal["greeting", "question", "command", "unknown"]:
    """메시지 타입에 따라 다음 노드를 결정하는 함수

    Args:
        state: 현재 상태

    Returns:
        다음에 실행할 노드 이름
    """
    message_type = state["message_type"]
    print(f"[Router] {message_type} 핸들러로 라우팅")
    return message_type


# Graph 구성
def create_conditional_agent() -> StateGraph:
    """조건부 분기를 가진 Agent 생성

    Returns:
        컴파일된 StateGraph
    """
    workflow = StateGraph(ConditionalState)

    # 노드 추가
    workflow.add_node("classify", classify_message)
    workflow.add_node("greeting", handle_greeting)
    workflow.add_node("question", handle_question)
    workflow.add_node("command", handle_command)
    workflow.add_node("unknown", handle_unknown)

    # 엣지 정의
    workflow.add_edge(START, "classify")

    # 조건부 엣지: classify 노드 후 message_type에 따라 분기
    workflow.add_conditional_edges(
        "classify",
        route_message,
        {
            "greeting": "greeting",
            "question": "question",
            "command": "command",
            "unknown": "unknown"
        }
    )

    # 모든 핸들러는 END로 이동
    workflow.add_edge("greeting", END)
    workflow.add_edge("question", END)
    workflow.add_edge("command", END)
    workflow.add_edge("unknown", END)

    return workflow.compile()


# 실행 함수
def run_conditional_agent(message: str) -> dict:
    """조건부 Agent 실행

    Args:
        message: 사용자 메시지

    Returns:
        최종 상태
    """
    print("\n" + "="*60)
    print("조건부 분기 Agent 실행")
    print("="*60 + "\n")

    app = create_conditional_agent()

    initial_state = {
        "message": message,
        "message_type": "",
        "response": "",
        "processed": False
    }

    final_state = app.invoke(initial_state)

    print("\n" + "="*60)
    print("실행 완료!")
    print("="*60 + "\n")

    return final_state


if __name__ == "__main__":
    # 여러 타입의 메시지 테스트
    test_messages = [
        "안녕하세요!",
        "LangGraph가 뭐예요?",
        "데이터 분석 실행해줘",
        "오늘 날씨 좋네요"
    ]

    for msg in test_messages:
        print(f"\n입력 메시지: '{msg}'")
        result = run_conditional_agent(msg)
        print(f"응답: {result['response']}")
        print(f"처리됨: {result['processed']}")
        print("-" * 60)

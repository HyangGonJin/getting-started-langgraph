"""
LLM을 사용하는 LangGraph Agent 예제

이 예제는 다음을 보여줍니다:
1. OpenAI API를 Agent에 통합
2. 실제 AI 모델과의 상호작용
3. 메시지 히스토리 관리

사용 전 준비:
1. OpenAI API 키 필요: https://platform.openai.com/api-keys
2. .env 파일에 OPENAI_API_KEY=your-key-here 추가
3. 또는 환경변수로 export OPENAI_API_KEY=your-key-here
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


# State 정의
class ChatState(TypedDict):
    """채팅 Agent 상태

    Attributes:
        messages: 대화 메시지 리스트
        model_name: 사용할 모델 이름
    """
    messages: Annotated[list, add_messages]
    model_name: str


def create_llm_node(model_name: str = "gpt-3.5-turbo"):
    """LLM을 호출하는 노드를 생성하는 팩토리 함수

    Args:
        model_name: OpenAI 모델 이름

    Returns:
        LLM 노드 함수
    """
    def call_llm(state: ChatState) -> ChatState:
        """LLM을 호출하여 응답을 생성하는 노드

        Args:
            state: 현재 상태

        Returns:
            업데이트된 상태
        """
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("[Warning] OPENAI_API_KEY가 설정되지 않았습니다.")
            return {
                "messages": [AIMessage(content="OpenAI API 키가 필요합니다. .env 파일에 설정해주세요.")]
            }

        # LLM 초기화
        llm = ChatOpenAI(
            model=state.get("model_name", model_name),
            temperature=0.7,
            api_key=api_key
        )

        print(f"[LLM Node] {model_name} 모델 호출 중...")

        # 메시지 변환
        messages = state["messages"]

        # LLM 호출
        response = llm.invoke(messages)

        print(f"[LLM Node] 응답 생성 완료")

        return {
            "messages": [response]
        }

    return call_llm


def create_llm_agent(model_name: str = "gpt-3.5-turbo") -> StateGraph:
    """LLM을 사용하는 간단한 채팅 Agent 생성

    Args:
        model_name: 사용할 OpenAI 모델

    Returns:
        컴파일된 StateGraph
    """
    workflow = StateGraph(ChatState)

    # LLM 노드 추가
    workflow.add_node("llm", create_llm_node(model_name))

    # 간단한 흐름: START -> LLM -> END
    workflow.add_edge(START, "llm")
    workflow.add_edge("llm", END)

    return workflow.compile()


def run_llm_agent(user_message: str, model_name: str = "gpt-3.5-turbo") -> dict:
    """LLM Agent를 실행하는 함수

    Args:
        user_message: 사용자 메시지
        model_name: 사용할 모델 이름

    Returns:
        최종 상태
    """
    print("\n" + "="*60)
    print(f"LLM Agent 실행 (모델: {model_name})")
    print("="*60 + "\n")

    app = create_llm_agent(model_name)

    initial_state = {
        "messages": [HumanMessage(content=user_message)],
        "model_name": model_name
    }

    final_state = app.invoke(initial_state)

    print("\n" + "="*60)
    print("실행 완료!")
    print("="*60 + "\n")

    return final_state


def run_conversation(model_name: str = "gpt-3.5-turbo"):
    """대화형 모드로 Agent 실행

    Args:
        model_name: 사용할 모델 이름
    """
    print("\n" + "="*60)
    print("LangGraph 채팅 Agent (대화형 모드)")
    print("종료하려면 'quit' 또는 'exit' 입력")
    print("="*60 + "\n")

    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
        print("\n설정 방법:")
        print("1. .env 파일 생성: echo 'OPENAI_API_KEY=your-key-here' > .env")
        print("2. 또는 환경변수 설정: export OPENAI_API_KEY=your-key-here")
        print("\nAPI 키는 https://platform.openai.com/api-keys 에서 발급받으세요.\n")
        return

    app = create_llm_agent(model_name)
    conversation_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "종료"]:
            print("대화를 종료합니다.")
            break

        if not user_input:
            continue

        # 대화 히스토리에 추가
        conversation_history.append(HumanMessage(content=user_input))

        # Agent 실행
        state = {
            "messages": conversation_history,
            "model_name": model_name
        }

        result = app.invoke(state)

        # AI 응답 추출
        ai_response = result["messages"][-1]
        conversation_history = result["messages"]

        print(f"Agent: {ai_response.content}\n")


if __name__ == "__main__":
    # 예제 1: 단일 질문
    print("\n### 예제 1: 단일 질문 ###")
    result = run_llm_agent(
        "LangGraph가 무엇인지 한 문장으로 설명해주세요.",
        model_name="gpt-3.5-turbo"
    )

    if result["messages"]:
        print(f"사용자: {result['messages'][0].content}")
        if len(result["messages"]) > 1:
            print(f"Agent: {result['messages'][-1].content}")

    # 예제 2: 대화형 모드 (주석 해제하여 사용)
    # print("\n### 예제 2: 대화형 모드 ###")
    # run_conversation(model_name="gpt-3.5-turbo")

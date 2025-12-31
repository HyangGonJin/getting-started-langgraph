"""
LangGraph Agent 튜토리얼 - 메인 실행 스크립트

이 스크립트는 모든 예제를 순서대로 실행합니다.

사용법:
    python src/main.py                    # 모든 예제 실행
    python src/main.py --example basic    # 기본 예제만 실행
    python src/main.py --example conditional  # 조건부 예제만 실행
    python src/main.py --example llm      # LLM 예제만 실행
"""

import argparse
from agents.basic_agent import run_basic_agent
from agents.conditional_agent import run_conditional_agent
from agents.llm_agent import run_llm_agent, run_conversation


def run_all_examples():
    """모든 예제를 순서대로 실행"""

    print("\n" + "="*70)
    print(" LangGraph Agent 튜토리얼 - 전체 예제 ")
    print("="*70)

    # 1. 기본 Agent
    print("\n\n" + "🔹"*35)
    print("1️⃣  기본 Agent 예제")
    print("🔹"*35 + "\n")
    print("설명: 가장 기본적인 LangGraph 구조를 보여줍니다.")
    print("     - State 정의")
    print("     - Node 함수들")
    print("     - Graph 연결\n")

    input("Press Enter to run...")
    run_basic_agent(user_name="튜토리얼 사용자", user_input="LangGraph 배우기!")

    # 2. 조건부 분기 Agent
    print("\n\n" + "🔹"*35)
    print("2️⃣  조건부 분기 Agent 예제")
    print("🔹"*35 + "\n")
    print("설명: 조건에 따라 다른 처리 경로를 선택합니다.")
    print("     - Conditional Edge")
    print("     - 동적 라우팅")
    print("     - 다양한 핸들러\n")

    input("Press Enter to run...")
    test_messages = [
        "안녕하세요!",
        "LangGraph가 뭐예요?",
        "데이터 분석 실행해줘"
    ]

    for msg in test_messages:
        print(f"\n📝 테스트 메시지: '{msg}'")
        result = run_conditional_agent(msg)
        print(f"✅ 응답: {result['response']}\n")
        print("-" * 60)

    # 3. LLM Agent
    print("\n\n" + "🔹"*35)
    print("3️⃣  LLM Agent 예제")
    print("🔹"*35 + "\n")
    print("설명: 실제 AI 모델(OpenAI)과 통합된 Agent입니다.")
    print("     - OpenAI API 사용")
    print("     - 대화 히스토리 관리")
    print("     - 실시간 AI 응답\n")
    print("⚠️  주의: OpenAI API 키가 필요합니다!")
    print("   .env 파일에 OPENAI_API_KEY를 설정해주세요.\n")

    choice = input("LLM 예제를 실행하시겠습니까? (y/n): ").lower()
    if choice == 'y':
        run_llm_agent("LangGraph를 사용하는 이유를 3가지만 말해주세요.")

    print("\n\n" + "="*70)
    print(" 모든 예제 실행 완료! ")
    print("="*70 + "\n")

    print("다음 단계:")
    print("1. src/agents/ 폴더의 코드를 읽어보세요")
    print("2. 각 파일을 개별적으로 실행해보세요:")
    print("   - python src/agents/basic_agent.py")
    print("   - python src/agents/conditional_agent.py")
    print("   - python src/agents/llm_agent.py")
    print("3. 코드를 수정하며 실험해보세요!")
    print()


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="LangGraph Agent 튜토리얼"
    )
    parser.add_argument(
        "--example",
        choices=["basic", "conditional", "llm", "all"],
        default="all",
        help="실행할 예제 선택"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="대화형 모드로 LLM Agent 실행"
    )

    args = parser.parse_args()

    if args.interactive:
        run_conversation()
        return

    if args.example == "basic":
        run_basic_agent()
    elif args.example == "conditional":
        test_msgs = ["안녕하세요!", "LangGraph가 뭐예요?", "분석 실행해줘"]
        for msg in test_msgs:
            run_conditional_agent(msg)
    elif args.example == "llm":
        run_llm_agent("LangGraph에 대해 설명해주세요.")
    else:
        run_all_examples()


if __name__ == "__main__":
    main()

"""
모든 Agent 그래프를 시각화하는 스크립트

이 스크립트는 프로젝트의 모든 Agent 그래프를 다양한 형식으로 시각화합니다.

사용법:
    python src/visualize_graphs.py                 # 모든 그래프 시각화
    python src/visualize_graphs.py --agent basic   # 특정 Agent만
    python src/visualize_graphs.py --format ascii  # 특정 포맷만
"""

import argparse
from pathlib import Path

# Agent import
from agents.basic_agent import create_basic_agent
from agents.conditional_agent import create_conditional_agent
from agents.llm_agent import create_llm_agent

# Visualization import
from utils.visualization import (
    print_mermaid_diagram,
    save_mermaid_diagram,
    save_png_diagram,
    visualize_graph
)


def visualize_all_agents(output_dir: str = "reports", save_files: bool = True):
    """모든 Agent의 그래프를 시각화

    Args:
        output_dir: 파일 저장 디렉토리
        save_files: 파일로 저장할지 여부
    """
    print("\n" + "="*70)
    print(" 🎨 LangGraph Agent 시각화 도구 🎨 ")
    print("="*70 + "\n")

    agents = {
        "basic": {
            "name": "기본 Agent",
            "create_fn": create_basic_agent,
            "description": "순차적으로 실행되는 가장 간단한 그래프"
        },
        "conditional": {
            "name": "조건부 분기 Agent",
            "create_fn": create_conditional_agent,
            "description": "메시지 타입에 따라 분기하는 그래프"
        },
        "llm": {
            "name": "LLM Agent",
            "create_fn": create_llm_agent,
            "description": "OpenAI API를 사용하는 채팅 그래프"
        }
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for agent_key, agent_info in agents.items():
        print("\n" + "🔹"*35)
        print(f"Agent: {agent_info['name']}")
        print(f"설명: {agent_info['description']}")
        print("🔹"*35 + "\n")

        # Agent 생성
        app = agent_info["create_fn"]()

        # 2. Mermaid 다이어그램 출력
        print_mermaid_diagram(app)

        # 3. 파일로 저장
        if save_files:
            mermaid_path = output_path / f"{agent_key}_agent_graph.md"
            save_mermaid_diagram(app, str(mermaid_path))

            # PNG도 시도 (pygraphviz가 있으면)
            png_path = output_path / f"{agent_key}_agent_graph.png"
            save_png_diagram(app, str(png_path))

        print("\n")

    print("\n" + "="*70)
    print(" ✅ 모든 그래프 시각화 완료! ")
    print("="*70 + "\n")

    if save_files:
        print(f"📁 저장 위치: {output_dir}/")
        print(f"   - *_agent_graph.md (Mermaid 다이어그램)")
        print(f"   - *_agent_graph.png (PNG 이미지, pygraphviz 설치 시)")
        print()


def visualize_single_agent(
    agent_name: str,
    output_dir: str = "reports",
    format_type: str = "all"
):
    """단일 Agent의 그래프를 시각화

    Args:
        agent_name: Agent 이름 (basic, conditional, llm)
        output_dir: 파일 저장 디렉토리
        format_type: 출력 포맷 (ascii, mermaid, png, all)
    """
    agents_map = {
        "basic": ("기본 Agent", create_basic_agent),
        "conditional": ("조건부 분기 Agent", create_conditional_agent),
        "llm": ("LLM Agent", create_llm_agent)
    }

    if agent_name not in agents_map:
        print(f"❌ 잘못된 Agent 이름: {agent_name}")
        print(f"사용 가능한 Agent: {', '.join(agents_map.keys())}")
        return

    agent_title, create_fn = agents_map[agent_name]

    print("\n" + "="*70)
    print(f" 🎨 {agent_title} 시각화 🎨 ")
    print("="*70 + "\n")

    app = create_fn()

    if format_type in ["mermaid", "all"]:
        print_mermaid_diagram(app)
        save_mermaid_diagram(app, f"{output_dir}/{agent_name}_graph.md")

    if format_type in ["png", "all"]:
        save_png_diagram(app, f"{output_dir}/{agent_name}_graph.png")

    print("\n" + "="*70)
    print(" ✅ 시각화 완료! ")
    print("="*70 + "\n")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="LangGraph Agent 시각화 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 모든 Agent 시각화
  python src/visualize_graphs.py

  # 특정 Agent만 시각화
  python src/visualize_graphs.py --agent basic

  # 특정 포맷으로만 출력
  python src/visualize_graphs.py --format ascii

  # 파일 저장 없이 출력만
  python src/visualize_graphs.py --no-save
        """
    )

    parser.add_argument(
        "--agent",
        choices=["basic", "conditional", "llm", "all"],
        default="all",
        help="시각화할 Agent 선택"
    )

    parser.add_argument(
        "--format",
        choices=["mermaid", "png", "all"],
        default="all",
        help="출력 포맷 선택"
    )

    parser.add_argument(
        "--output-dir",
        default="reports",
        help="파일 저장 디렉토리"
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="파일로 저장하지 않고 출력만"
    )

    args = parser.parse_args()

    save_files = not args.no_save

    if args.agent == "all":
        visualize_all_agents(args.output_dir, save_files)
    else:
        visualize_single_agent(args.agent, args.output_dir, args.format)


if __name__ == "__main__":
    main()

"""
LangGraph 그래프 시각화 유틸리티

이 모듈은 compile된 LangGraph를 다양한 방법으로 시각화합니다:
2. Mermaid 다이어그램 - 텍스트 형식 (온라인/IDE에서 렌더링 가능)
3. PNG 이미지 - 파일로 저장 (pygraphviz 설치 필요)
"""

from typing import Optional
from pathlib import Path


def get_mermaid_diagram(app) -> str:
    """그래프를 Mermaid 다이어그램 텍스트로 반환

    Mermaid는 텍스트로 다이어그램을 그리는 도구입니다.
    생성된 텍스트는:
    - GitHub/GitLab 마크다운에서 자동 렌더링됨
    - https://mermaid.live 에서 온라인으로 렌더링 가능
    - VS Code의 Mermaid 확장으로 렌더링 가능

    Args:
        app: compile된 LangGraph 앱

    Returns:
        Mermaid 다이어그램 텍스트

    Example:
        >>> app = create_basic_agent()
        >>> diagram = get_mermaid_diagram(app)
        >>> print(diagram)
    """
    try:
        graph = app.get_graph()
        mermaid_code = graph.draw_mermaid()
        return mermaid_code
    except Exception as e:
        return f"Mermaid 다이어그램 생성 실패: {e}"


def print_mermaid_diagram(app) -> None:
    """그래프를 Mermaid 다이어그램으로 출력

    Args:
        app: compile된 LangGraph 앱

    Example:
        >>> app = create_basic_agent()
        >>> print_mermaid_diagram(app)
    """
    print("\n" + "="*60)
    print("Graph Structure (Mermaid)")
    print("="*60 + "\n")

    mermaid_code = get_mermaid_diagram(app)
    print(mermaid_code)

    print("\n" + "-"*60)
    print("💡 이 다이어그램을 시각화하는 방법:")
    print("1. https://mermaid.live 에 복사 붙여넣기")
    print("2. VS Code에서 Mermaid 확장 설치 후 미리보기")
    print("3. GitHub/GitLab 마크다운 파일에 포함")
    print("-"*60 + "\n")


def save_mermaid_diagram(app, output_path: str = "graph_diagram.md") -> None:
    """그래프를 Mermaid 다이어그램 파일로 저장

    Args:
        app: compile된 LangGraph 앱
        output_path: 저장할 파일 경로 (.md 확장자 권장)

    Example:
        >>> app = create_basic_agent()
        >>> save_mermaid_diagram(app, "reports/my_graph.md")
    """
    mermaid_code = get_mermaid_diagram(app)

    # 마크다운 형식으로 저장
    content = f"""# LangGraph Diagram

```mermaid
{mermaid_code}
```

## 시각화 방법

1. **GitHub/GitLab**: 이 파일을 그대로 커밋하면 자동으로 렌더링됩니다.
2. **VS Code**: Mermaid 확장을 설치하고 미리보기를 엽니다.
3. **온라인**: https://mermaid.live 에 위 코드를 복사합니다.
"""

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")

    print(f"✅ Mermaid 다이어그램 저장 완료: {output_path}")


def save_png_diagram(app, output_path: str = "graph_diagram.png") -> None:
    """그래프를 PNG 이미지로 저장

    주의: 이 기능을 사용하려면 pygraphviz 설치가 필요합니다.

    설치 방법:
    - Mac: brew install graphviz && pip install pygraphviz
    - Ubuntu: sudo apt-get install graphviz graphviz-dev && pip install pygraphviz
    - Windows: https://graphviz.org/download/ 에서 설치 후 pip install pygraphviz

    Args:
        app: compile된 LangGraph 앱
        output_path: 저장할 파일 경로 (.png)

    Example:
        >>> app = create_basic_agent()
        >>> save_png_diagram(app, "reports/my_graph.png")
    """
    try:
        graph = app.get_graph()
        png_data = graph.draw_mermaid_png()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_bytes(png_data)

        print(f"✅ PNG 이미지 저장 완료: {output_path}")

    except ImportError:
        print("❌ pygraphviz가 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("  Mac:     brew install graphviz && pip install pygraphviz")
        print("  Ubuntu:  sudo apt-get install graphviz graphviz-dev && pip install pygraphviz")
        print("  Windows: https://graphviz.org/download/ 설치 후 pip install pygraphviz")
        print("\n또는 Mermaid 다이어그램을 사용하세요 (save_mermaid_diagram)")

    except Exception as e:
        print(f"❌ PNG 저장 실패: {e}")


def visualize_graph(
    app,
    method: str = "all",
    output_dir: str = "reports"
) -> None:
    """그래프를 여러 방법으로 시각화

    Args:
        app: compile된 LangGraph 앱
        method: 시각화 방법
            - "mermaid": Mermaid 다이어그램만
            - "png": PNG 이미지만
            - "all": 모든 방법 (기본값)
        output_dir: 파일 저장 디렉토리

    Example:
        >>> app = create_basic_agent()
        >>> visualize_graph(app, method="all")
    """
    print("\n" + "🎨"*30)
    print("LangGraph 시각화")
    print("🎨"*30 + "\n")

    if method in ["mermaid", "all"]:
        print_mermaid_diagram(app)

        # 파일로도 저장
        output_path = Path(output_dir) / "graph_mermaid.md"
        save_mermaid_diagram(app, str(output_path))

    if method in ["png", "all"]:
        output_path = Path(output_dir) / "graph_diagram.png"
        save_png_diagram(app, str(output_path))

    print("\n" + "🎨"*30)
    print("시각화 완료!")
    print("🎨"*30 + "\n")


if __name__ == "__main__":
    # 테스트 코드
    print("시각화 유틸리티를 테스트하려면 다음과 같이 사용하세요:\n")
    print("from agents.basic_agent import create_basic_agent")
    print("from utils.visualization import visualize_graph")
    print()
    print("app = create_basic_agent()")
    print("visualize_graph(app)")

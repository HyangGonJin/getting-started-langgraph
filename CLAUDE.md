# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview
- **Purpose**: [Describe your data science project - e.g., customer churn prediction, data analysis pipeline, ML model training]
- **Tech Stack**: Python 3.x, [key libraries: pandas, numpy, scikit-learn, pytorch, tensorflow, etc.]
- **Data Location**: `data/raw/` for original data, `data/processed/` for cleaned data

## Development Setup

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# For development tools
pip install -r requirements-dev.txt
```

### Key Commands
- **Run main script**: `python src/main.py`
- **Run tests**: `pytest tests/ -v`
- **Lint code**: `flake8 src/ tests/ --max-line-length=100`
- **Format code**: `black src/ tests/`
- **Type checking**: `mypy src/`
- **Run Jupyter**: `jupyter notebook notebooks/`
- **Generate reports**: `python src/reports/generate_report.py`

## Project Structure
```
├── data/
│   ├── raw/          # Original, immutable data (never commit large files)
│   ├── processed/    # Cleaned, transformed data
│   ├── external/     # Third-party data sources
│   └── README.md     # Data documentation and sources
├── notebooks/        # Jupyter notebooks for exploration
│   ├── exploratory/  # Initial data exploration
│   └── analysis/     # Final analysis notebooks
├── src/              # Source code (production-ready)
│   ├── data/         # Data loading and processing
│   ├── features/     # Feature engineering
│   ├── models/       # Model training and evaluation
│   ├── visualization/# Plotting and visualization
│   └── utils/        # Utility functions and helpers
├── tests/            # Unit and integration tests
│   └── fixtures/     # Small sample data for testing
├── models/           # Trained model artifacts (.pkl, .h5, etc.)
├── reports/          # Generated analysis reports and figures
├── config/           # Configuration files
├── requirements.txt  # Production dependencies
└── requirements-dev.txt  # Development dependencies
```

## Code Conventions

### Python Style
- Follow PEP 8 with 100-character line limit
- Use type hints for all function signatures
- Use Google-style docstrings for all functions and classes
- Example:
```python
def process_data(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Process the input dataframe by selecting and cleaning columns.

    Args:
        df: Input dataframe to process
        columns: List of column names to keep

    Returns:
        Processed dataframe with selected columns
    """
    pass
```

### Data Science Specific Guidelines
- **Reproducibility**: Always set random seeds (`RANDOM_STATE = 42` as constant)
- **Data Versioning**: Never commit large data files (>10MB); document data sources in `data/README.md`
- **Notebooks**:
  - Use for exploration only; refactor production code to `src/`
  - Name with numbers: `01_data_exploration.ipynb`, `02_feature_engineering.ipynb`
  - Clear outputs before committing: `jupyter nbconvert --clear-output --inplace notebook.ipynb`
- **Experiments**: Log all experiments (consider MLflow, Weights & Biases, or simple CSV logs)

### Naming Conventions
- **Files/modules**: `snake_case.py`
- **Notebooks**: `01_descriptive_name.ipynb` (numbered for execution order)
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

## Data Handling

### What NOT to Commit
- Raw data files (>10MB)
- Processed data files (>10MB)
- Model artifacts (>50MB) - use Git LFS or external storage
- API keys, credentials, tokens
- Personal/sensitive information

### What to ALWAYS Commit
- Data processing scripts
- Data documentation (`data/README.md`)
- Sample/fixture data for tests (<1MB)
- Model training scripts
- Configuration files (with sensitive values in `.env`)

### Data Loading Pattern
```python
# Use centralized data loading from src/data/load_data.py
from src.data.load_data import load_raw_data, load_processed_data

df = load_raw_data("dataset_name")
```

### Data Validation
- Use schemas to validate data (pandera, great_expectations, pydantic)
- Define schemas in `src/data/schemas.py`
- Validate early in the pipeline

## Model Development Workflow

1. **Explore** in `notebooks/exploratory/`
2. **Prototype** feature engineering and models
3. **Refactor** working code to `src/` modules
4. **Test** by adding unit tests in `tests/`
5. **Document** with docstrings and update README
6. **Log** experiments and track metrics
7. **Version** successful models

## Testing Guidelines
- Write unit tests for data processing functions
- Test feature engineering logic
- Use small sample datasets in `tests/fixtures/`
- Mock external API calls and file I/O
- Aim for >80% coverage on `src/` code
- Run tests before committing: `pytest tests/ -v`

## Dependencies Management
- **Production**: `requirements.txt` (pinned versions)
- **Development**: `requirements-dev.txt` (testing, linting, formatting tools)
- Update after adding packages: `pip freeze > requirements.txt`
- Use virtual environments to avoid conflicts

## Configuration
- Store config in `config/config.yaml` or environment variables
- Load using `src/config.py`
- Never hardcode paths - use `pathlib.Path`
- Example:
```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
```

## Common Patterns in This Codebase

### Logging
```python
from src.utils.logger import get_logger
logger = get_logger(__name__)
logger.info("Processing started")
```

### Error Handling
- Use custom exceptions defined in `src/exceptions.py`
- Log errors before raising
- Provide helpful error messages

### Constants
- Define in `src/constants.py`
- Use for random seeds, column names, file paths

## Machine Learning Specific

### Experiment Tracking
- Log: hyperparameters, metrics, artifacts
- Use consistent metric names
- Save model metadata with artifacts

### Model Serialization
```python
# Use joblib for sklearn models
import joblib
joblib.dump(model, 'models/model_v1.pkl')

# Use appropriate format for deep learning (PyTorch, TensorFlow)
```

### Model Evaluation
- Always evaluate on held-out test set
- Report multiple metrics (accuracy, precision, recall, F1, etc.)
- Save evaluation reports in `reports/`

## Notes for Claude Code

When working with this repository:
- Start explorations in notebooks, then refactor to `src/` for production
- Always include type hints and Google-style docstrings
- Add unit tests for new data processing or feature engineering functions
- Use existing utilities in `src/utils/` before creating new ones
- Set `RANDOM_STATE = 42` for all random operations
- Never commit large data files or credentials
- Clear notebook outputs before committing
- Update this CLAUDE.md when adding new patterns or conventions

## Getting Started Checklist

- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Add data sources documentation to `data/README.md`
- [ ] Configure logging in `src/utils/logger.py`
- [ ] Set up experiment tracking
- [ ] Create initial exploratory notebook
- [ ] Write first unit test

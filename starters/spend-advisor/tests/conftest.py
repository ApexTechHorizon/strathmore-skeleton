from pathlib import Path
import sys

# Keep this starter independently runnable, including from a repository-root pytest.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

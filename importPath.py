import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parents[2]))

from packages.svg.path import parse_path
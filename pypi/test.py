import os
from pathlib import Path
import subprocess
from info import version_string

subprocess.run(
    ["python", "setup.py", "sdist", "bdist_wheel"],
    cwd=Path(__file__).parent,
)
subprocess.run(
    [
        "pip",
        "install",
        os.path.join(
            "pypi", "dist", "buildingpy-" + version_string + "-py3-none-any.whl"
        ),
        "--force-reinstall",
    ]
)

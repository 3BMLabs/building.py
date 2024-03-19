import importlib
import inspect
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).resolve().parents[1]))

files = \
    [
    "abstract.vector",
    "geometry.point",
    "geometry.curve"
    ]

def remove_leading_whitespace(text: str) -> str:
    return '\n'.join(line.lstrip() for line in text.split('\n'))

def ensure_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_class_documentation(module_name):
    module = importlib.import_module(module_name)
    base_directory = "docs/usage"

    classes = [(cls_name, cls_obj) for cls_name, cls_obj in inspect.getmembers(module, inspect.isclass) if cls_obj.__module__ == module_name]

    for cls_name, cls_obj in classes:
        documentation_lines = []
        ensure_directory(base_directory)
        file_path = os.path.join(base_directory, f"{cls_name}.md")

        class_doc = cls_obj.__doc__ if cls_obj.__doc__ is not None else "No documentation available."
        documentation_lines.append(f"# Class `{cls_name}`\n{class_doc}\n\n## Constructor\n")

        methods = inspect.getmembers(cls_obj, predicate=inspect.isfunction)
        for method_name, method_obj in methods:
            if method_name == '__init__':
                signature = inspect.signature(method_obj)
                method_doc = method_obj.__doc__ if method_obj.__doc__ is not None else "No documentation available."
                documentation_lines.append(f"### `{method_name}{signature}`\n{method_doc}\n\n---\n")
                break

        documentation_lines.append("\n## Methods\n")
        for method_name, method_obj in methods:
            if method_name != '__init__':
                signature = inspect.signature(method_obj)
                signature = str(signature).replace("'", "")
                method_doc = method_obj.__doc__ if method_obj.__doc__ is not None else "No documentation available."
                method_doc = method_doc.split("#### Parameters:")[0]
                print(method_doc)

                documentation_lines.append(f"- `{method_name}{signature}`: {method_doc}\n")

        documentation_lines.append("\n## Documentation\n")

        for method_name, method_obj in methods:
            signature = inspect.signature(method_obj)
            method_doc_raw = method_obj.__doc__ if method_obj.__doc__ is not None else "No documentation available."
            method_doc = remove_leading_whitespace(method_doc_raw)
            if method_name != '__init__':
                documentation_lines.append(f"#### `{method_name}{signature}`\n\n{method_doc}\n\n---\n")

        # Writing to a Markdown file
        with open(file_path, 'w') as md_file:
            for line in documentation_lines:
                md_file.write(line + "\n")
        
        print(f"Documentation for {cls_name} generated in {file_path}")

for file in files:
    generate_class_documentation(file)

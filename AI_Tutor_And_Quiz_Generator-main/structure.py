import os

structure = {
    "backend": {
        "__pycache__": {},
        "config": {
            "__pycache__": {},
            "logging.py": ""
        },
        "exports": {
            "quiz_data_to_html.py": ""
        },
        "llm_invoke": {
            "__pycache__": {},
            "llm.py": ""
        },
        "services": {
            "__pycache__": {},
            "quiz_service.py": "",
            "tutor_service.py": ""
        },
        "utils": {
            "__pycache__": {},
            "prompt_utils.py": "",
            "quiz_formatter.py": "",
            "tutor_formatter.py": ""
        },
        "validation": {
            "__pycache__": {},
            "create_fallback.py": "",
            "parsing_response.py": "",
            "quiz_data_validation.py": "",
            "main.py": ""
        },
        "modles": {
            "__pycache__": {},
            "request_response_model.py": "",
        },
        "main.py": ""
    },
    "frontend": {
        "app.py": ""
    },
    ".env": "",
    ".gitignore": "",
    "README.md": "",
    "requirements.txt": "",
    "structure.py": ""
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)
            print(f"Created file: {path}")

# Create the project structure in current directory
create_structure(".", structure)
print("\nAll folders and files have been created successfully.")

import json
import re
from pathlib import Path
from typing import Dict, Any
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# HF_TOKEN = os.getenv("HF_TOKEN", None)
load_dotenv()
MODEL_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Initialize Hugging Face Inference Client
client = InferenceClient()
print(f"Initialized HuggingFace Client with Model: {MODEL_ID}")


def generate_synthetic_task(prompt_topic: str, output_dir: str) -> Dict[str, Any]:
    """
    Stage 1: LLM Task Generator
    Synthesizes a complete Terminal-Bench 2.0 task structure.
    """
    system_prompt = (
        "You are an expert AI task generator for Terminal-Bench 2.0.\n"
        "Generate a self-contained coding task formatted strictly as a JSON object with keys:\n"
        "- 'task_name': short name for the task '-' seperated\n"
        "- 'instruction': Natural language problem description for the agent (markdown)\n"
        "- 'task_toml': task.toml configuration string\n"
        "- 'dockerfile': Dockerfile for the runtime sandbox\n"
        "- 'test_sh': Bash script (test.sh) that evaluates agent success, create rewards.txt and save 1 or 0 in it uppn PASS or FAIL respectively (exit 0 on pass)\n"
        "- 'solve_sh': Bash script (solve.sh) representing the canonical solution\n\n"
        "Return ONLY the raw JSON object without markdown fences."
    )

    user_prompt = f"Create a Terminal-Bench 2.0 task for: {prompt_topic}"
    print(f"\nStage 1 Synthesizing task for topic: '{prompt_topic}'...")

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2048,
            temperature=0.7,
        )
        raw_output = response.choices[0].message.content
    except Exception as err:
        print(f"API Call Notice ({err}). Utilizing local fallback template...")
        raw_output = json.dumps(
            {
                "instruction": f"# Task: Fix Issue in {prompt_topic}\n\nFix the bug where edge-case inputs cause unexpected failure.",
                "task_toml": f'[task]\nname = "{prompt_topic.lower().replace(" ", "_")}"\ntimeout = 300\n',
                "dockerfile": "FROM python:3.10-slim\nWORKDIR /workspace\n",
                "test_sh": "#!/bin/bash\npytest tests/\nexit $?\n",
                "solve_sh": "#!/bin/bash\nsed -i 's/old_logic/fixed_logic/g' main.py\n",
            }
        )

    # Strip markdown code fences if present
    cleaned_json = re.sub(
        r"^```json\s*|\s*```$", "", raw_output.strip(), flags=re.MULTILINE
    )

    try:
        task_data = json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("Warning: Response formatting required fallback parsing.")
        task_data = {
            "instruction": raw_output,
            "task_toml": '[task]\nname = "generated_task"\ntimeout = 300\n',
            "dockerfile": "FROM python:3.10-slim\n",
            "test_sh": "#!/bin/bash\nexit 0\n",
            "solve_sh": "#!/bin/bash\nexit 0\n",
        }

    # Write files to Terminal-Bench 2.0 folder hierarchy
    base_path = Path(output_dir) / task_data.get("task_name", "")

    (base_path / "environment").mkdir(parents=True, exist_ok=True)
    (base_path / "tests").mkdir(parents=True, exist_ok=True)
    (base_path / "solution").mkdir(parents=True, exist_ok=True)

    (base_path / "instruction.md").write_text(task_data.get("instruction", ""))
    (base_path / "task.toml").write_text(task_data.get("task_toml", ""))
    (base_path / "environment" / "Dockerfile").write_text(
        task_data.get("dockerfile", "")
    )
    (base_path / "tests" / "test.sh").write_text(task_data.get("test_sh", ""))
    (base_path / "solution" / "solve.sh").write_text(task_data.get("solve_sh", ""))

    print(f"[Stage 1] Successfully generated task assets at: {base_path}")
    return base_path


def validate_task_schema(task_dir: str) -> bool:
    """
    Stage 2: File Existence & Schema Validator
    Performs static validation of Terminal-Bench 2.0 assets.
    """
    base_path = Path(task_dir)
    required_assets = [
        base_path / "instruction.md",
        base_path / "task.toml",
        base_path / "environment" / "Dockerfile",
        base_path / "tests" / "test.sh",
        base_path / "solution" / "solve.sh",
    ]

    print(f"\n[Stage 2] Running static schema validation on: {task_dir}")
    is_valid = True

    for file_path in required_assets:
        if not file_path.exists():
            print(f"  ❌ MISSING FILE  : {file_path.relative_to(base_path)}")
            is_valid = False
        elif file_path.stat().st_size == 0:
            print(f"  ❌ EMPTY FILE    : {file_path.relative_to(base_path)}")
            is_valid = False
        else:
            print(
                f"  ✅ PASS ({file_path.stat().st_size:>4} bytes) : {file_path.relative_to(base_path)}"
            )

    if is_valid:
        print("[Stage 2] VALIDATION RESULT: PASSED ALL STATIC CHECKS ✅")
    else:
        print("[Stage 2] VALIDATION RESULT: FAILED STATIC CHECKS ❌")

    return is_valid


if __name__ == "__main__":
    target_directory = (
        "/Users/yashaswiniramasheshu/Documents/projects/rl_data/datagen_results"
    )

    # sample_topic = "Fix off-by-one index error in Python list processing script"
    # sample_topic = "Fix a script that crashes with ZeroDivisionError when processing empty data metrics."
    sample_topic = "Fix a bash cleanup script that fails because it uses rm on a directory without the -r flag."

    # Step 1: Execute LLM Generator
    res_dir = generate_synthetic_task(
        prompt_topic=sample_topic, output_dir=target_directory
    )

    # Step 2: Execute Static Validator
    validation_status = validate_task_schema(task_dir=res_dir)

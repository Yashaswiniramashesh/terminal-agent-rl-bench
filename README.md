# Assignment Setup

Follow the steps below to configure your local development environment and run the assignment.

## Setup Instructions

### 1. Create a Virtual Environment
Create a localized Python environment named `.venv` to isolate the project dependencies:

```bash
# On macOS/Linux
cd rl_data
python3 -m venv .venv
pip install -r requirements.txt
```

### 2. Setup Huggingface Model
1. Edit `.env`
2. Add `HF_TOKEN` with your token from HF

### 3. Running task2

#### Setup the Task To Run

1. Some sample tasks are defined in directory `tasks`
2. Choose a task of your liking
3. Edit the main function in `assignment/agent_runner.py` 


For e.g:, Update the `task_path` and `models` to your choice
```
cd assignment2
vim agent_runner.py

'''
task_path = os.path.join(PROJECT_ROOT, "tasks/spellcheck-word-boundary")
models = [
        ("QwenAgent", "Qwen/Qwen2.5-Coder-32B-Instruct"),
        ("MetaAgent", "meta-llama/Llama-3.3-70B-Instruct"),
    ]

task = Task(task_path)
agent = Agent(
    system_prompt=terminal_bench_agent_prompt,
    agent_id=models[0][0],
    model_id=models[0][1],
)
'''
```

#### Running the agent

```
cd assignment2
python agent_runner.py
```


Sample STDOUT
```
❯ python agent_runner.py

Creating agent 'QwenAgent' with model: 'Qwen/Qwen2.5-Coder-32B-Instruct'
Building env for Task: spellcheck-word-boundary
Task artifacts: /Users/xxx/Documents/projects/rl_data/tasks/spellcheck-word-boundary
Running harness with Task: 'spellcheck-word-boundary' and Agent: 'QwenAgent'
Building Docker image for task: spellcheck-word-boundary
Dockerfile in: /Users/xxx/Documents/projects/rl_data/tasks/spellcheck-word-boundary/environment
Starting Docker container for task: spellcheck-word-boundary
CONTAINER ID   IMAGE                            COMMAND        CREATED                  STATUS                  PORTS     NAMES
55d41e7fa32b   image_spellcheck-word-boundary   "sleep 3600"   Less than a second ago   Up Less than a second             container_spellcheck-word-boundary

******************************************************************************************
{
   "step_num": 1,
   "command": "cat /app/spellcheck.py",
   "is_complete": false,
   "reasoning": "I need to first examine the current implementation of the spellcheck.py script to understand how it's currently handling the replacement and confirm the issue described.",
   "observation": "import sys\n\ntry:\n  with open(\"/app/draft.txt\", \"r\") as f:\n    text = f.read()\n\n  # Bug: basic string replace is case-sensitive and misses \"Recieve\"\n  corrected_text = text.replace(\"recieve\", \"receive\")\n\n  with open(\"/tmp/corrected_draft.txt\", \"w\") as out:\n    out.write(corrected_text)\nexcept Exception as e:\n  print(f\"Failed to run spellcheck: {e}\", file=sys.stderr)\n  sys.exit(1)\n",
   "exit_code": 0
}
******************************************************************************************
******************************************************************************************
{
   "step_num": 2,
   "command": "python3 /app/spellcheck.py",
   "is_complete": false,
   "reasoning": "I need to run the current spellcheck.py script to confirm it fails on capitalized instances like 'Recieve' before implementing the fix.",
   "observation": "(no output)",
   "exit_code": 0
}
...

Computing reward for task: deep-json-merger
{'binary_reward': 1.0, 'shaped_reward': 0.97, 'steps_taken': 8, 'test_output': 'Verification successful!\nREWARD = 1 (PASS)\n'}
Successfully created: /Users/xxx/Documents/projects/rl_data/results/QwenAgent/deep-json-merger/attempt4
Trajectory saved to: '/Users/xxx/Documents/projects/rl_data/results/QwenAgent/deep-json-merger/attempt4/trajectory.json'
Rewards saved to: '/Users/xxx/Documents/projects/rl_data/results/QwenAgent/spellcheck-word-boundary/attempt4/rewards.json'
Stopping and removing docker container: 36ef0cb6c836bb357b54667d77cd751cf0ecdca6f0f813a50b644c49bf760a3e
```
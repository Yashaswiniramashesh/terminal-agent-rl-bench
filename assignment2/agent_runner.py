import json
import os

from huggingface_hub import InferenceClient

from env_builder import EnvBuilder
from task import Task
from prompt import terminal_bench_agent_prompt
from schema import terminal_bench_schema
from dotenv import load_dotenv
from time import sleep

load_dotenv()

PROJECT_ROOT = os.environ.get("PROJECT_ROOT")


class Agent(object):
    def __init__(self, system_prompt, agent_id, model_id):
        self.model_id = model_id
        self.agent_id = agent_id
        self.system_prompt = system_prompt
        self.client = InferenceClient()
        print(f"Creating agent '{agent_id}' with model: '{model_id}'")

    def invoke(self, messages, max_tokens=1000, temperature=0.0, schema=None):
        messages = [{"role": "system", "content": self.system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=schema,
        )
        return response


class Harness(object):
    def __init__(self, env, task, agent, max_steps=10):
        self.client = InferenceClient()
        self.agent = agent
        # self.model_id = agent.model_id
        self.agent_id = agent.agent_id
        self.env = env
        self.task = task
        self.max_steps = max_steps
        print(
            f"Running harness with Task: '{task.task_name}' and Agent: '{self.agent_id}'"
        )

    def execute_agent(self):
        trajectory = []
        with open(self.task.instruction) as f:
            instruction = f.read()

        self.env.setup()
        conversation_history = []
        conversation_history.append(
            {
                "role": "user",
                "content": f"Here is your task:\n\n{instruction}\n\nWhat is the first command you want to run?",
            }
        )

        for step_num in range(self.max_steps):
            response = self.agent.invoke(
                messages=conversation_history, schema=terminal_bench_schema
            )
            response_json = json.loads(response.choices[0].message.content.strip())

            action = (
                response_json["command"]
                .replace("```bash", "")
                .replace("```", "")
                .replace("`", "")
                .strip()
            )
            cmd_reasoning = response_json["reasoning"]
            is_complete = response_json["is_complete"] or step_num >= self.max_steps

            conversation_history.append({"role": "assistant", "content": action})

            #: execute agent action
            env_result = self.env.step(action, cmd_reasoning)
            observation = env_result["observation"]
            result = {"step_num": step_num + 1}
            result.update(**response_json.copy())
            result["observation"] = observation
            result["exit_code"] = env_result["exit_code"]

            trajectory.append(result)

            print("*" * 90)
            print(json.dumps(result, indent=3))
            print("*" * 90)
            sleep(20)

            if is_complete:
                conversation_history.append(
                    {
                        "role": "user",
                        "content": f"Output:\n{observation}\n\nMax steps reached, ending the session.",
                    }
                )
                break
            else:
                conversation_history.append(
                    {
                        "role": "user",
                        "content": f"Output:\n{observation}\n\nWhat is your next command?",
                    }
                )

        return trajectory

    def save_results(self, trajectory, rewards):
        """
        proj_root/results/agent_id/task_id/trajectory.json, reward.json
        """

        def create_next_version_folder(base_dir, prefix="v"):
            version = 1

            # Loop until we find a version folder name that does NOT exist
            while True:
                folder_name = f"{prefix}{version}"
                target_folder = os.path.join(base_dir, folder_name)

                if not os.path.exists(target_folder):
                    # os.makedirs creates the folder (and any missing parent folders) safely
                    os.makedirs(target_folder, exist_ok=True)
                    print(f"Successfully created: {target_folder}")
                    return target_folder

                version += 1

        results_dir = os.path.join(PROJECT_ROOT, "results")
        agent_results_dir = os.path.join(
            results_dir, self.agent_id, self.task.task_name
        )

        attempts_dir = create_next_version_folder(agent_results_dir, prefix="attempt")

        trajectory_path = os.path.join(attempts_dir, "trajectory.json")
        rewards_path = os.path.join(attempts_dir, "rewards.json")

        os.makedirs(attempts_dir, exist_ok=True)

        #: save trajectory.json
        with open(trajectory_path, "w") as f:
            json.dump(trajectory, f, indent=4)

        print(f"Trajectory saved to: '{trajectory_path}'")

        #: save rewards.json
        with open(rewards_path, "w") as f:
            json.dump(rewards, f, indent=4)

        print(f"Rewards saved to: '{rewards_path}'")


if __name__ == "__main__":
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

    env = EnvBuilder(task=task)

    harness = Harness(env, task, agent, max_steps=15)
    try:
        trajectory = harness.execute_agent()
        reward_info = env.compute_final_reward(steps_taken=len(trajectory))
        harness.save_results(trajectory, reward_info)
        env.close()

    except Exception as e:
        print(e)
        env.close()

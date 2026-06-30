import os
import subprocess
import tempfile

from task import Task


class EnvBuilder(object):
    def __init__(self, task, max_steps=15):
        self.task = task
        self.task_path = task.task_path
        self.task_name = task.task_name
        self.max_steps = max_steps
        self.container_id = None
        self.steps_taken = 0
        self.trajectory = []
        self.logs_dir = None

        print(f"Building env for Task: {self.task_name}\nTask artifacts: {self.task_path}")

    def _validate_task(self):
        self.task.validate()

    def _call_subprocess(self, cmd):
        return subprocess.run(cmd, capture_output=True, text=True)
    
    def setup(self):
        """Kill the exisiting and Build Docker Image, Start fresh.
        Return task instruction as the first obeservation
        """
        self.close()
        self.steps_taken = 0
        self.trajectory = []
        self.logs_dir = tempfile.mkdtemp()
        image_name = f"image_{self.task_name}"
        dockefile_dir = os.path.join(self.task_path, "environment")
        tests_dir = os.path.join(self.task_path, "tests")
        container_name = f"container_{self.task_name}"
        
        print(f"Building Docker image for task: {self.task_name}")
        print(f"Dockerfile in: {dockefile_dir}")
        
        #: build docker image based on task's Dockerfile
        build = self._call_subprocess(
            [
                "docker", "build", "-t", image_name, dockefile_dir
            ]
        )
        
        if build.returncode !=0:
            raise RuntimeError(f"Build failed: {build.stderr[-400:]}")
        
        print(f"Starting Docker container for task: {self.task_name}")
        
        #: start the docker container
        #: caveat: sleep 3600 is a flaky command. need to add while True or something else for long running tasks
        start = self._call_subprocess(
            [
                "docker", "run", "-d",
                "-v", f"{tests_dir}:/tests",
                "-v", f"{self.logs_dir}:/logs", 
                "--name", container_name,
                image_name,
                "sleep", "3600"
            ]
        )
        
        if start.returncode !=0:
            raise RuntimeError(f"Starting container error: {start.stderr}")
        else:
            status = self._call_subprocess(["docker", "ps"])
            print(status.stdout)
        
        self.container_id = start.stdout.strip()
        return self.container_id

    def step(self, action: str, reasoning: str="(No reasoning)"):
        """Run shell commands inside the container
        Records it to the trajectory. Returns what happended
        """
        if not self.container_id:
            raise RuntimeError("Container env not found. Call reset() first")
        
        self.steps_taken += 1

        result =  self._call_subprocess(
            ["docker", "exec", self.container_id, "bash", "-c", action]
        )

        obs = result.stdout
        if result.stderr:
            obs += f"\n[stderr]: {result.stderr[:200]}"
        
        if not obs.strip():
            obs = "(no output)"

        self.trajectory.append({
            "step": self.steps_taken,
            "action": action,
            "reasoning" : reasoning,
            "observation": obs[:600],
            "exit_code": result.returncode
        })
        
        # return StepResult(
        #     observation=obs,
        #     reward=0.0,
        #     # completetion_state=(self.steps_taken >= self.max_steps),
        #     info={"step": self.steps_taken, "exit_code": result.returncode}
        # )
    
        return {
            "observation": obs,
            "exit_code": result.returncode
            # "info": {"step": self.steps_taken, "exit_code": result.returncode}
        } 
    
    def compute_final_reward(self, steps_taken):
        """Run test shell script inside the container, Read reward.txt, Return rewardss"""

        print(f"Computing reward for task: {self.task_name}")
        if not self.container_id:
            raise RuntimeError("Container not up. Call for setup()")
        
        run = self._call_subprocess(
            ["docker", "exec", self.container_id, "bash", "/tests/test.sh"]
        )
        
        reward_file = os.path.join(self.logs_dir, "verifier", "reward.txt")
        if os.path.exists(reward_file):
            with open(reward_file) as f:
                binary_reward = float(f.read())
        else:
            binary_reward = 0.0
        
        penalty = min(0.15, max(0, steps_taken - 5) * 0.01)
        shaped = round(binary_reward - penalty, 3)

        reward = {
            "binary_reward": binary_reward,
            "shaped_reward": shaped,
            "steps_taken": self.steps_taken,
            "test_output": run.stdout
        }

        print(reward)

        return reward
    
    # def save_trajectory(self, filepath):
    #     """Save the trajectory to a JSON file for grading later."""
    #     Path(filepath).write_text(json.dumps({
    #         "task": self.task_name,
    #         "steps": self.trajectory,
    #         "total_steps": self.steps_taken
    #     }, indent=2))

    def close(self):
        """Force stop and delete the container."""
        if self.container_id:
            print(f"Stopping and removing docker container: {self.container_id}")
            self._call_subprocess(["docker", "rm", "-f", self.container_id])
            self.container_id = None


if __name__ == "__main__":
    pass
    # task_path = "/Users/yashaswiniramasheshu/Documents/projects/rl_data/tasks/broken-log-parser"
    # env = EnvBuilder(Task(task_path))
    # env.setup()
    # result = env.step(action="ls")
    # print(result)

    # env.compute_final_reward(5)

    # env.close()
import os

from env._base import BaseEnv


class Env(BaseEnv):
    workflows_base_url: str = "https://api.mistral.ai"
    deployment_name: str | None = None


env = Env()

# Override workflows_base_url with SERVER_URL if set (platform-injected)
if os.environ.get("SERVER_URL"):
    env.workflows_base_url = os.environ["SERVER_URL"]

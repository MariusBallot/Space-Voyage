import os

from env._base import BaseEnv


class Env(BaseEnv):
    mistral_api_key: str | None = None
    # Optional Mistral REST API base URL. None uses the SDK default.
    mistral_base_url: str | None = None


env = Env()

# Override mistral_base_url with SERVER_URL if set (platform-injected)
if os.environ.get("SERVER_URL") and env.mistral_base_url is None:
    env.mistral_base_url = os.environ["SERVER_URL"]

import os
from dotenv import load_dotenv
from baymax import Baymax
import json


def main() -> None:

    load_dotenv()

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    llm_kwargs = config["model"]
    llm_kwargs["model_path"] = f"models/{os.environ['MODEL']}"

    baymax = Baymax(
        system_prompt=config["system_prompt"],
        chat_id=config["telegram"]["chat_id"],
        token=config["telegram"]["token"],
        llm_kwargs=config["model"],
        chat_completion_kwargs=config["chat_completion"]
    )
    baymax()


if __name__ == "__main__":
    main()

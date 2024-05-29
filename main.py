import os
from dotenv import load_dotenv
from baymax import Baymax
import json


def main() -> None:

    load_dotenv()

    with open('model_config.json', 'r') as config_file:
        config = json.load(config_file)

    baymax = Baymax(
        intial_prompt=config["initial_prompt"],
        chat_id=os.environ["TELEGRAM_CHAT_ID"],
        token=os.environ["TELEGRAM_TOKEN"],
        llm_kwargs=config["model"],
        chat_completion_kwargs=config["chat_completion"]
    )
    baymax()


if __name__ == "__main__":
    main()

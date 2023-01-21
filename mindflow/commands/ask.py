import sys
import argparse

from mindflow.clients.gpt.openai import GPT
from mindflow.clients.mindflow.completion import completion as remote_completion
from mindflow.utils.args import _add_ask_args, _add_remote_args, _add_response_args
from mindflow.utils.response import handle_response_text


class Ask:
    remote: bool
    skip_clipboard: bool
    return_prompt: bool
    prompt: str

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with basic request.",
        )
        _add_ask_args(parser)
        _add_response_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])
        self.remote: bool = args.remote
        self.skip_clipboard: bool = args.skip_clipboard
        self.return_prompt: bool = True
        self.prompt: str = args.prompt

    def execute(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        if not self.remote:
            GPT.authorize()

        ## Prompt GPT through Mindflow API or locally
        if self.remote:
            response: str = remote_completion(self.prompt, self.return_prompt).text
        else:
            ## Always return prompt for now...
            response: str = self.prompt

        handle_response_text(response, self.skip_clipboard)

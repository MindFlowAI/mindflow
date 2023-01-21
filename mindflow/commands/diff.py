import argparse
import sys

from mindflow.clients.gpt.openai import GPT
from mindflow.command_helpers.diff.diff import generate_diff_prompt
from mindflow.clients.mindflow.completion import completion as remote_completion
from mindflow.utils.args import _add_diff_args, _add_remote_args, _add_response_args
from mindflow.utils.response import handle_response_text


class Diff:
    remote: bool
    skip_clipboard: bool
    return_prompt: bool
    diffargs: str

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with git diff.",
        )
        _add_diff_args(parser)
        _add_response_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])
        self.remote = args.remote
        self.diffargs = args.diffargs
        self.return_prompt = True
        self.skip_clipboard = args.skip_clipboard

    def execute(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        if not self.remote:
            GPT.authorize()

        # Run Git diff and get the output with prompt suffix
        prompt = generate_diff_prompt(self.diffargs)

        ## Prompt GPT through Mindflow API or locally
        if self.remote:
            response: str = remote_completion(prompt, self.return_prompt).text
        else:
            ## Always return prompt for now...
            response: str = prompt

        handle_response_text(response, self.skip_clipboard)

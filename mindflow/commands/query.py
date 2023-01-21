import argparse

import sys

from typing import List
from mindflow.clients.gpt.openai import GPT

from mindflow.utils.response import handle_response_text
from mindflow.index.generate import generate_index
from mindflow.index.resolvers.base_resolver import Resolved
from mindflow.index.resolve import resolve
from mindflow.utils.args import (
    _add_query_args,
    _add_generate_args,
    _add_reference_args,
    _add_remote_args,
    _add_response_args,
)
from mindflow.clients.mindflow.query import query as remote_query
from mindflow.command_helpers.query.query import query as local_query


class Query:
    query: str
    references: List[str]
    index: bool
    remote: bool
    return_prompt: bool
    skip_clipboard: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="This command is use to query files, folders, and websites.",
        )
        _add_query_args(parser)
        _add_reference_args(parser)
        _add_generate_args(parser)
        _add_response_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.references = args.references
        self.index = args.index
        self.remote = args.remote
        self.query = args.query
        self.return_prompt = True
        self.skip_clipboard = args.skip_clipboard

    def execute(self):
        """
        This function is used to ask a custom question about files, folders, and websites.
        """
        if not self.remote:
            GPT.authorize()

        ## Resolve references (Path, URL, etc.)
        resolved_references: List[Resolved] = []
        for reference in self.references:
            resolved_references.extend(resolve(reference))

        ## Generate index and/or embeddings
        if self.index:
            generate_index(resolved_references, self.remote)

        reference_hashes: List[str] = [
            reference.text_hash for reference in resolved_references
        ]

        ## Query through Mindflow API or locally
        if self.remote:
            response: str = remote_query(
                self.query, reference_hashes, self.return_prompt
            ).text
        else:
            response: str = local_query(
                self.query, reference_hashes, self.return_prompt
            )

        handle_response_text(response, self.skip_clipboard)

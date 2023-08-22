import tiktoken
from typing import List, Dict, Callable
from colorama import Fore, Style
from formatting import ensure_terminal_formatting


gpt_token_encoder = tiktoken.encoding_for_model("gpt-4")
max_tokens = 8_000


def log(text: str, color: str = Fore.WHITE, end="\n"):
	print(f"{color}{text}{Style.RESET_ALL}", end=end)


def context_token_len(context: List[Dict[str, str]]) -> int:
	num_tokens = 0
	for message in context:
		num_tokens += 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
		num_tokens += len(gpt_token_encoder.encode(message["content"]))
	num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
	return num_tokens


def limit_context_length(context: List[Dict[str, str]]):
	while context_token_len(context) > max_tokens:
		context.pop(1)


def ask_llm(context: List[Dict[str, str]], ask_fn: Callable[[List[Dict[str, str]], bool], str]) -> str:
	limit_context_length(context)
	terminal_code = ask_fn(context).strip()
	formatted_code = ensure_terminal_formatting(terminal_code, ask_fn)
	return formatted_code

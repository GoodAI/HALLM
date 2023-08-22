from typing import List, Dict, Callable


def remove_terminal_line_decorators(terminal_code: str) -> str:
	return "\n".join([line[4:] for line in terminal_code.splitlines()])


def add_terminal_line_decorators(terminal_entry: str) -> str:
	decorated_lines = list()
	for i, line in enumerate(terminal_entry.splitlines()):
		decoration = ">>> " if i == 0 else "... "
		decorated_lines.append(decoration + line)
	return "\n".join(decorated_lines)


def ensure_terminal_formatting_strict(terminal_code: str, force: bool = False) -> str:
	formatted_lines = list()
	for i, line in enumerate(terminal_code.splitlines()):
		if line == "":
			continue
		if line[0] == "#":
			line = ">>> " + line
		if line in {">>>", "..."}:
			line += " "
		if force and line[:4] not in {">>> ", "... "}:
			continue
		assert line[:4] in {">>> ", "... "}, f"Line {i} doesn't look like terminal code:\n{terminal_code}"
		formatted_lines.append(line)
	return "\n".join(formatted_lines)


def ensure_terminal_formatting_llm(code: str, ask_fn: Callable[[List[Dict[str, str]], bool], str]) -> str:
	formatting_prompt = (
		"Format the following code as if it was code written in a python terminal. The output must comply with these "
		"rules:\n"
		"- Every line has to start with either `>>>` or `...`.\n"
		"- There can't be any blank line.\n"
		"- There can only be valid python commands or comments.\n"
		"If you find free-form text, convert it into a comment.\n\n"
		f"```\n{code}\n```"
	)
	return ask_fn([{"role": "user", "content": formatting_prompt}], True).strip()


def ensure_terminal_formatting(code: str, ask_fn: Callable[[List[Dict[str, str]], bool], str]) -> str:
	try:
		return ensure_terminal_formatting_strict(code)
	except AssertionError:
		pass
	llm_formatted_code = ensure_terminal_formatting_llm(code, ask_fn)
	# Sometimes, the LLM hallucinates output lines if `print` is on the last line.
	num_code_lines = len(code.splitlines())
	llm_formatted_code = "\n".join(llm_formatted_code.splitlines()[:num_code_lines])
	return ensure_terminal_formatting_strict(llm_formatted_code, force=True)


def extract_terminal_entries(terminal_code: str) -> List[str]:
	entries = terminal_code.split("\n>>> ")
	entries = entries[0:1] + [">>> " + e for e in entries[1:]]
	return [remove_terminal_line_decorators(e) for e in entries]

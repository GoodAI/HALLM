import contextlib
from io import StringIO
from typing import List, Tuple, Dict, Callable
from code import InteractiveConsole
from colorama import Fore
from wrappers import AgentIsDone
from utils import log, ask_llm
from formatting import add_terminal_line_decorators, extract_terminal_entries


class AgentInteractiveConsole(InteractiveConsole):
	def runcode(self, code) -> None:
		try:
			exec(code, self.locals)
		except (SystemExit, AgentIsDone):
			raise
		except:
			self.showtraceback()


def run_entry(
		interactive_console: AgentInteractiveConsole, entry_code: str
) -> Tuple[bool, str, str, str]:
	interactive_console.resetbuffer()
	message = ""
	agent_is_done = False
	executed_lines = []
	with StringIO() as redirected_stdout_stderr:
		with contextlib.redirect_stdout(redirected_stdout_stderr):
			with contextlib.redirect_stderr(redirected_stdout_stderr):
				try:
					more_input = False
					for line in entry_code.splitlines():
						executed_lines.append(line)
						more_input = interactive_console.push(line)
						if not more_input:
							break
					if more_input:
						interactive_console.push("")
				except AgentIsDone:
					agent_is_done = True
		executed_lines = add_terminal_line_decorators("\n".join(executed_lines))
		return (
			agent_is_done,
			redirected_stdout_stderr.getvalue(),
			executed_lines,
			message,
		)


def run_until_halt(
		interactive_console: AgentInteractiveConsole,
		ask_fn: Callable[[List[Dict[str, str]], bool], str],
		context: List[Dict[str, str]],
) -> Tuple[bool, str]:
	agent_is_done = False
	message = ""
	while not (agent_is_done or message != ""):
		captured_output = ""
		executed_entries = list()
		terminal_code = ask_llm(context, ask_fn)
		terminal_entries = extract_terminal_entries(terminal_code)
		for entry_code in terminal_entries:
			(
				agent_is_done,
				captured_output,
				executed_lines,
				message,
			) = run_entry(interactive_console, entry_code)
			executed_entries.append(executed_lines)
			# As soon as there's some output, the LLM might want to react to it -> put it in context and ask again.
			if agent_is_done or captured_output != "":
				break
		executed_code = "\n".join(executed_entries)
		context.append({"role": "assistant", "content": executed_code})
		log(executed_code, color=Fore.LIGHTYELLOW_EX)
		if captured_output != "":
			context.append({"role": "user", "content": captured_output})
			log(captured_output, color=Fore.LIGHTCYAN_EX, end="" if captured_output[-1] == "\n" else "\n")
	return agent_is_done, message


def react(
		interactive_console: AgentInteractiveConsole,
		ask_fn: Callable[[List[Dict[str, str]], bool], str],
		context: List[Dict[str, str]],
		user_command: str,
) -> Tuple[bool, str]:
	context.append({"role": "user", "content": user_command})
	log(user_command, color=Fore.LIGHTGREEN_EX)
	agent_is_done, message = run_until_halt(interactive_console, ask_fn, context)
	return agent_is_done, message

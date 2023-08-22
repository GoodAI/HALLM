import sys

real_stdout = sys.stdout


class AgentIsDone(Exception):
	pass


def done():
	raise AgentIsDone


def proxy_input(text: str) -> str:
	real_stdout.write(text)
	real_stdout.flush()
	return input(text)

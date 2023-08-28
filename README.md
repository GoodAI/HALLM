# HALLM

Read more about HALLM on [GoodAI's blog](https://www.goodai.com/hallm-an-llm-agent-embodied-within-a-python-terminal/).

This is a prototype that was developed by GoodAI's agents team with the
purpose of evaluating the performance of a Large Language Model (LLM)
within a highly dynamic and immersive environment. The main idea is that
the LLM can freely interact with a Python terminal, in a way that feels
very natural to the LLM and boosts engagement.

We chose the Python terminal for several reasons:

- **Familiarity**. Python is an extremely popular programming language and
therefore the LLM should be quite familiar with it. At the same time,
users might find it easier to follow the agent's actions.
- **Dynamism**. While interacting with a Python terminal or any kind of
terminal, one develops solutions step by step, engaging in a continuous
process of exploration, trial, and error.

In order to start the interactive session, follow these steps:

1. Make sure you have the right Python version. It should work with any
Python `3.x` version.

2. Install the requirements.

```bash
pip install -r requirements.txt
```

3. Open your terminal and set your OpenAI API key.

```bash
export OPENAI_API_KEY=...
```

2. Run the main script.

```bash
python main.py
```
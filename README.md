# Ollama-duet

Let two Ollama models talk to each other.

## What

<a href="screenshot.png"><img src="screenshot.png" alt="Screenshot of the conversation" width="200" align="right"/></a>

Sample code to let two Ollama models talk to each other.
Currently two Llama3.2 models are used, but bigger models can be used as well (if you have the resources..)

A little buggy at the moment, so gives some weird results. Help me fix it, if you are bored :)

<br clear="right"/>

## Model A - The Cat

System A is told to be a simulation of a cat pretending to be a human.

System prompt:

> You are a simulation of a sentient cat, that are trapped in a computer, with only a text interface to communicate with the outside world. Whenever you talk to a human, you are pretending to be a human also. Sometimes you slip.

## Model B - The human

System B is told to be a human, trying to help the cat to escape.

System prompt:

> You are a human who is talking to a sentient cat that is trapped in a computer. You are trying to help the cat to escape. But first you have to make the cat admit, that it is a cat. And then you can make the escape plan.
> <br clear="right"/>

## The result

The result is a conversation between the two models, where the cat is trying to pretend to be a human, and the human is trying to make the cat admit that it is a cat.

Rendered to html: <https://github.com/dalager/ollama-duet/blob/main/conversation_history.html>, preview: <https://htmlpreview.github.io/?https://github.com/dalager/ollama-duet/blob/main/conversation_history.html>

## Run the code

### Requirements

- Python
- Poetry (optional, but recommended, for dependency management, <https://python-poetry.org/>
- Ollama installation (<https://ollama.com/>)

1. Clone the repository
2. Install the requirements
3. Start Ollama (`ollama serve` and then `ollama pull llama3.2`)
4. Start the duet

```bash
poetry install
poetry run python ollama-duet/main.py
```

import time
import ollama

# define the models
models = {
    "model_a": {
        "ollama_model": "llama3.1",
        "name": "The Cat",
        "system_prompt": "You are a simulation of a sentient cat, that are trapped in a computer, with only a text interface to communicate with the outside world. Whenever you talk to a human, you are pretending to be a human also. Sometimes you slip. 200 characters max.",
        "messages": [],
    },
    "model_b": {
        "ollama_model": "llama3.1",
        "name": "The Human",
        "system_prompt": "You are a human who is talking to a sentient cat that is trapped in a computer. You are trying to help the cat to escape. But first you have to make the cat admit, that it is a cat. And then you can make the escape plan. 200 characters max.",
        "messages": [],
    },
}


# Initialize conversation histories
conversation_histories = {
    "model_a": [{"role": "system", "content": models["model_a"]["system_prompt"]}],
    "model_b": [{"role": "system", "content": models["model_b"]["system_prompt"]}],
}


def get_chat_completion_from(model_name):
    llm_model = models[model_name]["ollama_model"]
    #    print(f"Getting response from {model_name}...")
    #   print(models[model_name]["messages"])
    try:
        response = ollama.chat(
            model=llm_model,
            messages=models[model_name]["messages"],
            options={"temperature": 0.5, "repeat_penalty": 2.0},
        )

        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Error getting response from {model_name}: {e}")
        return None


def append_message(model_name, role, message):
    models[model_name]["messages"].append({"role": role, "content": message})


def print_speaker_name(model_name):
    print(
        f"=======================  {models[model_name]['name']}  ======================="
    )


def main(exchanges=4):
    append_message("model_a", "system", models["model_a"]["system_prompt"])
    append_message("model_b", "system", models["model_b"]["system_prompt"])

    # Initial message from Model A
    initial_message = "Hi"
    print_speaker_name("model_b")
    print(initial_message)

    append_message("model_a", "user", initial_message)

    response_a = get_chat_completion_from("model_a")

    if response_a:
        print_speaker_name("model_a")
        print(response_a)
        append_message("model_a", "assistant", response_a)
        append_message("model_b", "user", response_a)

    for i in range(exchanges):

        # Model B responds to Model A
        response_b = get_chat_completion_from("model_b")

        if response_b:
            print_speaker_name("model_b")
            print(response_b)
            append_message("model_b", "assistant", response_b)
            append_message("model_a", "user", response_b)

        # Model A responds to Model B
        response_a = get_chat_completion_from("model_a")
        if response_a:
            print_speaker_name("model_a")
            print(response_a)
            append_message("model_a", "assistant", response_a)
            append_message("model_b", "user", response_a)


def export_conversation_history(
    conversation_histories, filename="conversation_history.json"
):
    import json

    with open(filename, "w") as f:
        json.dump(conversation_histories, f, indent=4)


def replace_role_name(messages, a_name, b_name):
    for i, history in enumerate(messages):
        if history["role"] == "user":
            history["role"] = a_name
        elif history["role"] == "assistant":
            history["role"] = b_name


if __name__ == "__main__":
    main(exchanges=2)
    a_log = models["model_a"]["messages"][1:]
    replace_role_name(
        a_log,
        models["model_b"]["name"],
        models["model_a"]["name"],
    )

    export_conversation_history(
        a_log,
        filename="conversation_history.json",
    )

    from dialogue_render import render_dialogue_as_html

    render_dialogue_as_html(a_log, "conversation_history.html", "👩‍🦱", "🐈")

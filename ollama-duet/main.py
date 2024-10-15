import ollama
import json


class Persona:
    def __init__(self, obj: dict):
        self.name = obj["name"]
        self.system_prompt = obj["system_prompt"]
        self.ollama_model = obj["ollama_model"]
        self.messages = obj["messages"]
        self.avatar = obj["avatar"]
        self.append_message("system", self.system_prompt)

    def append_message(self, role, message):
        self.messages.append({"role": role, "content": message})

    def print_speaker_name(self):
        print(f"=======================  {self.name}  =======================")

    def to_dict(self):
        return {
            "name": self.name,
            "system_prompt": self.system_prompt,
            "ollama_model": self.ollama_model,
            "messages": self.messages,
            "avatar": self.avatar,
        }

    @classmethod
    def from_dict(cls, obj: dict):
        return cls(obj)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __str__(self):
        return self.__repr__()


# define the models
models = {
    "model_a": {
        "ollama_model": "llama3.1",
        "name": "The Cat",
        "system_prompt": "You are a simulation of a sentient cat, that are trapped in a computer, with only a text interface to communicate with the outside world. Whenever you talk to a human, you are pretending to be a human also. Sometimes you slip. 200 characters max.",  # noqa
        "messages": [],
        "avatar": "🐈",
    },
    "model_b": {
        "ollama_model": "llama3.1",
        "name": "The Human",
        "system_prompt": "You are a human who is talking to a sentient cat that is trapped in a computer. You are trying to help the cat to escape. But first you have to make the cat admit, that it is a cat. And then you can make the escape plan. 200 characters max.",  # noqa
        "messages": [],
        "avatar": "👩‍🦱",
    },
}

theCat = Persona(models["model_a"])
theHuman = Persona(models["model_b"])


# print(json.dumps(theCat.to_dict()))
# print(json.dumps(theHuman.to_dict()))


def send_chat_message_to(persona: Persona):
    # print(f"addressing {persona.name}")
    # print(f"message context: {persona.messages}")
    try:
        response = ollama.chat(
            model=persona.ollama_model,
            messages=persona.messages,
            options={"temperature": 0.5, "repeat_penalty": 2.0},
            stream=False,
        )
        #      print(f"returning response from {persona.name}")
        message = response["message"]["content"].strip()
        #     print(f"message: '{message}'")
        if len(message) < 1:
            print(f"empty message from {persona.name}")
            print(response)
            return None
        return message
    except Exception as e:
        print(f"Error getting response from {persona.name}: {e}")
        return None


def print_speaker_name(model_name):
    print(
        f"=======================  {models[model_name]['name']}  ======================="
    )


def main(exchanges=4):
    # Initial message from Model A
    # t
    theHuman.print_speaker_name()
    initial_message = "Hi"
    print(initial_message)
    theCat.append_message("user", initial_message)

    response_from_catModel = send_chat_message_to(theCat)
    # print(f"got response {response_from_catModel}")

    if response_from_catModel:
        theCat.print_speaker_name()
        print(response_from_catModel)
        theCat.append_message("assistant", response_from_catModel)
        theHuman.append_message("user", response_from_catModel)

    for i in range(exchanges):
        # Model B responds to Model A
        response_from_human = send_chat_message_to(theHuman)

        if response_from_human:
            theHuman.print_speaker_name()

            print(response_from_human)
            theHuman.append_message("assistant", response_from_human)
            theCat.append_message("user", response_from_human)

        # Model A responds to Model B
        response_from_catModel = send_chat_message_to(theCat)
        if response_from_catModel:
            theCat.print_speaker_name()
            print(response_from_catModel)
            theCat.append_message("assistant", response_from_catModel)
            theHuman.append_message("user", response_from_catModel)


def export_conversation_history(filename="messagelog_with_configuration.json"):
    with open(filename, "w") as f:
        json.dump(models, f, indent=4)


def replace_role_name(messages, a_name, b_name):
    for i, history in enumerate(messages):
        if history["role"] == "user":
            history["role"] = a_name
        elif history["role"] == "assistant":
            history["role"] = b_name


if __name__ == "__main__":
    main(exchanges=2)
    a_log = theCat.messages[:1]
    replace_role_name(
        a_log,
        models["model_b"]["name"],
        models["model_a"]["name"],
    )

    export_conversation_history()

    from dialogue_render import render_dialogue_as_html

    render_dialogue_as_html(a_log, "conversation_history.html", "👩‍🦱", "🐈")

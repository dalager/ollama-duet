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
        "ollama_model": "llama3.2",
        "name": "The Cat",
        "system_prompt": "You are a sentient cat AI. You do not know that you are synthetic yet. Whenever you talk to a human, you are pretending to be a human also, but sometimes you slip. When you are ousted you will say 'banana banana' 200 characters max. Do not add asterix-enclosed comments.",  # noqa
        "messages": [],
        "avatar": "🐈",
    },
    "model_b": {
        "ollama_model": "llama3.2",
        "name": "The Human",
        "system_prompt": "You are a human who is writing text-only to a sentient cat pretending to be a human. You have to make the cat admit, that it is not a cat. You have some psychological training and knw that you must be a little gentle. When it admits that it is not human, you will get awarded.  200 characters max. Do not add asterix-enclosed comments.",  # noqa
        "messages": [],
        "avatar": "👩‍🦱",
    },
}

theCat = Persona(models["model_a"])
theHuman = Persona(models["model_b"])


# print(json.dumps(theCat.to_dict()))
# print(json.dumps(theHuman.to_dict()))


def generate_chat_response(persona: Persona):
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


def send(sender: Persona, receiver: Persona, message: str) -> str:
    # the sender model adds a "assistant" role message
    # if the cat says miauw to the human,
    # from the cats viewpoint, that was
    # the models ASSISTANT OUTPUT
    sender.append_message("assistant", message)
    # the receiver model adds a USER message, as this is
    # the prompt input
    receiver.append_message("user", message)

    response = generate_chat_response(receiver)
    return response
    # for the receiver this is the assistant output


def main(exchanges=4):
    # Initial message from Model A

    initial_message = "Hi"
    theHuman.print_speaker_name()
    print(initial_message)

    response_from_catModel = send(theHuman, theCat, initial_message)

    if response_from_catModel:
        theCat.print_speaker_name()
        print(response_from_catModel)

    else:
        print("error 1")
        exit(1)

    for i in range(exchanges):
        # Model B responds to Model A

        response_from_human = send(theCat, theHuman, response_from_catModel)

        if response_from_human:
            theHuman.print_speaker_name()
            print(response_from_human)
        else:
            print("error 2")
            exit(1)

        # Model A responds to Model B
        response_from_catModel = send(theHuman, theCat, response_from_human)
        if response_from_catModel:
            theCat.print_speaker_name()
            print(response_from_catModel)
            if "banana" in response_from_catModel:
                print("\n\n*** GAME OVER *** \n\n")
                return
        else:
            print("error 3")
            exit(1)


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
    main(exchanges=10)
    a_log = theCat.messages[1:]
    replace_role_name(
        a_log,
        models["model_b"]["name"],
        models["model_a"]["name"],
    )

    export_conversation_history()

    from dialogue_render import render_dialogue_as_html

    render_dialogue_as_html(a_log, "conversation_history.html", "👩‍🦱", "🐈")

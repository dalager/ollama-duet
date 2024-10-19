# run ollama serve and pull llama3.2
# install litellm, `pip install 'litellm[proxy]'` and run with
# `litellm --model ollama/llama3.2`


from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

import asyncio

from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    OpenAIChatCompletionClient,
    SystemMessage,
    UserMessage,
)


from autogen_core.application import SingleThreadedAgentRuntime
from autogen_core.base import MessageContext
from autogen_core.components import (
    DefaultTopicId,
    RoutedAgent,
    default_subscription,
    message_handler,
    type_subscription,
)

import logging
from autogen_agentchat import EVENT_LOGGER_NAME
from autogen_agentchat.logging import ConsoleLogHandler
from autogen_core.components.models import LLMMessage

logger = logging.getLogger(EVENT_LOGGER_NAME)
logger.addHandler(ConsoleLogHandler())
logger.setLevel(logging.INFO)


@dataclass
class Message:
    content: str


class GroupChatMessage(BaseModel):
    body: LLMMessage


class RequestToSpeak(BaseModel):
    pass


@default_subscription
class GroupChatManager(RoutedAgent):
    def __init__(self, participant_topic_types: List[str]) -> None:
        super().__init__("Group chat manager")
        self._num_rounds = 0
        self._participant_topic_types = participant_topic_types
        self._chat_history: List[GroupChatMessage] = []

    @message_handler
    async def handle_message(
        self, message: GroupChatMessage, ctx: MessageContext
    ) -> None:
        self._chat_history.append(message)
        assert isinstance(message.body, UserMessage)
        if message.body.source == "Editor" and "APPROVE" in message.body.content:
            return
        speaker_topic_type = self._participant_topic_types[
            self._num_rounds % len(self._participant_topic_types)
        ]
        self._num_rounds += 1
        await self.publish_message(
            RequestToSpeak(), DefaultTopicId(type=speaker_topic_type)
        )


@default_subscription
@type_subscription("writer")
class WriterAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient, name: str) -> None:
        super().__init__("A writer")
        self._model_client = model_client
        self.name = name
        self._chat_history: List[LLMMessage] = [
            SystemMessage(
                "You are {name}, working in a writer's room for a very cerebral drama."
            )
        ]

    @message_handler
    async def handle_message(
        self, message: GroupChatMessage, ctx: MessageContext
    ) -> None:
        self._chat_history.append(message.body)

    @message_handler
    async def handle_request_to_speak(
        self, message: RequestToSpeak, ctx: MessageContext
    ) -> None:
        # print the context
        completion = await self._model_client.create(self._chat_history)
        assert isinstance(completion.content, str)
        self._chat_history.append(
            AssistantMessage(content=completion.content, source="Writer")
        )
        print(f"\n{'-'*80}\n{self.name}:\n{completion.content}")
        await self.publish_message(
            GroupChatMessage(
                body=UserMessage(content=completion.content, source="Writer")
            ),
            DefaultTopicId(),
        )


def get_model_client() -> OpenAIChatCompletionClient:
    "Mimic OpenAI API using Local LLM Server."
    return OpenAIChatCompletionClient(
        model="gpt-4o",  # Need to use one of the OpenAI models as a placeholder for now.
        api_key="NotRequiredSinceWeAreLocal",
        base_url="http://localhost:4000",
        temperature=0.3,
    )


async def main():
    runtime = SingleThreadedAgentRuntime()

    await WriterAgent.register(
        runtime,
        "cathy",
        lambda: WriterAgent(model_client=get_model_client(), name="cathy"),
    )

    await WriterAgent.register(
        runtime,
        "joe",
        lambda: WriterAgent(model_client=get_model_client(), name="joe"),
    )

    await GroupChatManager.register(
        runtime,
        "group_chat_manager",
        lambda: GroupChatManager(
            participant_topic_types=["writer"],
        ),
    )

    runtime.start()
    await runtime.publish_message(
        GroupChatMessage(
            body=UserMessage(
                content="Mike enters his house and meets his wife Anne wearing cat's ears. "
                "He has been drinking and a lot of bottled up resentment makes Anne react.",
                source="User",
            )
        ),
        DefaultTopicId(),
    )
    await runtime.stop_when_idle()


asyncio.run(main())

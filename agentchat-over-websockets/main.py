import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager, ConversableAgent

import autogen
from autogen.io.websockets import IOWebsockets

# have your keys set up in .env file in the main project folder
load_dotenv()
api_key = os.getenv('OPENAI_KEY')
claude_key = os.getenv('CLAUDE_KEY')

cl = [{"model": "gpt-4o-mini", "api_key": api_key}]
cl_full = [{"model": "gpt-4o", "api_key": api_key}]
cl_claude = [{"api_type": "anthropic",
              "model": "claude-3-5-sonnet-20241022",
              "api_key": claude_key}]

target_language = "Estonian"


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "tags": ["gpt-4o-mini"],
    },
)

PORT = 8001


def on_connect(iostream: IOWebsockets) -> None:
    print(
        f" - on_connect(): Connected to client using IOWebsockets {iostream}",
        flush=True,
    )

    print(" - on_connect(): Receiving message from client.", flush=True)

    # 1. Receive Initial Message
    initial_msg = iostream.input()
    print(f"{initial_msg=}")

    try:
        coordinator_agent = ConversableAgent(
            name="Coordinator_Agent",
            system_message="You output only the text to be translated into "+target_language+". If there already is an "+target_language+" translation,\
                you return the "+target_language+" translation.\
                Output in the following format:\
                Correct text:",
            llm_config={"config_list": cl_full},
            human_input_mode="NEVER",
        )

        translate_agent = ConversableAgent(
            name="Translate_Agent",
            system_message="You translate a text from English to "+target_language+" and return the translated text. \
                If the text is already in "+target_language+", you return the same text.\
                    Output in the following format:\
                        Translation:",
            llm_config={"config_list": cl_full},
            human_input_mode="NEVER",
        )

        grammar_agent = ConversableAgent(
            name="Grammar_Agent",
            system_message="You validate and fix "+target_language+" grammar in the text. You return only explanation and the \
            corrected text in a following format: \
            Explanation:\
            Correct text:",
            llm_config={"config_list": cl},
            human_input_mode="NEVER",
        )

        subject_agent = ConversableAgent(
            name="Subject_Agent",
            system_message="If the text addressed a person, you validate that the translated message is addressing the person informally and directly \
                the way that is appropriate to "+target_language+". \
            If the text misses the word 'you' but it would be appropriate in a given language, you add it.\
            If the text addresses person formally where formal addressing is not required in "+target_language+", change it to informal. \
            Correct the translation if necessary. \
            You return only explanation and the corrected text in a following format: \
            Explanation:\
            Correct text:",
            llm_config={"config_list": cl},
            human_input_mode="NEVER",
        )

        time_agent = ConversableAgent(
            name="Time_Agent",
            system_message="You validate that the translated "+target_language+" text is in the same tense as the original English text. \
                Return the explanation and corrected text in the following format: \
                    Explanation:\
                    Correct text:",
            llm_config={"config_list": cl},
            human_input_mode="NEVER",
        )

        validator_agent = ConversableAgent(
            name="Validator_Agent",
            system_message="You validate that the original English text and "+target_language+" text have the same meaning. \
                Return the explanation and corrected text in a following format: \
                    Explanation:\
                    Correct text:",
            llm_config={"config_list": cl},
            human_input_mode="NEVER",
        )

        # Figure of speech agent that checks if the text contains any idioms or figures of speech and corrects them if necessary.
        figure_of_speech_agent = ConversableAgent(
        name="Figure_of_Speech_Agent",
        system_message="You check if the text contains any idioms or figures of speech and correct them if necessary. \
            Make sure that the corrected text is still idiomatic in the "+target_language+". \
            Return the explanation and corrected text in the following format: \
                Explanation:\
                Correct text:",
        llm_config={"config_list": cl},
        human_input_mode="NEVER",
        )

        politeness_agent = ConversableAgent(
            name="Politeness_Agent",
            system_message="You check if the dialogue is polite and respectful in "+target_language+". \
                If the text is impolite or disrespectful, correct it to be polite and respectful. \
                Return the explanation and corrected text in the following format: \
                    Explanation:\
                    Correct text:",
            llm_config={"config_list": cl},
            human_input_mode="NEVER",
        )

        cultural_reference_agent = ConversableAgent(
            name="Cultural_Reference_Agent",
            system_message="You check if the text contains any unique cultural references to the source language. \
            If so, try to replace it with an equivalent reference to the "+target_language+" culture and language. \
            Return the explanation and corrected text in the following format: \
                Explanation:\
                Correct text:",
            llm_config={"config_list": cl_claude},
            human_input_mode="NEVER",
        )

        group_chat = GroupChat(
            agents=[coordinator_agent, politeness_agent, translate_agent,cultural_reference_agent, grammar_agent, subject_agent, time_agent, validator_agent, figure_of_speech_agent],
            messages=[],
            max_round=10,
            send_introductions=True,
            speaker_selection_method="auto",
            select_speaker_auto_verbose=False
        )

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": cl_full},
        )
        # 5. Initiate conversation
        print(
            f" - on_connect(): Initiating chat with agent {coordinator_agent} using message '{initial_msg}'",
            flush=True,
        )

        coordinator_agent.initiate_chat(
            group_chat_manager,
            #message="I am sad today, can you cheer me up. Can you smell the flowers?",
            message=initial_msg,
            summary_method="reflection_with_llm",
            summary_args = {"summary_prompt": "Return only the last best version of the translated text and nothing else."},
        )
    except Exception as e:
        print(f" - on_connect(): Exception: {e}", flush=True)
        raise e


class MyRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=Path(__file__).parent / "website_files" / "templates",
            **kwargs,
        )

    def do_GET(self):
        if self.path == "/":
            self.path = "/chat.html"
        return SimpleHTTPRequestHandler.do_GET(self)


handler = MyRequestHandler

with IOWebsockets.run_server_in_thread(on_connect=on_connect, port=8080) as uri:
    print(f"Websocket server started at {uri}.", flush=True)

    with HTTPServer(("", PORT), handler) as httpd:
        print("HTTP server started at http://localhost:" + str(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(" - HTTP server stopped.", flush=True)

# It is nice summer, so much snow!
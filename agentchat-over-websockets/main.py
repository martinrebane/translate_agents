from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime

import autogen
from autogen.io.websockets import IOWebsockets


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
        # 2. Instantiate ConversableAgent
        agent = autogen.ConversableAgent(
            name="chatbot",
            system_message="Complete a task given to you and reply TERMINATE when the task is done. If asked about the weather, use tool 'weather_forecast(city)' to get the weather forecast for a city.",
            llm_config={
                "config_list": config_list,
                "stream": False,
            },
        )

        # 3. Define UserProxyAgent
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            system_message="A proxy for the user.",
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("TERMINATE"),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config=False,
        )

        # 4. Define Agent-specific Functions
        def weather_forecast(city: str) -> str:
            return f"The weather forecast for {city} at {datetime.now()} is sunny."

        autogen.register_function(
            weather_forecast,
            caller=agent,
            executor=user_proxy,
            description="Weather forecast for a city",
        )

        # 5. Initiate conversation
        print(
            f" - on_connect(): Initiating chat with agent {agent} using message '{initial_msg}'",
            flush=True,
        )
        user_proxy.initiate_chat(  # noqa: F704
            agent,
            message=initial_msg,
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

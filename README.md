# Tartu Science Park port of agentchat UI for localisation agents

* you do not need to configure your models in OAI_CONFIG_LIST, use .env file instead
* copy .env_sample to .env and add your AI model keys
 * in case you do not have access to several different AI models, use just one
 * the model for each agent is selected by `llm_config={"config_list": cl}` in main.py - update `cl`, `cl_full` and `cl_claude` according to your needs per each agent
* install `pip install python-dotenv`
* agent code is in agentchat-over-websockets/main.py
* user interface template is in agentchat-over-websockets/website_files/templates/chat.html
* otherwise follow the instructions below

# Agentchat over websockets

This project demonstrates how to use the [`IOStream`](https://docs.ag2.ai/docs/reference/io/websockets) class for real-time input and output streaming with [WebSockets](https://websockets.readthedocs.io/en/stable/), enabling responsive and efficient web clients by eliminating the need for server polling.

## **Prerequisites**

Before you begin, ensure you have the following:
- **Python 3.9+**: The project was tested with `3.9`. Download [here](https://www.python.org/downloads/).
- **An OpenAI account and an OpenAI API Key.** You can sign up [here](https://platform.openai.com/).
  - **OpenAI Realtime API access.**

## **Local Setup**

Follow these steps to set up the project locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/ag2ai/agentchat-over-websockets.git
cd agentchat-over-websockets
```

### **2. Set Up Environment Variables**
Create a `OAI_CONFIG_LIST` file based on the provided `OAI_CONFIG_LIST_sample`:
```bash
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
```
In the OAI_CONFIG_LIST file, update the `api_key` to your OpenAI API key.

### (Optional) Create and use a virtual environment

To reduce cluttering your global Python environment on your machine, you can create a virtual environment. On your command line, enter:

```
python3 -m venv env
source env/bin/activate
```

### **3. Install Dependencies**
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### **4. Start the Server**
Run the `main.py` file:
```bash
python agentchat-over-websockets/main.py
```

## **Test the App**
With the server running, open the client application in your browser by navigating to [http://localhost:8001/](http://localhost:8001/). And send a message to the chat and watch the conversation between agents roll out in your browser.

## **License**
This project is licensed under the [Apache 2.0 license](LICENSE).

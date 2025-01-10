
# Agentchat over websockets

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
This project is licensed under the [MIT License](LICENSE).

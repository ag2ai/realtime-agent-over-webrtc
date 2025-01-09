
# **RealtimeAgent over WebRTC**

This project demonstrates how to create a voice assistant using Python, [FastAPI](https://fastapi.tiangolo.com/) and an [AG2 RealtimeAgent](https://docs.ag2.ai/docs/reference/agentchat/realtime_agent/realtime_agent#realtimeagent). The application streams audio from a client browser to [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime-webrtc) directly over [WebRTC](https://webrtc.org/).

## **Key Features**
- **WebRTC Audio Streaming**: Direct real-time audio streaming between the browser and OpenAI API over [WebRTC](https://webrtc.org/).
- **FastAPI Integration**: A lightweight Python backend for handling [RealtimeAgent](https://docs.ag2.ai/docs/reference/agentchat/realtime_agent/realtime_agent#realtimeagent) connection and function calling.

## **Prerequisites**

Before you begin, ensure you have the following:
- **Python 3.9+**: The project was tested with `3.9`. Download [here](https://www.python.org/downloads/).
- **An OpenAI account and an OpenAI API Key.** You can sign up [here](https://platform.openai.com/).
  - **OpenAI Realtime API access.**

## **Local Setup**

Follow these steps to set up the project locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/ag2ai/realtime-agent-over-webrtc.git
cd realtime-agent-over-webrtc
```

### **2. Set Up Environment Variables**
Create a `OAI_CONFIG_LIST` file based on the provided `OAI_CONFIG_LIST_sample`:
```bash
cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
```
In the OAI_CONFIG_LIST file, update the `api_key` to your OpenAI API key.

#### Important note

Currenlty WebRTC can be used only by API keys the begin with:

```
sk-proj
```

Other keys may result internal server error  (500) on OpenAI server. For more details see:
https://community.openai.com/t/realtime-api-create-sessions-results-in-500-internal-server-error/1060964/5

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
Run the application with [Uvicorn](https://www.uvicorn.org/):
```bash
uvicorn realtime_over_webrtc.main:app --port 5050
```

## **Test the App**
With the server running, open the client application in your browser by navigating to [http://localhost:5050/start-chat/](http://localhost:5050/start-chat/). Speak into your microphone, and the AI assistant will respond in real time.

## **License**
This project is licensed under the [MIT License](LICENSE).

# voca_grow_agent




## Setup

**clone**
```
git clone https://github.com/Mahmood-Anaam/voca_grow_agent.git
cd voca_grow_agent
```

**.env file**

```
LIVEKIT_URL=YOUR_LIVEKIT_URL_HERE
LIVEKIT_API_KEY=YOUR_LIVEKIT_API_KEY_HERE
LIVEKIT_API_SECRET=YOUR_LIVEKIT_API_SECRET_HERE
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```
**install dependencies**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Finally, run the agent with:**

```
python main.py dev
```
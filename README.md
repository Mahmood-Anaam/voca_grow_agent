# VocaGrow Agent

**VocaGrow Agent** is an AI-powered speech coaching assistant designed specifically for children. Built using **LiveKit Agents** and **Google Gemini Flash 2.0**, it helps children improve their pronunciation by dynamically adapting to their selected **language**, **character**, and **learning activity**. The agent offers cheerful, interactive guidance to make speech practice fun and engaging.

## ✨ Features

- Supports **Arabic** and **English**.
- Adapts persona based on selected **character** (e.g., Woody, Elsa, Spiderman, Snow).
- Focused exclusively on **speech pronunciation practice**.
- Real-time audio streaming via **LiveKit**.
- Dynamic conversation generation using **Google Gemini Live API**.
- Custom **voice selection** based on character's gender.
- Automatic **noise cancellation** support (optional if plugin available).

## 📋 Requirements

- Python 3.9 or higher
- LiveKit Cloud or Self-hosted Server
- Google Cloud API Key with Gemini access

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mahmood-Anaam/voca_grow_agent.git
cd voca_grow_agent
```

### 2. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```plaintext
LIVEKIT_URL=YOUR_LIVEKIT_URL_HERE
LIVEKIT_API_KEY=YOUR_LIVEKIT_API_KEY_HERE
LIVEKIT_API_SECRET=YOUR_LIVEKIT_API_SECRET_HERE
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Agent

```bash
python main.py dev
```



## 🎯 How It Works

- The agent connects to a **LiveKit room** and waits for a child participant to join.
- The child must send the following **participant attributes**:
  - `lang` – Language (`"ar"` or `"en"`)
  - `character` – Character name (`"Woody"`, `"Elsa"`, `"Spiderman"`, `"Snow"`)
  - `activitie` – Selected learning activity (e.g., `"Colors"`, `"Shapes"`)
- Based on these attributes:
  - A **custom system prompt** is dynamically created (Arabic or English).
  - A **specific voice** is selected matching the character's gender:

    | Character   | Voice    |
    |-------------|----------|
    | Woody       | Puck     |
    | Spiderman   | Fenrir   |
    | Snow        | Aoede    |
    | Elsa        | Kore     |

- The agent then:
  - Fully adopts the child's selected character persona.
  - Pronounces a word related to the selected activity in the chosen language.
  - Asks the child to repeat the word.
  - Listens to the child's pronunciation attempt.
  - Provides positive feedback if the pronunciation is correct.
  - Gently repeats and encourages if the pronunciation needs improvement.
  - Avoids unrelated questions or topics.
  - Keeps interactions short, cheerful, and focused on pronunciation practice.



## 📢 Important Notes

- If attributes are **not received within 30 seconds**, the agent uses default settings:  
  (`lang="ar"`, `character="Spiderman"`, `activitie="Shapes"`).
- Noise cancellation is **enabled if available** (fallbacks gracefully if the plugin is missing).
- The agent **only** focuses on pronunciation practice — no unrelated conversations are allowed.
- Real-time event handlers monitor when the child starts or stops speaking.
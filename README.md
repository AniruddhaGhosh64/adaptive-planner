# Adaptive Planner
*A real-time, AI-driven scheduling engine that dynamically re-routes your day around unexpected disruptions.*

**Adaptive Planner** is an intelligent scheduling API that leverages the power of AI to build, adjust, and optimize your daily plans dynamically. It understands your tasks, energy levels, and constraints to create realistic schedules—and can re-plan on the fly when life inevitably disrupts them.

## The Problem It Solves
Traditional calendars are rigid and don't reflect the realities of day-to-day life. When you oversleep, a meeting runs late, or your energy drops, static schedules fall apart. **Adaptive Planner** aims to solve this by providing dynamic time-boxing that acts like a personal assistant—not just putting blocks on a timeline, but constantly evaluating when to do tasks based on current contexts, shifting priorities seamlessly.

## Live Demo
You can try the live API and interactive UI deployed on Google Cloud Run here:
[Adaptive Planner UI](https://adaptive-planner-910282726941.asia-south1.run.app/ui)

## Demo Flow
1. **Input Parameters**: Provide your pending tasks, hard constraints, and current energy levels into the UI.
2. **Initial Generation**: The system evaluates your requirements and generates a highly optimized, conflict-free JSON schedule.
3. **Inject Disruption**: Simulate a real-world event (e.g., "Woke up 2 hours late").
4. **Adaptive Adjustment**: The engine instantly recalculates your timeline, preserving critical tasks while safely sliding or deferring less important ones.

## Features
- **Plan Generation (`/plan-day`)**: Ingests task arrays, time constraints, and energy metrics to intelligently synthesize a strict, continuous, and non-overlapping schedule.
- **Dynamic Re-routing (`/adjust-plan`)**: Accepts an existing schedule state alongside a disruption event payload, intelligently shuffling and re-prioritizing time blocks to maintain operational stability.
- **Smart Adaptive Planning (`/smart-plan`)**: A unified pipeline that orchestrates both generation and disruption logic in a single request for seamless UI integration and testing.

## How It Works
Under the hood, the application converts your structured endpoints and variables into highly engineered prompt schemas. It utilizes strict formatting constraints alongside Google's **Gemini AI** to reason over time blocks. The responses are consistently validated as raw, actionable JSON formats without the "AI fluff," acting entirely programmatically.

## Tech Stack
- **FastAPI**: For high-performance, asynchronous endpoints and automatic interactive documentation.
- **Native Web UI**: A minimal, dependency-free frontend utilizing vanilla HTML/CSS/JS and the Fetch API to visualize schedule mutations.
- **Pydantic**: Robust data validation and strict type enforcement across API boundaries.
- **Google Gemini API**: Utilizing the `gemini-2.5-flash` model for exceptionally rapid and intelligent reasoning constraints.

## Example

**Input to `/plan-day`:**
```json
{
  "tasks": ["Write report", "Reply to emails", "Grocery shopping"],
  "constraints": "Have a hard stop at 6 PM.",
  "energy": "Low energy morning, feeling sluggish."
}
```

**Output:**
```json
{
  "plan": [
    {
      "time": "10:00 AM - 11:00 AM",
      "activity": "Reply to emails",
      "notes": "Low effort task for sluggish morning."
    },
    {
      "time": "11:15 AM - 01:15 PM",
      "activity": "Write report",
      "notes": "Tackling deep work as energy improves before lunch."
    },
    {
      "time": "05:00 PM - 06:00 PM",
      "activity": "Grocery shopping",
      "notes": "Completing before the 6 PM hard stop constraint."
    }
  ],
  "message": "Plan generated successfully"
}
```

## Setup Instructions

**1. Clone the repository and navigate into the project:**
```bash
git clone <your-repo-url>
cd adaptive-planner
```

**2. Set up your virtual environment:**
```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables:**
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**5. Run the Local Development Server:**
```bash
uvicorn main:app --reload
```
You can now access the interactive UI at `http://127.0.0.1:8000/ui` to test out the application directly from your browser!

## Future Improvements
- **Google Calendar/Outlook Integration**: Directly pushing and reading existing events to work around permanent external constraints.
- **Persistent Logic**: Utilize a database to save "Past Versions" of a plan so users can rollback if needed.
- **Multi-Day Planning**: Extending block planning contexts logic over a week, preventing burnout during high-stress periods.

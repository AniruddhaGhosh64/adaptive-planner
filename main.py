import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI(title="Adaptive Planner")

# Request schema
class PlanRequest(BaseModel):
    tasks: List[str]
    constraints: str
    energy: str

class AdjustRequest(BaseModel):
    current_plan: List[dict]
    event: str

@app.get("/")
def read_root():
    return {"status": "API is running"}

def get_gemini_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable not set"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def parse_gemini_response(response):
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON returned by AI: {raw_text}"
        )

def generate_plan_logic(request: PlanRequest) -> List[dict]:
    model = get_gemini_model()
    prompt = f"""
You are a strict planning assistant.

Create a realistic daily schedule.

INPUT:
Tasks: {', '.join(request.tasks)}
Constraints: {request.constraints}
Energy Level: {request.energy}

RULES:
- Respect all constraints strictly
- Distribute tasks realistically
- If energy is low, reduce heavy tasks
- Include breaks if needed
- Do not overlap time blocks

OUTPUT FORMAT (STRICT JSON ONLY):
[
  {{
    "time": "HH:MM AM - HH:MM AM",
    "activity": "task description",
    "notes": "reasoning"
  }}
]

Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return parse_gemini_response(response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


def adjust_plan_logic(current_plan: List[dict], event: str) -> List[dict]:
    model = get_gemini_model()
    prompt = f"""
You are a strict planning assistant.

Adjust the existing schedule based on a new disruption/event.

INPUT:
Current Plan: {json.dumps(current_plan, indent=2)}
Disruption/Event: {event}

RULES:
- Keep important tasks
- Reschedule missed tasks
- Maintain realistic timing
- Avoid overlapping time blocks
- Respect energy levels if possible

OUTPUT FORMAT (STRICT JSON ONLY):
[
  {{
    "time": "HH:MM AM - HH:MM AM",
    "activity": "task",
    "notes": "reason for adjustment"
  }}
]

Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return parse_gemini_response(response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to adjust plan: {str(e)}")


@app.post("/plan-day")
def plan_day(request: PlanRequest):
    plan = generate_plan_logic(request)
    return {
        "plan": plan,
        "message": "Plan generated successfully"
    }

@app.post("/adjust-plan")
def adjust_plan(request: AdjustRequest):
    return adjust_plan_logic(request.current_plan, request.event)

@app.post("/smart-plan")
def smart_plan(request: PlanRequest):
    original_plan = generate_plan_logic(request)
    event = "User woke up late and missed first task"
    adjusted_plan = adjust_plan_logic(original_plan, event)
    
    return {
        "original_plan": original_plan,
        "adjusted_plan": adjusted_plan
    }
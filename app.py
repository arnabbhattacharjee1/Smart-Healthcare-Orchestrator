from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from adk.core import Message
from main import TriageOrchestrator
from pydantic import BaseModel

app = FastAPI(title="ADK Healthcare Orchestrator")

# We mount the web directory to serve static HTML/CSS/JS
app.mount("/static", StaticFiles(directory="web"), name="static")

class TriageRequest(BaseModel):
    complaint: str

class TrackedOrchestrator(TriageOrchestrator):
    """An extension of the Base Orchestrator that collects agent traces."""
    def run_plan_with_trace(self, patient_input: str):
        trace = []
        
        # 1. Symptom Agent
        trace.append({"agent": "Orchestrator", "action": "Routing to SymptomAgent", "data": patient_input})
        msg_1 = Message(self.name, "SymptomAgent", patient_input)
        response_1 = self.route_message("SymptomAgent", msg_1)
        extracted_symptoms = response_1.content
        trace.append({"agent": "SymptomAgent", "action": "Extracted Structured Symptoms", "data": extracted_symptoms})
        
        # 2. Triage Agent
        trace.append({"agent": "Orchestrator", "action": "Routing to TriageAgent", "data": extracted_symptoms})
        msg_2 = Message(self.name, "TriageAgent", extracted_symptoms)
        response_2 = self.route_message("TriageAgent", msg_2)
        triage_evaluation = response_2.content
        trace.append({"agent": "TriageAgent", "action": "Evaluated Severity", "data": triage_evaluation})
        
        # 3. Routing Agent
        trace.append({"agent": "Orchestrator", "action": "Routing to RoutingAgent", "data": triage_evaluation})
        msg_3 = Message(self.name, "RoutingAgent", triage_evaluation)
        response_3 = self.route_message("RoutingAgent", msg_3)
        final_decision = response_3.content
        trace.append({"agent": "RoutingAgent", "action": "Final Routing Decision", "data": final_decision})
        
        return {
            "final_decision": final_decision,
            "trace": trace
        }

@app.post("/api/triage")
async def perform_triage(request: TriageRequest):
    orchestrator = TrackedOrchestrator()
    try:
        result = orchestrator.run_plan_with_trace(request.complaint)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)

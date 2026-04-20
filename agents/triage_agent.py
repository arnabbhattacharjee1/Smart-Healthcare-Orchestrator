from adk.core import Agent, Message
from adk.llm import call_gemini
from typing import List
import json

class TriageAgent(Agent):
    def __init__(self):
        super().__init__("TriageAgent", "Evaluates severity using Gemini 2.5 Flash Lite reasoning.")
        
    def execute(self, message: Message) -> Message:
        symptoms: List[str] = message.content
        symptoms_text = ", ".join(symptoms)
        
        system_instruction = (
            "You are a medical triage agent. Given a list of symptoms, determine the severity as strictly 'Low', 'Medium', or 'High'. "
            "Your output must be strictly valid JSON without any markdown block formatting. "
            "Format: {\"classification\": \"High/Medium/Low\", \"reasoning\": \"1 sentence explanation\"}. "
            "Example: {\"classification\": \"High\", \"reasoning\": \"Chest pain indicates a potential cardiac event requiring immediate attention.\"}"
        )
        
        try:
            llm_response = call_gemini(system_instruction, symptoms_text)
            clean_response = llm_response.strip().removeprefix("```json").removesuffix("```").strip()
            result = json.loads(clean_response)
            
            classification = result.get("classification", "Low")
            reasoning = [result.get("reasoning", "No valid reasoning provided.")]
            # Arbitrary score for backward compatibility with RoutingAgent logic which we might skip using
            severity_score = 5 if classification == "High" else (3 if classification == "Medium" else 1)
        except Exception as e:
            print(f"[{self.name}] Error parsing LLM response: {e}")
            classification = "Medium" # Fallback
            reasoning = ["Error performing triage."]
            severity_score = 3
            
        print(f"[{self.name}] Reasoned Severity: {classification}")
        
        return Message(
            sender=self.name,
            receiver=message.sender,
            content={
                "severity_score": severity_score,
                "classification": classification,
                "reasoning": reasoning
            }
        )

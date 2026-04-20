from adk.core import Agent, Message
from typing import List

class TriageAgent(Agent):
    def __init__(self):
        super().__init__("TriageAgent", "Evaluates severity using rules and mock LLM reasoning.")
        
        # Simulated predefined rules
        self.critical_symptoms = {"chest pain", "shortness of breath", "bleeding"}
        self.moderate_symptoms = {"fever", "dizziness", "pain"}
        
    def execute(self, message: Message) -> Message:
        symptoms: List[str] = message.content
        
        severity_score = 0
        reasoning = []
        
        for symptom in symptoms:
            if symptom in self.critical_symptoms:
                severity_score += 5
                reasoning.append(f"CRITICAL: '{symptom}' requires immediate attention.")
            elif symptom in self.moderate_symptoms:
                severity_score += 2
                reasoning.append(f"MODERATE: '{symptom}' increases priority.")
            else:
                severity_score += 1
                reasoning.append(f"MILD: '{symptom}' is of standard priority.")
                
        # Normalize severity classification
        classification = "Low"
        if severity_score >= 5:
            classification = "High"
        elif severity_score >= 3:
            classification = "Medium"
            
        print(f"[{self.name}] Reasoned Severity: {classification} (Score: {severity_score})")
        
        return Message(
            sender=self.name,
            receiver=message.sender,
            content={
                "severity_score": severity_score,
                "classification": classification,
                "reasoning": reasoning
            }
        )

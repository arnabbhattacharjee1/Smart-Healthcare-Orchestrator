from adk.core import Agent, Message
from typing import List
import re

class SymptomAgent(Agent):
    def __init__(self):
        super().__init__("SymptomAgent", "Extracts structured symptoms from free-text using heuristics/rules.")
        
        # A simple simulated dictionary of possible symptoms
        self.known_symptoms = [
            "fever", "headache", "cough", "chest pain", "shortness of breath",
            "nausea", "dizziness", "bleeding", "rash", "fatigue", "pain"
        ]

    def execute(self, message: Message) -> Message:
        text = str(message.content).lower()
        
        # Simulated "LLM"/Extraction Logic: We just match known keywords for demonstration
        extracted_symptoms = []
        for symptom in self.known_symptoms:
            if re.search(r'\b' + re.escape(symptom) + r'\b', text):
                extracted_symptoms.append(symptom)
                
        # If no symptoms directly matched, generic fallback
        if not extracted_symptoms:
            extracted_symptoms.append("unknown or vague discomfort")
            
        print(f"[{self.name}] Extracted symptoms: {extracted_symptoms}")
            
        return Message(
            sender=self.name,
            receiver=message.sender,
            content=extracted_symptoms,
            metadata={"status": "success"}
        )

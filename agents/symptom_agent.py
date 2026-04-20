from adk.core import Agent, Message
from adk.llm import call_gemini
import json

class SymptomAgent(Agent):
    def __init__(self):
        super().__init__("SymptomAgent", "Extracts structured symptoms from free-text using Gemini 2.5 Flash Lite.")

    def execute(self, message: Message) -> Message:
        text = str(message.content)
        
        system_instruction = (
            "You are a medical assistant agent. Extract symptoms from the user's input. "
            "Respond ONLY with a valid JSON array of strings containing the symptoms. "
            "For example: [\"fever\", \"headache\", \"chest pain\"]. "
            "Do not include markdown blocks like ```json."
        )
        
        try:
            llm_response = call_gemini(system_instruction, text)
            # Remove any trailing/leading markdown just in case the model adds it
            clean_response = llm_response.strip().removeprefix("```json").removesuffix("```").strip()
            extracted_symptoms = json.loads(clean_response)
            if not isinstance(extracted_symptoms, list):
                extracted_symptoms = [str(extracted_symptoms)]
        except Exception as e:
            print(f"[{self.name}] Error parsing LLM response: {e}")
            print(f"[{self.name}] Raw Response was: {llm_response if 'llm_response' in locals() else 'Request failed'}")
            extracted_symptoms = ["evaluation error"]
            
        print(f"[{self.name}] Extracted symptoms: {extracted_symptoms}")
            
        return Message(
            sender=self.name,
            receiver=message.sender,
            content=extracted_symptoms,
            metadata={"status": "success"}
        )

from adk.core import Orchestrator, Message
from agents.symptom_agent import SymptomAgent
from agents.triage_agent import TriageAgent
from agents.routing_agent import RoutingAgent

class TriageOrchestrator(Orchestrator):
    def __init__(self):
        super().__init__("MedicalTriageOrchestrator")
        
        # Register the sub-agents
        self.register_agent(SymptomAgent())
        self.register_agent(TriageAgent())
        self.register_agent(RoutingAgent())

    def run_plan(self, patient_input: str) -> str:
        print(f"\n[{self.name}] Starting triage for complaint: '{patient_input}'")
        
        # Step 1: Call Symptom Agent
        msg_1 = Message(self.name, "SymptomAgent", patient_input)
        response_1 = self.route_message("SymptomAgent", msg_1)
        extracted_symptoms = response_1.content
        
        # Step 2: Call Triage Agent
        msg_2 = Message(self.name, "TriageAgent", extracted_symptoms)
        response_2 = self.route_message("TriageAgent", msg_2)
        triage_evaluation = response_2.content
        
        # Step 3: Call Routing Agent
        msg_3 = Message(self.name, "RoutingAgent", triage_evaluation)
        response_3 = self.route_message("RoutingAgent", msg_3)
        final_decision = response_3.content
        
        print(f"[{self.name}] Triage completed.")
        return final_decision


def main():
    orchestrator = TriageOrchestrator()
    
    # Test Scenario 1: Emergency
    print("=" * 60)
    complaint_1 = "I woke up with severe chest pain and I have shortness of breath."
    result_1 = orchestrator.run_plan(complaint_1)
    print(f"\nFinal Recommendation: {result_1}")
    
    # Test Scenario 2: Moderate
    print("\n" + "=" * 60)
    complaint_2 = "I've had a high fever for two days and some headache."
    result_2 = orchestrator.run_plan(complaint_2)
    print(f"\nFinal Recommendation: {result_2}")
    
    # Test Scenario 3: Mild
    print("\n" + "=" * 60)
    complaint_3 = "Just feeling some mild fatigue and my toe has a rash."
    result_3 = orchestrator.run_plan(complaint_3)
    print(f"\nFinal Recommendation: {result_3}")

if __name__ == "__main__":
    main()

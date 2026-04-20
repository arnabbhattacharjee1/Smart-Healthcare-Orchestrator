from adk.core import Agent, Message

class RoutingAgent(Agent):
    def __init__(self):
        super().__init__("RoutingAgent", "Decides whether to route to Emergency vs Non-emergency.")
        
    def execute(self, message: Message) -> Message:
        triage_data = message.content
        classification = triage_data.get("classification", "Low")
        
        # Decision Logic
        if classification == "High":
            decision = "EMERGENCY - Route to nearest hospital or ER immediately."
        elif classification == "Medium":
            decision = "URGENT - Schedule same-day clinic visit or urgent care."
        else:
            decision = "NON-EMERGENCY - Recommend rest and schedule routine follow-up."
            
        print(f"[{self.name}] Routing Decision: {decision}")
        
        return Message(
            sender=self.name,
            receiver=message.sender,
            content=decision
        )

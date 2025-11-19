
from model.sales_agent_logic import scan_and_select_rfp

class MainOrchestrator:
    def __init__(self, rfp_source_file):
        self.rfp_source = rfp_source_file
        self.selected_rfp = None
        self.technical_response = None
        self.pricing_response = None

    def run_workflow(self):
        """
        Executes the entire RFP response workflow step-by-step.
        """
        print("""
## Starting New RFP Response Workflow... ##
""") 

    
        print("--- [Step 1: Sales Agent] ---")
        self.selected_rfp = scan_and_select_rfp(self.rfp_source)

    
        if not self.selected_rfp:
            print("""
##  Workflow ENDED: No actionable RFP found. ##
""") 
            return

        print("""
📬 Orchestrator: Received RFP from Sales Agent.
""")
        print(f"   - RFP Title: {self.selected_rfp['title']}")


        print("""
--- [Step 2: Technical Agent] ---""")
        print("   - Task: Analyze technical specs and match products.")
        print("   - Status: PENDING...")
     

 
        print("""
--- [Step 3: Pricing Agent] ---""")
        print("   - Task: Calculate material and service costs.")
        print("   - Status: PENDING...")
      
        print("""
--- [Step 4: Final Consolidation] ---""") 
        print("   - Task: Combine all agent responses into a final summary.")
        print("   - Status: PENDING...")
        
        
        print("""
##  Workflow Paused: Waiting for Technical & Pricing Agents to be built. ##
""") 



if __name__ == "__main__":
 
    orchestrator = MainOrchestrator(rfp_source_file='rfp_page_1.html')
    orchestrator.run_workflow()

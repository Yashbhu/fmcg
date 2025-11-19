import pandas as pd
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from sales_agent_logic import scrape_all_tenders as scan_and_select_rfp
from technical_agent_logic import analyze_rfp_specs
from pricing_agent_logic import calculate_pricing


class RfpWorkflowState(TypedDict):
    selected_rfp: Optional[dict]
    technical_analysis: Optional[pd.DataFrame]
    final_pricing: Optional[pd.DataFrame]
    error: str | None


def sales_node(state):
    rfp = scan_and_select_rfp()
    return {"selected_rfp": rfp} if rfp else {"error": "No actionable RFP found."}


def technical_node(state):
    analysis = analyze_rfp_specs(state["selected_rfp"])
    return {"technical_analysis": analysis} if analysis is not None else {"error": "Technical analysis failed."}


def pricing_node(state):
    pricing = calculate_pricing(state["technical_analysis"])
    return {"final_pricing": pricing} if pricing is not None else {"error": "Pricing calculation failed."}


def should_continue(state):
    return "end" if state.get("error") else "continue"


workflow = StateGraph(RfpWorkflowState)

workflow.add_node("sales", sales_node)
workflow.add_node("technical", technical_node)
workflow.add_node("pricing", pricing_node)

workflow.set_entry_point("sales")

workflow.add_conditional_edges("sales", should_continue, {"continue": "technical", "end": END})
workflow.add_conditional_edges("technical", should_continue, {"continue": "pricing", "end": END})
workflow.add_edge("pricing", END)

app = workflow.compile()

final_state = app.invoke({})

print("\n--- FINAL RFP RESPONSE SUMMARY ---")
if final_state.get("error"):
    print(f"\nWorkflow Halted with Error: {final_state['error']}")
else:
    print("\nWorkflow Completed Successfully!\n")
    print(final_state['final_pricing'][['RFP_Item', 'Recommended_SKU', 'Total_Cost']].to_string(index=False))

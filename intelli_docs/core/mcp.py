from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama
import traceback

class MCPStep(BaseModel):
    """
    Represents a single step in the Model Context Protocol
    """
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    prompt_template: str

class MCPPipeline:
    """
    Implements the Model Context Protocol for structured reasoning.
    
    The Model Context Protocol (MCP) acts as a transportation layer to help an agent access data from sources such as
        - DataBase
        - APIs
        - Local files
        - specific tools
        - Other Servers in turn

    MCP is hosted as an application and exposed to an agent like LLM - it follows a client-server architecture with the following main components
        - a host (mostly LLM applications)
        - a client (provides interfaces for 1:1 connection)
        - a server (separate processes that expose specific capability)
    MCP can in turn communicate with the agent and do specific actions so that the implementations are simplified
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        # Initialize Ollama without custom callbacks
        self.llm = Ollama(model=model_name)
        self.steps: List[MCPStep] = []
        
    def add_step(self, step: MCPStep):
        """
        Add a step to the MCP pipeline
        """
        self.steps.append(step)
        
    def execute(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the MCP pipeline with the given initial context
        """
        current_context = initial_context.copy()
        
        for step in self.steps:
            try:
                # Create a prompt from the step's template
                prompt = PromptTemplate(
                    template=step.prompt_template,
                    input_variables=list(step.input_schema.keys())
                )
                
                # Create chain
                chain = LLMChain(llm=self.llm, prompt=prompt)
                
                # Prepare inputs for the chain
                chain_inputs = {
                    k: current_context.get(k) for k in step.input_schema.keys()
                }
                
                # Execute step
                result = chain.run(**chain_inputs)
                
                # Parse the result into a structured format
                if step.name == "document_analysis":
                    # For document analysis, extract key (list of) points and the relevance score
                    key_points = [line.strip() for line in result.split('\n') if line.strip()]
                    relevance_score = 0.8  # Default relevance score
                    current_context.update({
                        step.name: {
                            "key_points": key_points,
                            "relevance_score": relevance_score
                        }
                    })
                elif step.name == "answer_generation":
                    # For answer generation, structure the response
                    current_context.update({
                        step.name: {
                            "answer": result,
                            "confidence": 0.9,  # Default confidence
                            "sources": current_context.get("document_content", "")
                        }
                    })
                else:
                    # For other steps, store the raw result
                    current_context.update({step.name: result})
                    
            except Exception as e:
                error_msg = f"Error in step {step.name}: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                # Provide a default response for failed steps
                if step.name == "document_analysis":
                    current_context.update({
                        step.name: {
                            "key_points": [f"Error analyzing document: {str(e)}"],
                            "relevance_score": 0.0
                        }
                    })
                elif step.name == "answer_generation":
                    current_context.update({
                        step.name: {
                            "answer": f"Error generating answer: {str(e)}",
                            "confidence": 0.0,
                            "sources": ""
                        }
                    })
                else:
                    current_context.update({step.name: f"Error: {str(e)}"})
            
        return current_context

# Somw MCP steps for document QA
DOCUMENT_ANALYSIS_STEP = MCPStep(
    name="document_analysis",
    description="Analyze the document content and extract key information",
    input_schema={
        "document_content": "str",
        "query": "str"
    },
    output_schema={
        "key_points": "List[str]",
        "relevance_score": "float"
    },
    prompt_template="""
    Analyze the following document content in relation to the query:
    
    Document: {document_content}
    Query: {query}
    
    Extract key points and determine relevance.
    Format your response as a list of key points, one per line.
    """
)

ANSWER_GENERATION_STEP = MCPStep(
    name="answer_generation",
    description="Generate a comprehensive answer based on the analysis",
    input_schema={
        "key_points": "List[str]",
        "query": "str",
        "relevance_score": "float"
    },
    output_schema={
        "answer": "str",
        "confidence": "float",
        "sources": "List[str]"
    },
    prompt_template="""
    Based on the following key points and query, generate a comprehensive answer:
    
    Key Points: {key_points}
    Query: {query}
    Relevance Score: {relevance_score}
    
    Provide a detailed answer that directly addresses the query.
    """
) 

# Similarly other steps can be formulated
import traceback
from typing import List, Dict, Any
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from intelli_docs.core.config import settings
from intelli_docs.core.mcp import MCPPipeline, DOCUMENT_ANALYSIS_STEP, ANSWER_GENERATION_STEP
from intelli_docs.services.embedding_service import EmbeddingService

class QAService:
    """
    Handles question answering using Model Context Protocl (MCP) and Retrieval Augmented Generation (RAG)
    """
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        
        # init Ollama without any custom callbacks
        self.llm = Ollama(model=settings.OLLAMA_MODEL)
        
        # setup the MCP piepline for usage
        self.mcp_pipeline = MCPPipeline(model_name=settings.OLLAMA_MODEL)
        
        # Add the MCP steps for doc analysis and answer gen
        self.mcp_pipeline.add_step(DOCUMENT_ANALYSIS_STEP)
        self.mcp_pipeline.add_step(ANSWER_GENERATION_STEP)
        
        # Create QA chain
        self.qa_prompt = PromptTemplate(
            template="""
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know.
            Please don't try to make up an answer or halucinate.
            
            Context: {context}
            
            Question: {question}
            
            Answer: """,
            input_variables=["context", "question"]
        )
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
    
    def answer_question(self, question: str, n_context_docs: int = 3) -> Dict[str, Any]:
        """
        Answer a question using RAG and MCP
        """
        error_source = "QA service"
        sources = []
        try:
            # Search for relevant documents
            relevant_docs = self.embedding_service.search_similar(
                query=question,
                n_results=n_context_docs
            )
            
            if not relevant_docs:
                return {
                    "answer": "No relevant documents found to answer your question.",
                    "sources": [],
                    "analysis": {
                        "document_analysis": {
                            "key_points": ["No relevant documents found"],
                            "relevance_score": 0.0
                        },
                        "answer_generation": {
                            "answer": "No relevant documents found",
                            "confidence": 0.0,
                            "sources": ""
                        }
                    }
                }
            
            # Prepare context from relevant documents
            context = "\n\n".join([doc['content'] for doc in relevant_docs])
            
            try:
                # Execute MCP pipeline
                mcp_result = self.mcp_pipeline.execute({
                    "document_content": context,
                    "query": question
                })
                
                # Generate final answer using QA chain
                answer = self.qa_chain.run(
                    context=context,
                    question=question
                )
                
                # Prepare response
                response = {
                    "answer": answer,
                    "sources": [
                        {
                            "content": doc['content'],
                            "metadata": doc['metadata'],
                            "relevance_score": 1 - (doc['distance'] if doc['distance'] is not None else 0)
                        }
                        for doc in relevant_docs
                    ],
                    "analysis": mcp_result
                }
                
                return response
                
            except Exception as e:
                error_source = "MCP pipeline"
                sources = [
                    {
                        "content": doc['content'],
                        "metadata": doc['metadata'],
                        "relevance_score": 1 - (doc['distance'] if doc['distance'] is not None else 0)
                    }
                    for doc in relevant_docs
                ]
                raise e
        except Exception as e:
            error_msg = f"Error in {error_source}: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "sources": sources,
                "analysis": {
                    "document_analysis": {
                        "key_points": [f"Error in {error_source}: {str(e)}"],
                        "relevance_score": 0.0
                    },
                    "answer_generation": {
                        "answer": f"Error in {error_source}: {str(e)}",
                        "confidence": 0.0,
                        "sources": ""
                    }
                }
            }
    
    def get_answer_with_sources(self, question: str) -> Dict[str, Any]:
        """
        Get answer with source documents
        """
        
        relevant_docs = self.embedding_service.search_similar(
            query=question,
            n_results=5
        )
        
        # prepare the context
        context = "\n\n".join([doc['content'] for doc in relevant_docs])
        
        # gen. answer
        answer = self.qa_chain.run(
            context=context,
            question=question
        )
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc['content'],
                    "metadata": doc['metadata'],
                    "relevance_score": 1 - (doc['distance'] if doc['distance'] is not None else 0)
                }
                for doc in relevant_docs
            ]
        } 
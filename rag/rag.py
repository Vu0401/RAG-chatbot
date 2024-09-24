from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

class Str_OutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()
    
    def parse(self, text: str) -> str:
        return self.extract_answer(text)
    
    
    def extract_answer(self,
                       text_response: str,
                       pattern: str = r"Answer:\s*(.*)"
                       ) -> str:
        
        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else:
            return text_response
        
class RAG:
    def __init__(self, llm, retriever):
        self.prompt = PromptTemplate(template="""Instruction:"You are a helpful assistant and keep this template for your response."\nRag:{retriever}\nHistory:{history}\nQuestion:{question}\nAnswer:""", \
            input_variables=["question"], partial_variables={"retriever": "{retriever}", "history": "{history}"})
        self.llm = llm
        self.retriever = retriever
        self.str_parser = Str_OutputParser()
        
    def rag_chain(self, history, question):
        if self.retriever is None:
            context = ""
        else:
            context = self.retriever.get_relevant_documents(question)
        
        chain = self.prompt | self.llm | self.str_parser
        response = chain.invoke({"retriever": context, "history": history, "question": question})
        
        # Improved output processing
        response = self.str_parser.parse(response)
      
        last_period_index = response.rfind('.')
        if last_period_index != -1:
            response = response[:last_period_index + 1]
        
        return response

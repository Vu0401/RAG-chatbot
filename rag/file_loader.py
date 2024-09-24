from langchain_community.document_loaders import PyPDFLoader
from typing import Union, List, Literal
import multiprocessing
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from abc import ABC, abstractmethod

def remove_non_utf8_characters(text):
    return ''.join(char for char in text if ord(char) < 128)

def load_pdf(pdf_file):
    docs = PyPDFLoader(pdf_file, extract_images=True).load()
    for doc in docs:
        doc.page_content = remove_non_utf8_characters(doc.page_content)
    return docs

def get_num_cpu():
    return multiprocessing.cpu_count()

class BaseLoader(ABC):
    def __init__(self) -> None:
        self.num_processes = get_num_cpu()
        
    @abstractmethod
    def __call__(self, files: List[str], **kwargs):
        pass
    
class PDFLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, files: List[str], **kwargs):
        num_processes = min(self.num_processes, kwargs["workers"])
        with multiprocessing.Pool(processes=num_processes) as pool:
            doc_loaded = []
            total_files = len(files)
            with tqdm(total=total_files, desc="Loading PDFs", unit="file") as pbar:
                for result in pool.imap_unordered(load_pdf, files):
                    doc_loaded.extend(result)
                    pbar.update(1)
        return doc_loaded
    
class TextSplitter:
    def __init__(self, 
                 separators: List[str] = ['\n\n', '\n', ' ', ''],
                 chunk_size: int = 300,
                 chunk_overlap: int = 0
                 ) -> None:
        
        self.splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    def __call__(self, documents):
        return self.splitter.split_documents(documents)

class Loader:
    def __init__(self, split_kwargs: dict = {"chunk_size": 200, "chunk_overlap": 20}) -> None:
        self.doc_loader = PDFLoader()
        self.doc_splitter = TextSplitter(**split_kwargs)

    def load(self, pdf_files: Union[str, List[str]], workers: int = 1) -> List:
        if isinstance(pdf_files, str):
            pdf_files = [pdf_files]
        doc_loaded = self.doc_loader(pdf_files, workers=workers)
        return self.doc_splitter(doc_loaded)



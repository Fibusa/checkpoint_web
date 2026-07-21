from pathlib import Path
from typing import List
from storage.base import DomainStorage

class FileStorage(DomainStorage):
    """Хранилище доменов в локальном файле."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def get_domains(self) -> List[str]:
        if not self.file_path.exists():
            return []
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [
                line.strip() 
                for line in f 
                if line.strip() and not line.startswith("#")
            ]
    
    def save_domains(self, domains: List[str]) -> bool:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                for domain in domains:
                    f.write(f"{domain}\n")
            return True
        except Exception:
            return False
    
    def is_available(self) -> bool:
        try:
            if not self.file_path.exists():
                self.file_path.touch()
            return True
        except Exception:
            return False
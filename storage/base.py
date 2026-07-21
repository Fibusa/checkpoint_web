from abc import ABC, abstractmethod
from typing import List

class DomainStorage(ABC):
    """Базовый интерфейс для хранилища доменов."""
    
    @abstractmethod
    def get_domains(self) -> List[str]:
        """Получить список доменов."""
        pass
    
    @abstractmethod
    def save_domains(self, domains: List[str]) -> bool:
        """Сохранить список доменов."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверить доступность хранилища."""
        pass
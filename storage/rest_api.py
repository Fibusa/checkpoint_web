import requests
from typing import List, Optional
from storage.base import DomainStorage

class RestApiStorage(DomainStorage):
    """Хранилище доменов через REST API."""
    
    def __init__(
        self, 
        base_url: str, 
        get_endpoint: str = "/domains",
        save_endpoint: str = "/domains",
        api_key: Optional[str] = None,
        timeout: int = 10
    ):
        self.base_url = base_url.rstrip("/")
        self.get_endpoint = get_endpoint
        self.save_endpoint = save_endpoint
        self.api_key = api_key
        self.timeout = timeout
        self._available = None
    
    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def get_domains(self) -> List[str]:
        try:
            url = f"{self.base_url}{self.get_endpoint}"
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data.get("domains", [])
            return data if isinstance(data, list) else []
        except Exception:
            return []
    
    def save_domains(self, domains: List[str]) -> bool:
        try:
            url = f"{self.base_url}{self.save_endpoint}"
            response = requests.post(
                url, 
                headers=self._get_headers(), 
                json={"domains": domains},
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
        except Exception:
            return False
    
    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        
        try:
            url = f"{self.base_url}{self.get_endpoint}"
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            self._available = response.status_code < 500
        except Exception:
            self._available = False
        
        return self._available
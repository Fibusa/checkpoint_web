import re
from typing import List
import api as api

class CheckpointStorage():
    """Хранилище доменов через Check Point API."""
    
    def __init__(self, base_url: str, list_name: str):
        self.base_url = base_url
        self.list_name = list_name
    
    def login(self, api_key: str) -> str:
        """Авторизация в Check Point API."""
        result = api.login(api_key, self.base_url)
        return result.get("sid", "")
    
    def logout(self, sid: str) -> str:
        """Завершение сессии."""
        result = api.logout(sid, self.base_url)
        return result.get("message", "")
    
    def _format_domains_for_api(self, domains: List[str]) -> List[str]:
        """Конвертирует список доменов в формат для Check Point API."""
        result = []
        for domain in domains:
            escaped = re.escape(domain)
            result.extend([f"\\/{escaped}", f"\\.{escaped}"])
        return result
    
    def _format_domains_from_api(self, url_list: List[str]) -> List[str]:
        """Конвертирует список URL-паттернов из API в список доменов."""
        domains = set()
        for pattern in url_list:
            domain = re.sub(r'^\\[\\/\.]', '', pattern)
            domain = domain.replace('\\.', '.')
            if domain:
                domains.add(domain)
        return sorted(list(domains))
    
    def get_domains(self, sid: str) -> List[str]:
        """Получить список доменов из Check Point."""
        try:
            result = api.show_application_site(sid, self.base_url, self.list_name)
            url_list = result.get("url-list", [])
            return self._format_domains_from_api(url_list)
        except Exception:
            return []
    
    def save_domains(self, sid: str, domains: List[str]) -> bool:
        """Сохранить список доменов в Check Point."""
        try:
            current_domains = set(self.get_domains(sid))
            new_domains = set(domains)

            to_add = new_domains - current_domains
            to_remove = current_domains - new_domains

            if to_add:
                url_list = self._format_domains_for_api(list(to_add))
                api.set_application_site(
                    sid, self.base_url, self.list_name, "add",
                    {"url-list": url_list}
                )

            if to_remove:
                url_list = self._format_domains_for_api(list(to_remove))
                api.set_application_site(
                    sid, self.base_url, self.list_name, "remove",
                        {"url-list": url_list}
                )
                
            # Публикация изменений
            api.publish(sid, self.base_url)

            return True
        except Exception as e:
            print(f"Error in save_domains: {e}")
            return False
        
if __name__ == '__main__':
    storage = CheckpointStorage(
        base_url="http://localhost:8080",
        list_name="WhiteList_kontur.ru"
    )
    
    print("=" * 50)
    print("Тест CheckpointStorage")
    print("=" * 50)
    
    # Тест 1: login (обязательно первый)
    print("\n[1] Тест login()...")
    sid = storage.login("FFl8+KF1AJ2Tisac6d0K+w==")
    print(f"    Session ID: {sid}")
    print(f"    Статус: {'OK' if sid else 'FAILED'}")
    
    if not sid:
        print("\nТест прерван: не удалось получить сессию")
        exit(1)
    
    # Тест 2: get_domains (требует сессию)
    print("\n[2] Тест get_domains()...")
    domains = storage.get_domains(sid)
    print(f"    Домены: {domains}")
    print(f"    Количество: {len(domains)}")
    print(f"    Статус: OK")
    
    # Тест 3: save_domains (требует сессию)
    print("\n[3] Тест save_domains()...")
    test_domains = ["example.com", "test.ru"]
    result = storage.save_domains(sid, test_domains)
    print(f"    Отправлено: {test_domains}")
    print(f"    Результат: {result}")
    print(f"    Статус: {'OK' if result else 'FAILED'}")
    
    # Тест 4: logout (требует сессию)
    print("\n[4] Тест logout()...")
    logout_result = storage.logout(sid)
    print(f"    Результат: {logout_result}")
    print(f"    Статус: OK")
    
    print("\n" + "=" * 50)
    print("Все тесты завершены")
    print("=" * 50)
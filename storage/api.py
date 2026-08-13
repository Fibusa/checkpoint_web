import requests

def login(api_key: str, base_url: str) -> dict:
    url = f"{base_url}/web_api/login"
    headers = {"Content-Type": "application/json"}
    payload = {"api-key": api_key}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

def logout(sid: str, base_url: str) -> dict:
    url = f"{base_url}/web_api/logout"
    headers = {"Content-Type": "application/json", "X-chkp-sid": sid}
    payload = {}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

def show_application_site(sid: str, base_url: str, list_name: str = None) -> dict:
    url = f"{base_url}/web_api/show-application-site"
    headers = {"Content-Type": "application/json", "X-chkp-sid": sid} 
    payload = {"name": list_name}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

def publish(sid: str, base_url: str) -> dict:
    url = f"{base_url}/web_api/publish"
    headers = {"Content-Type": "application/json", "X-chkp-sid": sid}
    payload = {}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

def set_application_site(sid: str, base_url: str, list_name: str, action: str, data: dict) -> dict:
    url = f"{base_url}/web_api/set-application-site"
    headers = {"Content-Type": "application/json", "X-chkp-sid": sid}
    payload = {
        "name": list_name,
        "url-list": {
            action: data
        }
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

if __name__ == '__main__':
    result = login(
        api_key="FFl8+KF1AJ2Tisac6d0K+w==",
        base_url="http://localhost:8080"
    )
    
    print(f"login: {result}")
    sid= result.get('sid')
    
    result = show_application_site(
        sid= sid, 
        base_url="http://localhost:8080",
        list_name="WhiteList_kontur.ru"
    )

    print(f"show_application_site: {result}")
    
    result = set_application_site(
        sid= sid, 
        base_url="http://localhost:8080",
        list_name="WhiteList_kontur.ru",
        action="add",
        data=["\\/example\\.com","\\.example\\.com"]
    )

    print(f"set_application_site: {result}")

    result = publish(
        sid= sid, 
        base_url="http://localhost:8080"
    )

    print(f"publish: {result}")    
    
    result = logout(
        sid= sid, 
        base_url="http://localhost:8080"
    )

    print(f"logout: {result}")
import kfp
from kfp import dsl
from kfp.dsl import component
import requests
from bs4 import BeautifulSoup
import os

# Replace with your actual Kubernetes service account token
KUBERNETES_SERVICE_ACCOUNT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Inkzc2VfLTlxVDRuczNQTXRERjBaY0pWUWgyazRjczd1WDBtREhreUtjWW8ifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUzMjgzMDc4LCJpYXQiOjE3NTMyNzk0NzgsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNTZkOGI1MmMtNTA2Mi00MDFkLWE2NTgtZGQ4MDc4NzQ4OGU3Iiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlZmxvdyIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJkZWZhdWx0IiwidWlkIjoiOTcyZGVhNTUtOTZlNC00MDRlLTkwZTUtOWVjNGY5MzEwZGExIn19LCJuYmYiOjE3NTMyNzk0NzgsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlZmxvdzpkZWZhdWx0In0.rVHrc2Jm2SMvksp_6xaanpiwpjbhg0heKqhS3NJOJfFPDKMkSktsmKAL8cfzv3riY4AVpFta_PtQR-JamsPj67nnVE4Q8fMesdQyT3wRpc3JQT5-X9mz7X-BoP3HNMY1KuDaYCd8YpPtI-NknKOLJa7s8pd9lbNgWwNBgnss-DD3oAJILtRUd4Q0A1yiU1B9i7rerTKM3D3983VMvv6vo7o8h2XlzcBjLituKpZhRuSEe0z8poMXS8IQyF4T4djhTk3_cWnn_M_GgUDirxtFpJeuco1E-JaH3fUK_1WG1aZmQnpWbU5cSxxZVquznMHTZAxqMsYxkIFY1-UDdkyz4g"
HOST = "https://kubeflow.keti-dp.re.kr/"
USERNAME = "yjwon@keti.re.kr"
PASSWORD = "won1234!"


def check_by_existing_token():
    print("Attempting to authenticate with Kubernetes service account token and list pipelines...")
    client = kfp.Client(
        host=f"{HOST}/pipeline",
        existing_token=KUBERNETES_SERVICE_ACCOUNT_TOKEN
    )
    try:
        r = client.list_pipelines()
        print("Successfully listed pipelines:")
        print(r)
    except Exception as e:
        print(f"Failed to list pipelines: {e}")
        print("Please ensure your KUBERNETES_SERVICE_ACCOUNT_TOKEN is valid and has the necessary permissions.")


def get_kubeflow_session_cookie(target_host, target_username, target_password):
    session = requests.Session()
    response = session.get(target_host)

    headers = {
        # "Content-Type": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    user_data = {"login": target_username, "password": target_password}
    response = session.post(response.url, data=user_data, verify=False)
    if response.status_code == 200:
        print("🔐 Successfully authenticated to Kubeflow.")
        return session.cookies.get("authservice_session")
    else:
        print("❌ Authentication failed. Check your credentials.")
        print(response.status_code)
        exit(1)


def check_by_session_call(target_host, target_username, target_password, target_namespace):
    print("Attempting to authenticate with Kubernetes session and list pipelines...")
    my_cookie = get_kubeflow_session_cookie(target_host=target_host, target_username=target_username,
                                            target_password=target_password)
    print(my_cookie)
    client = kfp.Client(
        host=f"{target_host}/pipeline",
        namespace=target_namespace,
        cookies=f"authservice_session={my_cookie}",
    )
    r = client.list_pipelines()
    print(r)
    client.delete_pipeline(pipeline_id="55b688d8-848a-4272-98f0-5ab0bc97f926")


def check_pipeline_info(target_host, target_username, target_password, target_namespace):
    my_cookie = get_kubeflow_session_cookie(target_host=target_host, target_username=target_username,
                                            target_password=target_password)
    client = kfp.Client(
        host=f"{target_host}/pipeline",
        namespace=target_namespace,
        cookies=f"authservice_session={my_cookie}",
    )
    # pipeline_name = "example_pipeline_private4"
    # r = client.get_pipeline("1f1ef00b-82fb-45e2-814d-09c612849bdd")
    # print(r)
    pipelines = client.list_pipelines()
    print(pipelines)
    pipeline_info = client.get_pipeline(pipeline_id="60051ac0-17ef-418e-9e0e-c6bd07849933")
    print(pipeline_info)
    print(target_namespace)


def get_kubeflow_session_cookie(target_host, target_username, target_password):
    session = requests.Session()
    response = session.get(target_host)
    print(response.status_code)
    headers = {
        "Content-Type": "application/json",
        # "Content-Type": "application/x-www-form-urlencoded",
    }
    user_data = {"login": target_username, "password": target_password}
    response = session.post(response.url, data=user_data, verify=False)
    if response.status_code == 200:
        print("🔐 Successfully authenticated to Kubeflow.")
        return session.cookies.get("authservice_session")
    else:
        print("❌ Authentication failed. Check your credentials.")
        print(response.status_code)
        exit(1)


def extract_hrefs_from_string(html_string):
    """Extract href values from HTML string"""
    soup = BeautifulSoup(html_string, 'html.parser')
    links = soup.find_all('a', href=True)
    return [link['href'] for link in links]


def kubeflow_authenticate_and_get_cookie(host: str, username: str, password: str, auth_suffix: str = "/oauth2/start", auth_type="ldap"):
    session = requests.Session()
    auth_url = f"{host}{auth_suffix}"
    session_response = session.get(auth_url)
    # Since 1.9.1 cookie's name is `oauth2_proxy_kubeflow_csrf`
    # cookie_name = "oidc_state_csrf" # For Kubeflow Manifest 1.8.1
    # cookie_name = "oauth2_proxy_kubeflow_csrf"
    cookie_name = session.cookies.keys()[0]
    cookie_value_1 = session.cookies.get(cookie_name)
    href_values = extract_hrefs_from_string(session_response.text)
    auth_request_url = ""
    for href_url in href_values:
        if href_url.split("/")[3].split("?")[0] == auth_type:
            auth_request_url = host + href_url
            break
    auth_response = session.get(auth_request_url, cookies={cookie_name: cookie_value_1}, verify=False)
    login_request_url = auth_response.url
    login_response = session.post(login_request_url, data={"login": username, "password": password}, verify=False,
                                  cookies={cookie_name: cookie_value_1})
    login_response.raise_for_status()
    print(session.cookies)
    cookie_return = None
    for a_cookie in session.cookies:
        # login_cookie_name = "oauth2_proxy_kubeflow" # For Kubeflow 1.9.1 and later
        # login_cookie_name = "authservice_session" # For Kubeflow 1.8.1
        login_cookie_name = a_cookie.name
        login_cookie_value = a_cookie.value
        cookie_return = f"{login_cookie_name}={login_cookie_value}"
        break
    return cookie_return


if __name__ == '__main__':
    #HOST = "http://34.82.249.126:8090"
    HOST = os.environ.get("KUBEFLOW_HOST", "https://kubeflow.sunjoo.org")
    USERNAME = os.environ.get("KUBEFLOW_USERNAME", "user@example.com")
    PASSWORD = os.environ.get("KUBEFLOW_PASSWORD", "12341234")
    AUTH_SOURCE = os.environ.get("KUBEFLOW_AUTH_SOURCE", "local")
    cookie_value = kubeflow_authenticate_and_get_cookie(HOST, USERNAME, PASSWORD, auth_type=AUTH_SOURCE)
    client = kfp.Client(
        host=HOST + "/pipeline",
        cookies=cookie_value
    )
    r = client.list_pipelines()
    print(r)

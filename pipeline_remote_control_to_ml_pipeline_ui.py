import kfp
from kfp import dsl
from kfp.dsl import component
import requests

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


def check_request(host: str, username: str, password: str, auth_suffix: str = "/oauth2/start"):
    session = requests.Session()
    auth_url = f"{host}{auth_suffix}"
    session_response = session.get(auth_url)
    cookie_value_1 = session.cookies.get('oidc_state_csrf')
    auth_request_url = f"{host}/dex/auth/ldap?client_id=kubeflow-oidc-authservice&redirect_uri=%2Fauthservice%2Foidc%2Fcallback&response_type=code&scope=openid+profile+email+groups&state={cookie_value_1}"
    auth_response = session.get(auth_request_url, cookies={'oidc_state_csrf': cookie_value_1}, verify=False)
    login_request_url  = auth_response.url
    login_response = session.post(login_request_url, data={"login": username, "password": password}, verify=False, cookies={"oidc_state_csrf": cookie_value_1})
    login_response.raise_for_status()
    print(session.cookies)
    cookie_name = "oauth2_proxy_kubeflow"
    if auth_suffix == "":
        cookie_name = "authservice_session"
    cookie_value = session.cookies.get(cookie_name)
    return f"{cookie_name}={cookie_value}"

if __name__ == '__main__':
    #HOST = "http://35.185.198.208:8090"
    HOST = "https://kubeflow.sunjoo.org"
    #USERNAME = "user@example.com"
    #PASSWORD = "12341234"
    USERNAME = "sunjoo.park"
    PASSWORD = "Postech2001!"
    cookie_value = check_request(HOST, USERNAME, PASSWORD, auth_suffix="")
    #cookie_value = check_request(HOST, USERNAME, PASSWORD, "")
    #client = kfp.Client(host=HOST, existing_token="eyJhbGciOiJSUzI1NiIsImtpZCI6InhnMnItc2dJelFNbWlPcW4zRml2eUwyNjZSV3l0MU9oRXZoQVJudXhhM1EifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUzNTQ2NzU3LCJpYXQiOjE3NTM1NDMxNTcsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlZmxvdy11c2VyLWV4YW1wbGUtY29tIiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImRlZmF1bHQiLCJ1aWQiOiJlM2ZhZDA0OS02ZGI3LTQzYjAtOTk2NC03ZTE4MTdmMTg5ZWIifX0sIm5iZiI6MTc1MzU0MzE1Nywic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVmbG93LXVzZXItZXhhbXBsZS1jb206ZGVmYXVsdCJ9.KRbyCxTAPdUW1FEqw1TVnbK0esO_K_s73MTPziVB-EHp6HOjfyttiZFJuZ_2Mw3NlxCays2f6yCEh0ZSLkOD3nm1DIfMhyk4BzWE0dd91mTpO-uqtgipI6PtByw8S6balUkKAyzZsEKF7mkQPeE8a8lgsOw-Krg7ihH-SVsLzR1QE3XGeDlK4ushpetkubpwEOL1yhhEQwBsBnuVrAFiChLXLyV447zjd-dJtoYWUegsfV4jaZX4a6KRR5esRuLUqYOJ75KjOhhhTXudg7cvQOLvl2fHhP5bje58nKInI6ukyWyTdXgVZwd7fRjfleY19Dln70MOesARtkU_xJaZlg")
    client = kfp.Client(
        host=HOST + "/pipeline",
        cookies=cookie_value
    )
    r = client.list_pipelines()
    #r2 = client.get_pipeline("5759ebbd-defc-4cd0-ad34-e50e0ff446cf")
    print(r)
    #print(r2)

import kfp
from kfp import dsl
from kfp.dsl import component

HOST = "https://kubeflow.sunjoo.org"
# Replace with your actual Kubernetes service account token
KUBERNETES_SERVICE_ACCOUNT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Inkzc2VfLTlxVDRuczNQTXRERjBaY0pWUWgyazRjczd1WDBtREhreUtjWW8ifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUzMjgzMDc4LCJpYXQiOjE3NTMyNzk0NzgsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNTZkOGI1MmMtNTA2Mi00MDFkLWE2NTgtZGQ4MDc4NzQ4OGU3Iiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlZmxvdyIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJkZWZhdWx0IiwidWlkIjoiOTcyZGVhNTUtOTZlNC00MDRlLTkwZTUtOWVjNGY5MzEwZGExIn19LCJuYmYiOjE3NTMyNzk0NzgsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlZmxvdzpkZWZhdWx0In0.rVHrc2Jm2SMvksp_6xaanpiwpjbhg0heKqhS3NJOJfFPDKMkSktsmKAL8cfzv3riY4AVpFta_PtQR-JamsPj67nnVE4Q8fMesdQyT3wRpc3JQT5-X9mz7X-BoP3HNMY1KuDaYCd8YpPtI-NknKOLJa7s8pd9lbNgWwNBgnss-DD3oAJILtRUd4Q0A1yiU1B9i7rerTKM3D3983VMvv6vo7o8h2XlzcBjLituKpZhRuSEe0z8poMXS8IQyF4T4djhTk3_cWnn_M_GgUDirxtFpJeuco1E-JaH3fUK_1WG1aZmQnpWbU5cSxxZVquznMHTZAxqMsYxkIFY1-UDdkyz4g"

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

if __name__ == '__main__':
    check_by_existing_token()
import kfp
from kfp import dsl
from kfp.dsl import component
import requests

# Replace with your actual Kubernetes service account token
KUBERNETES_SERVICE_ACCOUNT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Inkzc2VfLTlxVDRuczNQTXRERjBaY0pWUWgyazRjczd1WDBtREhreUtjWW8ifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUzMjgzMDc4LCJpYXQiOjE3NTMyNzk0NzgsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNTZkOGI1MmMtNTA2Mi00MDFkLWE2NTgtZGQ4MDc4NzQ4OGU3Iiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlZmxvdyIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJkZWZhdWx0IiwidWlkIjoiOTcyZGVhNTUtOTZlNC00MDRlLTkwZTUtOWVjNGY5MzEwZGExIn19LCJuYmYiOjE3NTMyNzk0NzgsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlZmxvdzpkZWZhdWx0In0.rVHrc2Jm2SMvksp_6xaanpiwpjbhg0heKqhS3NJOJfFPDKMkSktsmKAL8cfzv3riY4AVpFta_PtQR-JamsPj67nnVE4Q8fMesdQyT3wRpc3JQT5-X9mz7X-BoP3HNMY1KuDaYCd8YpPtI-NknKOLJa7s8pd9lbNgWwNBgnss-DD3oAJILtRUd4Q0A1yiU1B9i7rerTKM3D3983VMvv6vo7o8h2XlzcBjLituKpZhRuSEe0z8poMXS8IQyF4T4djhTk3_cWnn_M_GgUDirxtFpJeuco1E-JaH3fUK_1WG1aZmQnpWbU5cSxxZVquznMHTZAxqMsYxkIFY1-UDdkyz4g"
HOST  = "https://kubeflow.keti-dp.re.kr/"
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
        #"Content-Type": "application/json",
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
    my_cookie =get_kubeflow_session_cookie(target_host=target_host, target_username=target_username,
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
    #pipeline_name = "example_pipeline_private4"
    #r = client.get_pipeline("1f1ef00b-82fb-45e2-814d-09c612849bdd")
    #print(r)
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
        #"Content-Type": "application/x-www-form-urlencoded",
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



if __name__ == '__main__':
    HOST = "http://35.185.198.208:8090"
    #client = kfp.Client(host=HOST, existing_token="eyJhbGciOiJSUzI1NiIsImtpZCI6InhnMnItc2dJelFNbWlPcW4zRml2eUwyNjZSV3l0MU9oRXZoQVJudXhhM1EifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUzNTQ2NzU3LCJpYXQiOjE3NTM1NDMxNTcsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlZmxvdy11c2VyLWV4YW1wbGUtY29tIiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImRlZmF1bHQiLCJ1aWQiOiJlM2ZhZDA0OS02ZGI3LTQzYjAtOTk2NC03ZTE4MTdmMTg5ZWIifX0sIm5iZiI6MTc1MzU0MzE1Nywic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVmbG93LXVzZXItZXhhbXBsZS1jb206ZGVmYXVsdCJ9.KRbyCxTAPdUW1FEqw1TVnbK0esO_K_s73MTPziVB-EHp6HOjfyttiZFJuZ_2Mw3NlxCays2f6yCEh0ZSLkOD3nm1DIfMhyk4BzWE0dd91mTpO-uqtgipI6PtByw8S6balUkKAyzZsEKF7mkQPeE8a8lgsOw-Krg7ihH-SVsLzR1QE3XGeDlK4ushpetkubpwEOL1yhhEQwBsBnuVrAFiChLXLyV447zjd-dJtoYWUegsfV4jaZX4a6KRR5esRuLUqYOJ75KjOhhhTXudg7cvQOLvl2fHhP5bje58nKInI6ukyWyTdXgVZwd7fRjfleY19Dln70MOesARtkU_xJaZlg")
    client = kfp.Client(
        host=HOST+"/pipeline",
        cookies="oauth2_proxy_kubeflow=Z3Phcqz3FrhqGzJE83N8waH0vMYH6DRJKzCEmwwMO3aWek8403QS01enVBqIPnhycjwmy5RLUrjbvS27Z6c4Lbq6M93uitezOp36rG25XYVnqYQHXe5ITdCO48fHtE9Y-Cm9NG1txIx2Pt3lTdI9b3yHCQpiPJJlWfUdWZPqsP2VF-t1Lh-MR58GNsfy8xyNLaUGhT_M31NCFvZ2duRSWqUUnv9w2OuLwoJucEAJ1pFklHGb0DdK6eH4xBg9DvXa_4hMKjehJ8cPalwNyJ-ZULDQAIAO_btb6XuBjjXjaVUjUsFzVepsQfTeu6LnCEnzqhmi1t4FinRFwbgvrXu1pu7oJK42GiACJTwg6VixpKUg-B0Yehp5o6C316z2a-1Wpg1aym1z-69cJfZqaI6zVlzxO5FxD2PLGdNqDdEO2McSQY0BNuTCB6cugCdbZiXBoQ8LMIetLiyjZSszqBcuyCVx4IBn5K0_Mu1zxV7O3X0dP26Z77i69pWIk54PHLWNohGZ0DKerZIEt6Chm5QF23_trXJcrBTjfZYr37Uy5w5QmiqqXDawTctgNb-GEsq3OeSO2jV8uFGK3VCIB5xL_Mdh5sF53NNSf3Z_rzYHDZgtlsS7WQf_ds8vp8Q3UIF0jSPuL8HGmFal0A8UrX6oHSxoJ6FsVfyHtjZM4frP3RvV1tkf7RaRTonaUdVCl8wMxP700gTz9ZwFyrE9_Xwwc5ZK_irtWXPppNyTmZnWbvMQfRTOjJ3zTKuaNYV1wr5-do2r4wbIvArUN2UFn-o0Z6XpUro7vR_ZUbU4PXKeTgT0DIib0nGZSPtPYKX3l5bAiKhp6MeqYn5rsyQCINiU6Fgjt_D0qDygln-MBVIqjUHLOgh4BJEln4_6g_TMRAYwzQ_pnsx9q9FVEksspI8dhRqGjnc8NlXw8RO1RTdwVQNqTIcjzRlO7QPDbFnVMvZ5gTyHV3rPg9WpW9c96NStpMH3G7cUsS7Q6UF6X1wtRv2Uk1fBLsqoSHSJnRImDn0NASlCpSsmYvDXPVFTNnMHO78gINVbY5Su_mFUtu6kFjjO9Gg4P6gJ39_aK7f6iAfn_0eVy0QeXw9D42PlOynltJmVZ79q0KHM6LiGqxqdsjylK6zHZzMtTSSIJUMhnxBdT0QSLtXQOJdH2xjL0WTinQHGpF-yrQhnwQb5IxFtFBQtHf9akl46NSNwK2dwOiYuDvE27iWyaqsB9oqzBf-tlitPSaKkXS8y-3i-is73K98PEiSq77pqXAUeufC3k4K0foumKOKouRusJxT2dGEnaH3eICOXLie1uCEP3EkISzeJkZkUnY51YWhcg8WFyxArsk2o7rjIa4U4P9h2l23DnDmOovOrGDY6lNySAOaRTp_9tEttcWC56IP2z8HdGaeWGVArtAHFuV8CePNd3fJmJZZ6R2lqjrhVpe6PcH-APYtH89r0bU3D_LHPOMxDtTByUHpQ_Cem4ZhKhyCGYqCglBMx3UIpYgrKjmnkDda-74Cr2hibJdY5_ficS60XwTthqZir6fGPAPDL6869b-jSPdNXyac252wxGmH11uSTxSdJv2z5DvAHqv5guXQMLOd_JO5gJHD-RvygNed3lDwDjHfYc9zNjVs81xwHs754WfqX43Eg16pzpowZeszJU48mUPRQFJSyyVlGpBDr27X031jWRTvV6N7a5bW-KVogwMFkuTvLky90vuaT2iI1_M7EE2fNz2_nkjfDNWLYdl8orGAO2YqHQrew6PIbkRw6oMih1y6qpjlWOYcMXV2THCyQeLXs-wayrrjzluOZcz-ruW5iePMqEFtZhw_13fRAz0CPkyyRdd9TBNn1uQfbGwhpZ9zMXcTV5Gz3ZhPh3XjZLkI2W3LjmoFE44t-KVqGmih7T_E75WbUhRI1ITY=|1753609444|QXwmB0qRtRq8U1VOCI9mLsBbZkyCdrQEle23OjFb2yQ=")
    r = client.list_pipelines()
    r2 = client.get_pipeline("5759ebbd-defc-4cd0-ad34-e50e0ff446cf")
    print(r)
    print(r2)


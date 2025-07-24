import kfp
from kfp import dsl
from kfp.dsl import component
import requests
from datetime import datetime

def shell_operator():
    return dsl.ContainerSpec(
        image='all4dich/pytorch-cuda-example:dev',
        command=["bash", "-c", "echo 'Hello from the shell operator!'"]
    )

def ubuntu_operator():
    return dsl.ContainerSpec(
        image='all4dich/pytorch-cuda-example:dev',
        #command=["apt-get", "update",  "-y", "&&", "apt-get", "install",  "-y",  "curl", "&&", "curl", "https://gist.githubusercontent.com/all4dich/d4518fc493bf1aeb0fcae3756655b1f7/raw/625177726128b4ba9b2656bdf0654d26d52a7ac7/call.py",  "-o", "/tmp/call.py", "&&", "python3", "/tmp/call.py"]
    )

@component
def hello_world(name: str):
    print("Hello, ", name)

@component
def print_address(name: str):
    print("320 , ", name)

@dsl.pipeline(
    name='example-pipeline',
    description='An example pipeline that checks CUDA availability.'
)
def example_pipeline():
    # This is a placeholder for a pipeline step.
    # You can add your own components here.
    hello_world(name = "Sunjoo")
    print_address(name = "resdfsdf")

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

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_func=example_pipeline, package_path='example_pipeline.yaml')
    print("Pipeline compiled successfully and saved to 'example_pipeline.yaml'.")
    target_host = "https://kubeflow.sunjoo.org"
    target_username = "user@example.com"
    target_password = "12341234"
    target_namespace = "kubeflow-user-example-com"
    pipeline_id = "a6915e0d-47b8-47f8-9a69-d29d09efd9fa"
    my_cookie =get_kubeflow_session_cookie(target_host=target_host, target_username=target_username,
                                target_password=target_password)

    print(my_cookie)
    client = kfp.Client(
        host=f"{target_host}/pipeline",
        namespace=target_namespace,
        cookies=f"authservice_session={my_cookie}",
    )
    r = client.get_pipeline(pipeline_id)
    print(r)
    #r = client.upload_pipeline(
    #    pipeline_package_path='example_pipeline.yaml',
    #    pipeline_name='example_pipeline_private4',
    #    namespace='kubeflow-user-example-com'
    #)
    #id = client.get_pipeline_id(name = "example_pipeline_private3")
    #print(id)
    r  = client.upload_pipeline_version(
        pipeline_package_path='example_pipeline.yaml',
        #pipeline_name='example_pipeline_private4',
        pipeline_version_name=f"pipeline at {datetime.now()}",
        pipeline_id = pipeline_id
    )
    #client.create_run_from_pipeline_package(
    #    pipeline_file ='example_pipeline.yaml',
    #    #pipeline_name='example_pipeline_private4',
    #    experiment_id = "6862b4f0-00cb-46df-a29d-72b596451b5b"
    #)
    client.run_pipeline(
        experiment_id="6862b4f0-00cb-46df-a29d-72b596451b5b",
        pipeline_id=r.pipeline_id,
        version_id=r.pipeline_version_id,
        job_name=f"job {datetime.now()}"

    )

import kfp
from humanfriendly.terminal import message
from kfp import dsl
from kfp.dsl import component
import requests
from datetime import datetime
import logging

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
def hello_world(name: str) -> str:
    import os
    message = ("Hello, ", name)
    print(message)
    os.system("uname -a")
    return "message"

@component
def print_address(name: str, input_message: str) -> str:
    import os
    print("320 , ", name)
    os.system("uname -a")
    print(input_message)
    return "Done"

@component
def ending_message():
    print("Done.....")

@component(
    base_image="python:3.13-slim",
)
def print_ubuntu_info():
    import os
    os.system("which vim")
    os.system("which git")
    os.system("uname -a")

@dsl.pipeline(
    name='example-pipeline',
    description='An example pipeline that checks CUDA availability.'
)
def example_pipeline():
    # This is a placeholder for a pipeline step.
    # You can add your own components here.
    a = hello_world(name = "Sunjoo")
    b = print_address(name = "resdfsdf", input_message=a.output)
    c = ending_message().after(b)
    d = ending_message().after(a)
    print_ubuntu_info().after(c)
    print_ubuntu_info().after(d)

@dsl.component
def square(x: float) -> float:
    return x ** 2

@dsl.component
def add(x: float, y: float) -> float:
    return x + y

@dsl.component
def square_root(x: float) -> float:
    return x ** .5

@dsl.pipeline
def square_and_sum(a: float, b: float) -> float:
    a_sq_task = square(x=a)
    b_sq_task = square(x=b)
    return add(x=a_sq_task.output, y=b_sq_task.output).output

@dsl.pipeline
def pythagorean(a: float = 1.2, b: float = 1.2) -> float:
    sq_and_sum_task = square_and_sum(a=a, b=b)
    return square_root(x=sq_and_sum_task.output).output

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
    #kfp.compiler.Compiler().compile(pipeline_func=pythagorean, package_path='example_pipeline.yaml')
    print("Pipeline compiled successfully and saved to 'example_pipeline.yaml'.")
    target_host = "https://kubeflow.sunjoo.org"
    target_username = "user@example.com"
    target_password = "12341234"
    target_namespace = "kubeflow-user-example-com"
    pipeline_name = "example_pipeline_8"
    pipeline_id = "c35d9aa1-1a94-4b00-8b38-b8e1b8dbd2f9"
    experiment_name = "experiment_1"
    experiment_id= "6862b4f0-00cb-46df-a29d-72b596451b5b"
    from pipeline_remote_control_to_ml_pipeline_ui import kubeflow_authenticate_and_get_cookie

    # IF you  create connector configuration for LDAP on Dex configuration, set auth_type='ldap'
    my_cookie = kubeflow_authenticate_and_get_cookie(host=target_host, username=target_username, password=target_password, auth_type="local")

    client = kfp.Client(
        host=f"{target_host}/pipeline",
        namespace=target_namespace,
        cookies=f"{my_cookie}",
    )

    print("Upload pipeline to the existing pipeline (upload pipeline version )")
    r  = client.upload_pipeline_version(
        pipeline_package_path='example_pipeline.yaml',
        #pipeline_name=pipeline_name,
        pipeline_version_name=f"pipeline at {datetime.now()}",
        pipeline_id = pipeline_id
    )

    client.run_pipeline(
        experiment_id=experiment_id,
        pipeline_id=r.pipeline_id,
        version_id=r.pipeline_version_id,
        job_name=f"job {datetime.now()}"

    )

    #client.create_run_from_pipeline_package(
    #    pipeline_file ='example_pipeline.yaml',
    #    #pipeline_name='example_pipeline_private4',
    #    experiment_id = "6862b4f0-00cb-46df-a29d-72b596451b5b"
    #)

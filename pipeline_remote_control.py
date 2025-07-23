import kfp
from kfp import dsl
from kfp.dsl import component

HOST = "https://kubeflow.sunjoo.org"
USERNAME  = "user@example.com"
PASSWORD = "12341234"

if __name__ == '__main__':
    print("Pipeline compiled successfully and saved to 'example_pipeline.yaml'.")
    client = kfp.Client(
        host=f"{HOST}/pipeline"
    )
    r = client.list_pipelines()
    print(r)

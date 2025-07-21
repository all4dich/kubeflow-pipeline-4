import kfp
from kfp import dsl

def ubuntu_operator():
    return dsl.ContainerOp(
        name='ubuntu-operator',
        image='all4dich/pytorch-cuda-example:dev',
        #command=["apt-get", "update",  "-y", "&&", "apt-get", "install",  "-y",  "curl", "&&", "curl", "https://gist.githubusercontent.com/all4dich/d4518fc493bf1aeb0fcae3756655b1f7/raw/625177726128b4ba9b2656bdf0654d26d52a7ac7/call.py",  "-o", "/tmp/call.py", "&&", "python3", "/tmp/call.py"]
    )
@dsl.pipeline(
    name='example-pipeline',
    description='An example pipeline that checks CUDA availability.'
)
def example_pipeline():
    # This is a placeholder for a pipeline step.
    # You can add your own components here.
    ubuntu_operator()

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_func=example_pipeline, package_path='example_pipeline.yaml')
    print("Pipeline compiled successfully and saved to 'example_pipeline.yaml'.")
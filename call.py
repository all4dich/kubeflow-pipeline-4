import torch
import time
a = torch.cuda.is_available()
print(f"CUDA available: {a}")
if a == True:
    print("CUDA is available on this machine.")
else:
    print("CUDA is not available on this machine.")

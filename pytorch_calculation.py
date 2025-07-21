import torch
import time

torch.set_default_device('cuda')  # Ensure calculations are done on CPU
# Set the duration for the calculation (in seconds)
duration = 5 * 60  # 5 minutes

# Get the start time
start_time = time.time()

print(f"Starting PyTorch calculation for {duration / 60} minutes...")

# Loop for the specified duration
while time.time() - start_time < duration:
    # Initialize large random tensors on the CPU
    # The size of the tensors can be adjusted based on the machine's performance
    # A larger size will result in a more intensive calculation
    tensor_a = torch.rand(10000, 10000)
    tensor_b = torch.rand(10000, 10000)

    # Perform a computationally expensive operation (matrix multiplication)
    result = torch.matmul(tensor_a, tensor_b)

    # Optional: Print a message to show that the script is running
    # print(f"Calculation in progress... Time elapsed: {time.time() - start_time:.2f} seconds")

# Get the end time
end_time = time.time()

print(f"PyTorch calculation finished after {end_time - start_time:.2f} seconds.")

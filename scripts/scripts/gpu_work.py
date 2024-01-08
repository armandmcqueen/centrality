import torch

# Check if CUDA is available
if torch.cuda.is_available():
    # Create large tensors and perform a matrix multiplication
    a = torch.rand(10000, 10000, device="cuda")
    b = torch.rand(10000, 10000, device="cuda")
    for _ in range(100_000):
        c = torch.matmul(a, b)
else:
    raise RuntimeError("CUDA not available")

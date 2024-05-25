"""
top_k: int
    The top-k value to use for sampling.
    Default value: 40

top_p: float
    The top-p value to use for sampling.
    Default value: 0.95

temperature: float
    The temperature to use for sampling.
    Default value: 0.8

repetition_penalty: float
    The repetition penalty to use for sampling.
    Default value: 1.1

last_n_tokens: int
    The number of last tokens to use for repetition penalty.
    Default value: 64

seed: int
    The seed value to use for sampling tokens.
    Default value: -1

max_new_tokens: int
    The maximum number of new tokens to generate.
    Default value: 256

stop: List[str]
    A list of sequences to stop generation when encountered.se
    Default value: None

stream: bool
    Whether to stream the generated text.
    Default value: False

reset: bool
    Whether to reset the model state before generating text.
    Default value: True

batch_size: int
    The batch size to use for evaluating tokens in a single prompt.
    Default value: 8

threads: int
    The number of threads to use for evaluating tokens.
    Default value: -1

context_length: int
    The maximum context length to use.
    Default value: -1

gpu_layers: int
    The number of layers to run on GPU.
    Default value: 0
"""

MODEL_TYPE = 'mistral'
# MODEL_TYPE = 'llama'
LIB = 'avx2'

MAX_NEW_TOKES = 5
REPETITION_PENALTY = 1.1
TEMPERATURE = 0.01
TOP_K = 50
TOP_P = 0.85
THREADS = -1
SEED = -1
CONTEXT_LENGTH = -1
BATCH_SIZE = 8


CONFIG = {
    "top_k": TOP_K,
    "top_p": TOP_P,
    "temperature": TEMPERATURE,
    "repetition_penalty": REPETITION_PENALTY,
    "seed": SEED,
    "max_new_tokens": MAX_NEW_TOKES,
    "stream": False,
    "reset": False,
    "batch_size": BATCH_SIZE,
    "threads": THREADS,
    "context_length": CONTEXT_LENGTH,
}

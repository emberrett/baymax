#!/bin/sh

c/Users/berre/Documents/models:/models ghcr.io/ggerganov/llama.cpp:full --all-in-one "/models/" Mistral-7B-v0.1

docker run -v c/Users/berre/Documents/models:/models ghcr.io/ggerganov/llama.cpp:full --convert "/models/Mistral-7B-v0.1" 1

docker run -v c/Users/berre/Documents/models:/models ghcr.io/ggerganov/llama.cpp:full --quantize "/models/Mistral-7B-v0.1/ggml-model-f32.gguf" "/models/Mistral-7B-v0.1/ggml-model-Q4_K_M.bin" Q4_K_M

docker run -v c/Users/berre/Documents/models:/models --entrypoint '/app/main' ghcr.io/ggerganov/llama.cpp:full  -m "/models/Mistral-7B-v0.1/ggml-model-Q4_K_M.bin" -n 512 -p "Tell me a story"
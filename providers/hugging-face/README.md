# Hugging Face

Roles: weights-host, inference-provider, gateway
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Hub downloads, routed Inference Providers, and dedicated Inference Endpoints are separate products.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Router location depends on provider; dedicated endpoint regions/hardware must be selected. Gated repositories can restrict EU access."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Free $0.10 monthly credits subject to change; PRO and organization seats $2 monthly general compute credits. Provider quotas still apply."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Routed gateway does not store request/response bodies or use them for training; debugging metadata up to 30 days. Actual inference provider has its own policy."}

## Notes

- Each repository's license controls weights and commercial use. Gated downloads require account approval/contact-data sharing. Local inference costs hardware and operations.

## Limitations

- Privacy/data-use details were not fully verified in this baseline.
- Exact public or account-specific quotas were not established.

## Offers

22 linked model(s), 25 access route(s), 2 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[huggingface.co](https://huggingface.co/docs/inference-providers/main/pricing) · [huggingface.co](https://huggingface.co/docs/inference-providers/en/security) · [huggingface.co](https://huggingface.co/docs/inference-endpoints/pricing) · [huggingface.co](https://huggingface.co/docs/hub/models-gated) · [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B) · [Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) · [Qwen3.8-2.4T-A95B model card](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) · [Qwen3-Coder-Next model card](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B) · [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) · [DeepSeek-V4-Pro-0813 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [Mistral Small 4 119B model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) · [Mistral Medium 3.5 128B model card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) · [Mistral Large 3 675B Instruct model card](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512) · [Ministral 3 8B Instruct model card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) · [Devstral Small 2 24B model card](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) · [Phi-4-Reasoning-Vision-15B model card](https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B) · [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3) · [GLM-5.3-Flash model card](https://huggingface.co/zai-org/GLM-5.3-Flash) · [MiniMax M3 model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [Nemotron3 Ultra 550B-A55B model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16) · [Llama 4 Scout / Maverick model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) · [Llama 4 Maverick official card](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) · [Phi-4 Mini / Multimodal model card](https://huggingface.co/microsoft/Phi-4-mini-instruct) · [Phi-4 Multimodal official card](https://huggingface.co/microsoft/Phi-4-multimodal-instruct) · [huggingface.co](https://huggingface.co/docs/inference-endpoints/guides/access)

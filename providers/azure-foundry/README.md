# Microsoft Foundry / Azure

Roles: cloud-platform, inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Models sold by Azure and partner offerings must be distinguished; region, Global and DataZone deployments differ.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Standard processing within selected geography; Global may process in any supported geography; DataZone within defined US/EU zone. At-rest geography differs from inference location."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Per-model/deployment/account quotas and prices not verified."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Reviewed policy covers models sold by Azure: no base-model training on prompts/completions. Stateful features can store data; flagged abuse may trigger storage/human review. Modified monitoring requires approval."}
- Claude Marketplace offers are operated by Anthropic as an independent processor; Azure-hosted and Anthropic-hosted processing differ, with exceptions-only safety review. Models sold by Azure policy does not cover this route.

## Notes

- Azure billing is separate from Microsoft/Copilot consumer subscriptions and original creator subscriptions.
- Official Phi pages advertise Foundry. Exact region, SKU and per-token price not verified.
- creator: Microsoft
- url: https://azure.microsoft.com/en-us/products/phi

## Limitations

- Privacy/data-use details were not fully verified in this baseline.
- Exact public or account-specific quotas were not established.

## Offers

18 linked model(s), 24 access route(s), 1 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy) · [azure.microsoft.com](https://azure.microsoft.com/en-us/products/phi) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/) · [Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview) · [Claude models in Foundry: data, privacy and security](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/claude-models/data-privacy)

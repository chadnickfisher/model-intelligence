# Microsoft Foundry / Azure

Roles: cloud-platform, inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Models sold by Azure and partner offerings must be distinguished; region, Global and DataZone deployments differ.

## Api compatibility

- Claude Marketplace offerings use the Claude API response format, Azure-hosted endpoints, and Azure API-key or Entra ID authentication; deployment names identify requested models. Fable 5.1 is Anthropic-hosted only.
- Haiku 4.5 on Foundry uses the Claude Messages API with Microsoft Entra ID or a deployment API key; model refers to the chosen deployment name, which may differ from the public model ID.
- Claude Marketplace uses Messages-format Azure endpoints authenticated by deployment API keys or Entra ID; deployment names can differ from model IDs.
- Claude Marketplace uses Messages-format endpoints with Azure API key or Entra ID; custom deployment name is the request model value.
- Claude Sonnet 5.5 uses Azure-hosted Claude API endpoints with API-key or Entra authentication. Message Batches, Models API and server fallback are unsupported; additional tools differ by hosting option.

## Geographic availability

- {"status": "partial", "summary": "Standard processing within selected geography; Global may process in any supported geography; DataZone within defined US/EU zone. At-rest geography differs from inference location."}
- not_exhaustively_verified
- Haiku 5.5 supports both hosting choices; Azure-hosted offers Global or US Data Zone. Anthropic-hosted processing may leave Azure/selected region. Exact region/version listings need deployment-specific validation.
- Opus 5.5 supports both hosting choices; Azure hosting offers Global or US Data Zone. Anthropic hosting can process outside Azure/selected region.
- Primary-source conflict checked 2026-10-09: Microsoft lists Sonnet 5.5 Hosted on Azure in US Data Zone and publishes quota defaults; Anthropic's Foundry guide says Sonnet 5.5 Global Standard only. Global support is agreed; Azure US Data Zone availability remains unresolved, and no new offer is added.

## Rate limits

- {"status": "partial", "summary": "Per-model/deployment/account quotas and prices not verified."}
- Haiku 4.5 Global Standard public defaults: PAYG 80 RPM/80000 uncached ITPM/16000 OTPM; Enterprise/MCA-E 10000/10000000/2000000; Free Trial zero. Exact account capacity and Data Zone quotas remain unknown.
- Haiku 5.5 pay-as-you-go defaults: 40 RPM, 40,000 input TPM and 8,000 output TPM. Enterprise/MCA-E: 10,000 RPM, 10M input TPM and 2M output TPM. Free Trial defaults are zero. Subscription pools are shared by model/version and deployment type.
- Opus 5.5 PAYG defaults 40 RPM/40000 input TPM/8000 output TPM; Enterprise/MCA-E 10000/10M/2M; Free Trial zero. Model/version/deployment-type pools are shared.
- Sonnet 5.5 Global Standard defaults in both hosts: PAYG 40 RPM / 40,000 uncached ITPM / 8,000 OTPM; Enterprise/MCA-E 10,000 / 10,000,000 / 2,000,000; Free Trial zero. Actual subscription allocation may differ.
- All Global deployments of the same Claude model/version within a subscription share one pool across regions. Microsoft also publishes Azure US Data Zone rows, but Anthropic documents Sonnet 5.5 as Global-only; that deployment disagreement is unresolved.

## Caching batching

- Claude Fable 5.1 has documented five-minute/one-hour prompt-cache pricing through Foundry CCU conversion. Message Batches API is unsupported on Foundry.
- Haiku 4.5 prompt caching has a 4096-token minimum and documented five-minute/one-hour TTL options. A model-specific Foundry Batch API tariff was not established; generic batching advice is not an offer.
- Claude Haiku 5.5 caching minimum 512 tokens with 5-minute or 1-hour TTL; native Message Batches unsupported in Foundry.
- Opus 5.5 cache minimum 512 tokens; native Message Batches unsupported. Azure hosting excludes Files API, code execution, Agent Skills and programmatic tool calling.
- Sonnet 5.5 on Foundry supports automatic and explicit prompt caching, with a 512-token minimum and five-minute or one-hour TTL. Cache writes count toward input limits; cache reads do not.
- Claude Message Batches API is explicitly unsupported on Foundry; no direct-Claude batch discount is assigned to this route.

## Privacy data use

- {"status": "public_verified", "summary": "Reviewed policy covers models sold by Azure: no base-model training on prompts/completions. Stateful features can store data; flagged abuse may trigger storage/human review. Modified monitoring requires approval."}
- Claude Marketplace offers are operated by Anthropic as an independent processor; Azure-hosted and Anthropic-hosted processing differ, with exceptions-only safety review. Models sold by Azure policy does not cover this route.

## Notes

- Azure billing is separate from Microsoft/Copilot consumer subscriptions and original creator subscriptions.
- Official Phi pages advertise Foundry. Exact region, SKU and per-token price not verified.
- creator: Microsoft
- url: https://azure.microsoft.com/en-us/products/phi

## Limitations

- For Fable 5.1 Hosted on Anthropic, Microsoft documents Preview without an SLA; this restriction is specific to that offering.
- Broad partner catalog conflicts with exact Opus 5.5/integration docs on image output, disabled thinking and hosting-specific tools; no runtime test resolved it.
- Earlier baseline privacy/quota gaps have now been investigated for Models sold by Azure and Claude Marketplace; these products have distinct processors and handling rules.
- Public Claude quotas are subscription/model/version/deployment-specific defaults. Individual allocations, negotiated agreements and retention/monitoring settings are unverified.
- Claude Sonnet 5.5 US Data Zone support is documented by Microsoft but excluded by Anthropic's Foundry guide; treat it as unresolved until the provider reconciles the docs.

## Offers

18 linked model(s), 24 access route(s), 1 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy) · [azure.microsoft.com](https://azure.microsoft.com/en-us/products/phi) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/) · [Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview) · [Claude models in Foundry: data, privacy and security](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/claude-models/data-privacy)

# Claude Platform on AWS

Roles: cloud-platform, access-product
Verified: 2026-10-07

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Marketplace enrollment, separate Anthropic organization; AWS IAM SigV4 or platform API key.

## Api compatibility

- Claude API request format; platform-specific SDK clients remain beta; OpenAI-compatible endpoints unavailable.

## Geographic availability

- AWS commercial regions for gateway access; gateway region does not establish inference residency; Haiku 4.5 rejects inference_geo.

## Rate limits

- Anthropic usage tier and monthly spend caps apply; negotiated/account limits require confirmation.

## Caching batching

- Prompt caching and batch processing documented; use the exact model eligibility and separate tariff.

## Privacy data use

- Anthropic is an independent data processor; approved zero retention is opt-in. Content is processed/stored on AWS, with pre-September-18-2026 workspace exceptions.

## Notes

- New public access-product identity; policies and account-specific entitlements remain unverified.

## Limitations

- No private entitlement, negotiated throughput or SLA inspected.

## Offers

4 linked model(s), 4 access route(s), 0 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Claude plan pricing](https://claude.com/pricing) · [Claude Code model configuration](https://code.claude.com/docs/en/model-config) · [Claude Code API key billing priority](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code) · [Claude Code subscription authentication](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan) · [Claude Fable 5.1 on AWS](https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-1-on-aws/) · [aws.amazon.com](https://aws.amazon.com/bedrock/pricing/) · [Cloud generative AI pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) · [Fable models on Claude plans](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) · [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)

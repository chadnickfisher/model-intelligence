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
- Haiku 5.5 permits US-only inference at 1.1× or global at base price; gateway region is distinct from inference geography. AWS launch text described North America availability, so individual region entitlement remains untested.
- Opus 5.5 permits global routing or US-only inference at 1.1x. Gateway/workspace region and inference geography are distinct.
- Sonnet 5.5 supports global or US-only inference geography; US-only pricing is 1.1x across token categories. The AWS gateway region does not itself pin inference geography.

## Rate limits

- Anthropic usage tier and monthly spend caps apply; negotiated/account limits require confirmation.
- New organizations begin at Start; tier history comes from paid Marketplace invoices. Monthly caps reset first-of-month 00:00 UTC; enforcement can lag about 2 hours and billed overshoot is possible.
- Organizations begin at Start; paid Marketplace history can raise tier. Calendar caps reset first-of-month 00:00 UTC; enforcement can lag about two hours and overshoot is billed.

## Caching batching

- Prompt caching and batch processing documented; use the exact model eligibility and separate tariff.

## Privacy data use

- Anthropic is an independent data processor; approved zero retention is opt-in. Content is processed/stored on AWS, with pre-September-18-2026 workspace exceptions.
- AWS Service Terms section 50.16 says Platform content is processed by Anthropic outside AWS; Anthropic technical guidance says AWS infrastructure for current workspaces, with pre-September 18, 2026 exceptions. The wording mismatch was not resolved into a universal residency guarantee.

## Notes

- Public access-product identity is distinct from Bedrock. Fable-specific documented policies were inspected on 2026-10-08; account entitlement and negotiated SLA remain unverified, and processing-scope wording differs between technical documentation and AWS terms.
- Earlier baseline: this new public access product’s policies and account entitlements had not been verified. Public documentation inspected on 2026-10-08 establishes Anthropic-managed rate/spend policies and opt-in zero data retention with the documented older-workspace exception. Private account entitlement, actual ZDR enrollment, negotiated limits and SLA remain unverified.

## Limitations

- No private entitlement, negotiated throughput or SLA inspected.
- Platform-wide exclusions include HIPAA-ready program participation, OAuth, OpenAI-compatible endpoints, fast mode and the newer computer/browser toolsets; older beta computer-use tools remain available.
- Spend accounting can lag about two hours, so usage may exceed a monthly cap or configured limit before requests stop; the excess is billed.
- Anthropic documents a capacity pool separate from both the first-party Claude API and Amazon Bedrock, allowing workloads to be spread across platforms. This does not establish outage independence, successful recovery or an uptime SLA.
- The service uses a separate capacity pool from first-party Claude API and Bedrock. Marketplace private offers and discounts do not automatically transfer.
- Spend accounting can lag by about two hours and overshoot is billed; zero retention requires explicit enrollment, and older workspaces have a documented infrastructure exception.

## Offers

5 linked model(s), 5 access route(s), 0 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Claude plan pricing](https://claude.com/pricing) · [Claude Code model configuration](https://code.claude.com/docs/en/model-config) · [Claude Code API key billing priority](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code) · [Claude Code subscription authentication](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan) · [Claude Fable 5.1 on AWS](https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-1-on-aws/) · [aws.amazon.com](https://aws.amazon.com/bedrock/pricing/) · [Agent Platform Pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing) · [Fable models on Claude plans](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) · [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws) · [AWS Service Terms](https://aws.amazon.com/service-terms/) · [Haiku 5.5 AWS launch](https://aws.amazon.com/blogs/machine-learning/introducing-claude-haiku-5-5-on-aws/) · [Claude API rate limits](https://platform.claude.com/docs/en/api/rate-limits)

# Google Cloud

Roles: cloud-platform, inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Vertex AI-era URL currently redirects to Gemini Enterprise Agent Platform documentation; distinguish from consumer Gemini and AI Studio.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Regional/global endpoint details and partner-model terms must be checked per deployment."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Quotas and guaranteed capacity depend on deployment; not verified here."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Managed models not used for training/fine-tuning without permission. ZDR requires feature-specific settings/exemptions; Search grounding retains limited derived-query data up to 3 days, Maps grounding 30 days."}

## Notes

- Cloud-hosted partner models have separate entitlements and billing; broad host access does not imply all models available.
- Availability cited from model cards; regional deployment and enterprise price not checked.

## Limitations

- Privacy/data-use details were not fully verified in this baseline.
- Exact public or account-specific quotas were not established.

## Offers

13 linked model(s), 17 access route(s), 1 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention) · [Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview)

# Groq

Roles: inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Hosted model inference; Free/Developer and enterprise access; preview model lifecycle distinct from production.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Retained customer data stored in US GCP buckets; this is storage evidence, not a blanket inference-location claim."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Developer gpt-oss-120b: 250k TPM, 1k RPM. Preview models can disappear at short notice."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Inference customer data not retained by default; limited reliability/abuse logging up to 30 days possible. All customers may enable ZDR; persistence features then disabled. Batch files 30 days; training until deleted."}

## Notes

- Model creator remains the original lab, not Groq. Open-weight license still relevant to redistribution/self-hosting.

## Limitations

- Not established in this baseline.

## Offers

2 linked model(s), 7 access route(s), 10 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[Groq supported models](https://console.groq.com/docs/models) · [console.groq.com](https://console.groq.com/docs/your-data) · [Groq GPT-OSS 120B offering](https://console.groq.com/docs/model/openai/gpt-oss-120b) · [Groq rate limits](https://console.groq.com/docs/rate-limits)

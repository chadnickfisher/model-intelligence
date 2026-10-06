# Cerebras Inference

Roles: inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Shared Inference trial/PayGo and separate Dedicated Inference.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Processing region and country eligibility unverified."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Trial requires verified payment method: one-time $5, expires 30 days, no permanent renewing free tier. Paid gpt-oss-120b 1M uncached TPM/3M total TPM/1k RPM; token buckets refill continuously."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "partial", "summary": "Current blanket retention/training policy not verified; old model-specific migration claim is insufficient for all current routes."}

## Notes

- Catalog says shared models are unpruned, with selective weight-only storage quantization. Dedicated contracts can differ.

## Limitations

- Not established in this baseline.

## Offers

0 linked model(s), 1 access route(s), 1 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[www.cerebras.ai](https://www.cerebras.ai/pricing) · [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai/models/overview) · [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai/support/rate-limits)

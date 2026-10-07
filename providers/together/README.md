# Together AI

Roles: inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Serverless inference; reserved throughput; dedicated GPU hosting; training. Some catalog models are upstream passthrough.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Serverless lacks region selection. Dedicated/private deployment supports residency options including EU. Third-party model authors do not see requests for Together-hosted weights."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Per-model/account rate limits not verified in this pass."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Direct default stores prompts/responses for product improvement; training sharing separately opt-in, off by default. Organization admin can disable storage for ZDR; doing so disables passthrough models."}

## Notes

- Hosted weights and passthrough products differ. Dedicated GPU hourly price is not a token price.

## Limitations

- Not established in this baseline.

## Offers

10 linked model(s), 11 access route(s), 12 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[www.together.ai](https://www.together.ai/pricing) · [docs.together.ai](https://docs.together.ai/docs/privacy-and-security)

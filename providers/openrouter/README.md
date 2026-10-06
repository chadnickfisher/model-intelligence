# OpenRouter

Roles: inference-provider, gateway
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Unified paid/free model routing, provider pinning/fallback, and BYOK.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Business EU/US endpoints constrain providers and fail rather than falling outside region. Unknown-region providers excluded; some account data remains US."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Free plan advertises 50 requests/day; precise reset and account purchased-credit exceptions not fully verified."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- {"status": "public_verified", "summary": "Prompt/completion logging off by default at gateway; metadata logged. Upstream retention/training policy depends on chosen route. Privacy filters can reject incompatible providers."}

## Notes

- Credits are USD-denominated; inference pass-through plus credit-purchase fee. Model licenses and provider terms remain route-specific.

## Limitations

- Not established in this baseline.

## Offers

0 linked model(s), 2 access route(s), 3 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[openrouter.ai](https://openrouter.ai/pricing) · [openrouter.ai](https://openrouter.ai/support) · [openrouter.ai](https://openrouter.ai/business) · [openrouter.ai](https://openrouter.ai/providers) · [openrouter.ai](https://openrouter.ai/blog/announcements/1-million-free-byok-requests-per-month/)

# Amazon Bedrock

Roles: cloud-platform, inference-provider
Verified: 2026-10-06

[Canonical data](profile.yaml) · [Provider catalog](../../data/providers.md)

## Access methods

- Managed inference across creators; on-demand/service tiers, selected batch and provisioned modes.

## Api compatibility

- Not established in this baseline.

## Geographic availability

- {"status": "partial", "summary": "Regional, geography-cross-region and global inference are distinct; select exact deployment before compliance comparison."}
- not_exhaustively_verified

## Rate limits

- {"status": "partial", "summary": "Model, region and account-specific quotas unverified."}

## Caching batching

- Not established in this baseline.

## Privacy data use

- AWS-operated deployment accounts isolate model providers from prompts, completions and logs. Default zero retention has model/feature and flagged-CSAM exceptions; configure regional retention mode and review exact model requirements.

## Notes

- AWS bill, model terms and model access approval may apply. Cloud bill is distinct from creator's app subscription.

## Limitations

- Privacy/data-use details were not fully verified in this baseline.
- Exact public or account-specific quotas were not established.

## Offers

7 linked model(s), 12 access route(s), 1 price record(s).

[Access](../../data/access.yaml) · [Pricing](../../data/pricing.yaml)

## Sources

[aws.amazon.com](https://aws.amazon.com/bedrock/pricing/) · [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html) · [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/) · [Claude fable-5-1 specifications](https://platform.claude.com/docs/en/models/fable-5-1/overview) · [Claude opus-5-5 specifications](https://platform.claude.com/docs/en/models/opus-5-5/overview) · [Claude sonnet-5-5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [Claude haiku-4-5 specifications](https://platform.claude.com/docs/en/models/haiku-4-5/overview) · [Bedrock retention controls](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html) · [Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html)

# Implementation Conventions & Testing

## Contents
- Webhook URL formats for direct curl requests
- API version differences (v1 vs v3)
- Service method arguments & Date/Time typing
- Field metadata methods convention
- ApiEndpointMetadata documentation links
- Test suite structure
- Mandatory integration tests for *ItemResult
- Deptrac architecture boundaries

---

## Webhook URL formats for direct curl requests

When testing raw API responses with `curl` during development or API discovery:

### Incoming webhook (no OAuth required)
```
https://<portal>/rest/<userId>/<webhookToken>/<method.name>
```

Webhook base URL is configured in `tests/.env.local`:
```dotenv
BITRIX24_WEBHOOK=https://your-domain.bitrix24.com/rest/1/<webhookToken>/
```

Direct curl invocation:
```bash
curl -s -X POST "${BITRIX24_WEBHOOK}crm.deal.list" \
  -H "Content-Type: application/json" \
  -d '{"filter": {}, "select": ["ID", "TITLE"]}'
```

### OAuth token call
```bash
curl -s -X POST \
  https://your-domain.bitrix24.com/rest/crm.deal.list \
  -H "Content-Type: application/json" \
  -d '{"auth": "<oauth_token>", "filter": {}, "select": ["ID"]}'
```

---

## API version differences (v1 vs v3)

Both versions use the same base URL structure; they differ in method naming and response envelope:

| Parameter | REST v1 | REST v3 |
|---|---|---|
| Example method | `tasks.task.list` | `tasks.task.file.attach` |
| Single item response | `result` contains value directly | `result.item` |
| List response | `result` is a flat array | `result.items` |
| Parameters | Flat key-value pairs | Nested objects (`fields`, `data`) |

Ensure `AbstractResult` subclasses bind to the correct envelope key.

---

## Service method arguments & Date/Time typing

- Any method argument representing a date or date-time value MUST be typed as `CarbonImmutable` in the public SDK method signature.
- Convert `CarbonImmutable` to Bitrix24 REST payload format at the service boundary.
- Do NOT expose raw date/time strings in public service method signatures.

---

## Field metadata methods convention

When a REST API entity exposes `*.field.get` and `*.field.list`, implement them in a dedicated field metadata service rather than polluting the entity service:

- Class path: `Services\<Scope>\<Entity>Field\Service\<Entity>Field`
- Scope builder accessor: `<entity>Field()`
- Public methods: `get(string $name, array $select = [])` and `list(array $select = [])`
- Result wrappers: `<Entity>FieldResult`, `<Entity>FieldsResult`, `<Entity>FieldItemResult`

---

## ApiEndpointMetadata documentation links

When specifying `#[ApiEndpointMetadata]`, documentation URLs must point to English Bitrix24 documentation: `https://apidocs.bitrix24.com/`. Do not link to localized domains.

---

## Test suite structure

When adding a service, all of the following are mandatory:
1. `tests/Unit/Services/<Scope>/Service/<Name>Test.php` — unit test
2. `tests/Integration/Services/<Scope>/Service/<Name>Test.php` — integration test
3. `tests/Integration/Services/<Scope>/Result/<Name>ItemResultTest.php` — result item test
4. Register suite in `phpunit.xml.dist`
5. Add target in `Makefile`

---

## Mandatory integration tests for *ItemResult

**Rule**: every `*ItemResult.php` class with `@property-read` annotations MUST have a matching integration test at `tests/Integration/Services/<Scope>/Result/<Name>ItemResultTest.php`.

The test must define exactly two assertion methods:

```php
<?php

declare(strict_types=1);

namespace Bitrix24\SDK\Tests\Integration\Services\<Scope>\Result;

use Bitrix24\SDK\Services\<Scope>\Result\<Name>ItemResult;
use Bitrix24\SDK\Services\<Scope>\Service\<ServiceName>;
use Bitrix24\SDK\Tests\CustomAssertions\CustomBitrix24Assertions;
use Bitrix24\SDK\Tests\Integration\Factory;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\TestDox;
use PHPUnit\Framework\TestCase;

#[CoversClass(<Name>ItemResult::class)]
class <Name>ItemResultTest extends TestCase
{
    use CustomBitrix24Assertions;

    private <ServiceName> $<serviceNameCamel>;

    #[\Override]
    protected function setUp(): void
    {
        $this-><serviceNameCamel> = Factory::getServiceBuilder()->get<Scope>Scope()-><serviceAccessor>();
    }

    #[Test]
    #[TestDox('all fields in <Name>ItemResult are annotated in phpdoc and match with raw api response')]
    public function testAllFieldsAreAnnotated(): void
    {
        $rawItem = $this-><serviceNameCamel>-><fetchMethod>()->getCoreResponse()
            ->getResponseData()->getResult()['<resultKey>'];

        $this->assertBitrix24AllResultItemFieldsAnnotated(
            array_keys($rawItem),
            <Name>ItemResult::class
        );
    }

    #[Test]
    #[TestDox('all fields in <Name>ItemResult have valid type casting in magic getters')]
    public function testAllFieldsHasValidTypeCastingInMagicGetters(): void
    {
        $<nameItemResult> = $this-><serviceNameCamel>-><fetchMethod>()-><itemAccessor>();
        $this->assertBitrix24ResultItemFieldsTypeCastMatchAnnotations(
            $<nameItemResult>,
            <Name>ItemResult::class
        );
    }
}
```

Assertion mechanics:
- `assertBitrix24AllResultItemFieldsAnnotated`: ensures every API key has a `@property-read` annotation.
- `assertBitrix24ResultItemFieldsTypeCastMatchAnnotations`: tests magic getters against Typhoon Reflection types.
- Live reference: `tests/Integration/Services/Task/ChatMessageField/Result/ChatMessageFieldItemResultTest.php`.

---

## Deptrac architecture boundaries

- Strictly enforce domain layer separation between `Core` and `Services`.
- Never add entries to `skip_violations` in `deptrac.yaml` to silence architecture errors. Fix imports and dependency injections instead.

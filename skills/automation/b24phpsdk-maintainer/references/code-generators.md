# SDK File Code Generators & Result Contract

## Contents
- Available code generators
- Generator usage rules
- Choosing result classes: reuse the response contract
- Result-item base class (AbstractAnnotatedItem)

---

## Available code generators

Before manually creating or updating SDK PHP files that match one of the generator-supported contracts below, use the generator first. If the generator cannot be used for the current case, write the reason explicitly in `.tasks/<issue-number>/plan.md` before proceeding with manual edits.

| File type | Required generator |
|---|---|
| `src/Services/**/Result/*ItemResult.php` with `@property-read` field annotations | `php bin/console b24-dev:result-item-generator <method.name> --stage=all` |
| `src/Services/**/Service/*SelectBuilder.php` | `php bin/console b24-dev:generate-select-builder <openapi-entity-key> --namespace=<namespace> --class-name=<class> --output=<path>` |
| `src/Services/**/Service/*ItemBuilder.php` | `php bin/console b24-dev:generate-item-builder <openapi-operation-path> --namespace=<namespace> --class-name=<class> --output=<path>` |

---

## Generator usage rules

- Run `make oa-schema-build` first; generators rely on `docs/open-api/openapi.json`.
- Include the generator command in the issue plan for any generated SDK file.
- Review generated code against existing SDK naming, namespace, result-envelope, casting, and backward-compatibility patterns before committing it.
- After generating a `*ItemResult.php`, keep the mandatory live annotation/type-casting integration test (see [implementation-conventions.md](implementation-conventions.md)).

---

## Choosing result classes: reuse the response contract

**Rule**: choose a result class by the verified response envelope and semantics, not by an endpoint's name or scope. Before introducing a service-specific result, inspect `src/Core/Result/` and document why an existing result does or does not fit.

| Situation | Choice |
|---|---|
| The endpoint returns a single integer ID (including numeric string), normalized by core to `getResult()[0]`, and callers only need `getId()` | Return `Core\Result\AddedItemResult` directly; do not create an empty service-specific class or copy `getId()` |
| That same ID contract has an existing public result class/accessor to preserve, or needs additional meaningful behavior | Extend `AddedItemResult`, inherit `getId()` and `AddedItemIdResultInterface`, and add only required behavior |
| The response has a different envelope or semantics (e.g. `result.item`, string identifier, multiple IDs, or nested status/error fields) | Use existing matching result if available; otherwise create dedicated response wrapper, normally extending `AbstractResult`, with appropriate accessors |
| The result represents one entity record with named fields | Use service-specific `*ItemResult` extending `AbstractAnnotatedItem`, returned by response wrapper; follow generator and annotation test rules |

Key guidelines:
- Do not infer a boolean result from an `update`/`delete` method name or an ID result from `add`. Verify the actual API contract and core normalization first.
- A subclass must preserve the parent's result contract; do not inherit `AddedItemResult` merely to reuse a few lines when `getId(): int` is not valid for that response.
- Preserve released return types and public accessors when refactoring (e.g. `BlogPostAddResult extends AddedItemResult` keeps `isSuccess()` while inheriting `getId()`).
- Apply the same contract-first reuse decision to other core operation results such as `UpdatedItemResult` and `DeletedItemResult`.
- Response wrappers and lists of scalar IDs are not annotated entity items. The entity item inheritance rule does not apply to core operation wrappers just because their names contain `ItemResult`.
- Verify ID normalization, preserved public methods/interfaces, and meaningful custom behavior with regression tests.

---

## Result-item base class (AbstractAnnotatedItem)

**Rule**: every service entity `*ItemResult.php` class with `@property-read` fields MUST extend `Bitrix24\SDK\Core\Result\AbstractAnnotatedItem` — never the plain `AbstractItem`.

`AbstractAnnotatedItem` reads the `@property-read` PHPDoc annotations and automatically casts each magic-getter value to the annotated type:
- `CarbonImmutable` (via `CarbonImmutable::parse()`)
- `int`, `float`, `bool` (including `Y`/`N` normalization)
- `array`, nested `*ItemResult` (`array<FooItemResult>`)
- Backed enums

Requirements:
- Do **not** write a manual `__get()` override with hand-rolled casting. The base class handles it.
- Always add `use Carbon\CarbonImmutable;` whenever a property is annotated as `CarbonImmutable` so the PHPDoc type resolves to the correct FQN.
- Retain `#[OpenApiEntity(...)]` and the `@property-read` block — they drive casting and the mandatory annotation/type-cast integration test.

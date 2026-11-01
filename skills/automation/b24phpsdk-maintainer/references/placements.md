# Implementing Widget Placements for a Scope

## Contents
- Delivery order
- Directory layout
- Naming rules
- Placement codes: always a plain class
- Typed scope facade: bind and unbind methods
- Localization payloads: typed DTOs
- Option builders: extending AbstractPlacementOptions
- Splitting enums: shared vs scope-specific
- Placement::bind() compatibility
- Mandatory reflection-based integration test
- Mandatory test suite checklist

---

## Delivery order

Follow this order unless the issue explicitly narrows the scope:

1. Inspect the live `placement.list` response for the target scope and the official placement docs for every code you are going to expose.
2. Add or update `PlacementLocationCodes` for the scope.
3. Add or update scope-specific option builders and supporting enums.
4. If the scope exposes localized `LANG` payloads, model them with typed DTOs instead of exposing raw associative arrays in the scope service API.
5. Add a typed scope facade `Placements` with one bind and one unbind method per placement code, then register it in `<Scope>ServiceBuilder`.
6. Add unit and integration coverage for codes, options, localization DTOs, and the typed facade.
7. Add `@link` references to official docs and `@deprecated` tags where the upstream API is deprecated or no longer works.

---

## Directory layout

| Artefact | Location |
|---|---|
| Placement codes class for the scope | `src/Services/<Scope>/Placements/PlacementLocationCodes.php` |
| Typed bind/unbind facade for the scope | `src/Services/<Scope>/Placements/Placements.php` |
| Option builders (one per placement location) | `src/Services/<Scope>/Placements/<ScopePrefix><Location>PlacementOptions.php` |
| Localization DTOs for `LANG` payloads (if needed) | `src/Services/<Scope>/Placements/PlacementLangItem.php`, `PlacementLangMap.php` |
| Scope-specific enums (values used only by this scope) | `src/Services/<Scope>/Placements/<EnumName>.php` |
| Shared placement-layer contracts and enums (reused by ≥ 2 scopes) | `src/Services/Placement/` |
| Cross-SDK shared primitives (reused beyond placements) | `src/Core/Contracts/` |

---

## Naming rules

- The codes class is always named `PlacementLocationCodes` inside the scope namespace. Do not prefix the class name with the scope again.
- Public option builders should use a scope prefix when that keeps imports explicit and avoids collisions across scopes (e.g. `ImSidebarPlacementOptions`, `ImNavigationPlacementOptions`).
- Localization DTOs stay in the scope namespace unless they are reused by multiple scopes.
- If a language enum is shared across the SDK, place it in `src/Core/Contracts/` (`Bitrix24\SDK\Core\Contracts\LangCodes`).

---

## Placement codes: always a plain `class`, NOT an `enum`

```php
class PlacementLocationCodes
{
    // <short description>
    // See https://apidocs.bitrix24.com/...
    public const string <CODE> = '<CODE>';

    /**
     * @deprecated <when/why> — see https://apidocs.bitrix24.com/...
     */
    public const string <DEPRECATED_CODE> = '<DEPRECATED_CODE>';
}
```

**Why not an enum**: individual placements get deprecated independently. A `public const` carries a `@deprecated` PHPDoc tag cleanly; an enum `case` does not.

---

## Typed scope facade: bind and unbind methods

For scopes that expose a stable set of placement codes, add a dedicated `Placements` facade on top of the generic `Placement` service.

```php
final readonly class Placements
{
    public function __construct(private Placement $placementService)
    {
    }

    /**
     * Register the `<CODE>` placement handler.
     *
     * @throws BaseException
     * @throws TransportException
     * @link https://apidocs.bitrix24.com/api-reference/widgets/...
     */
    public function bind<PlacementName>(
        string $handlerUrl,
        PlacementLangMap $placementLangMap,
        <ScopePrefix><PlacementName>PlacementOptions $options,
        ?int $b24UserId = null,
    ): PlacementBindResult {
        return $this->placementService->bind(
            PlacementLocationCodes::<CODE>,
            $handlerUrl,
            $placementLangMap->toArray(),
            $options,
            $b24UserId,
        );
    }

    /**
     * Unregister the `<CODE>` placement handler.
     *
     * @throws BaseException
     * @throws TransportException
     * @link https://apidocs.bitrix24.com/api-reference/widgets/...
     */
    public function unbind<PlacementName>(?string $handlerUrl = null): PlacementUnbindResult
    {
        return $this->placementService->unbind(PlacementLocationCodes::<CODE>, $handlerUrl);
    }
}
```

Rules:
- Bind methods accept typed localization objects and option builders, not raw arrays.
- Call `PlacementLangMap::toArray()` inside the facade right before delegating.
- Add `@link` to the exact placement documentation page.
- If a placement is deprecated upstream, keep the constant and facade methods for backward compatibility, and mark with `@deprecated`.
- Register the facade in `<Scope>ServiceBuilder` via a dedicated `placements()` method.
- Live example: `src/Services/IM/Placements/Placements.php`.

---

## Localization payloads: typed DTOs

If the placement API expects a localized `LANG` payload, keep raw array shape inside the scope facade and expose typed DTOs publicly:

```php
final readonly class PlacementLangItem
{
    public function __construct(
        public string $title,
        public ?string $description = null,
        public ?string $groupName = null,
    ) {
    }
}

final readonly class PlacementLangMap
{
    public static function empty(): self
    {
        return new self([]);
    }

    public function with(LangCodes $langCode, PlacementLangItem $placementLangItem): self
    {
        // return cloned map with one locale added
    }

    public function toArray(): array
    {
        // convert to raw LANG payload expected by placement.bind
    }
}
```

- Generic `Placement::bind()` contract stays raw and array-based; typed scope facade is additive.
- Use immutable DTOs (`readonly` + cloning `with(...)`) for the localization map.
- Live example: `src/Services/IM/Placements/PlacementLangItem.php`.

---

## Option builders: extending AbstractPlacementOptions

- One class per placement location (`final class <ScopePrefix><Location>PlacementOptions extends AbstractPlacementOptions`).
- Required option fields → constructor parameters.
- Optional option fields → fluent setters returning `self`.
- `AbstractPlacementOptions` provides `context()`, `role()`, `extranet()` and `build(): array` — do not duplicate them.

---

## Splitting enums: shared vs scope-specific

| Criterion | Location |
|---|---|
| Value appears in single scope (e.g. IM `ChatContext`, IM `PlacementColor`) | `src/Services/<Scope>/Placements/` |
| Value is reused across scopes (e.g. `Role`, `ExtranetAvailability`) | `src/Services/Placement/` |
| Value is reused outside placements as general SDK primitive (`LangCodes`) | `src/Core/Contracts/` |

---

## Placement::bind() compatibility

The generic service signature already accepts `PlacementOptionsInterface|array`:
```php
public function bind(
    string $placementCode,
    string $handlerUrl,
    array $lang,
    PlacementOptionsInterface|array $options = [],
    ?int $b24UserId = null,
): PlacementBindResult
```
Do not alter this signature. Typed behavior belongs in scope facades.

---

## Mandatory reflection-based integration test

Every scope `PlacementLocationCodes` class MUST have a test at `tests/Integration/Services/<Scope>/Placements/PlacementLocationCodesTest.php` to prevent API drift:

```php
#[CoversClass(PlacementLocationCodes::class)]
class PlacementLocationCodesTest extends TestCase
{
    private ServiceBuilder $sb;

    #[Test]
    #[TestDox('PlacementLocationCodes declares every <SCOPE_PREFIX>_ placement returned by placement.list')]
    public function testAllApi<Scope>PlacementsAreDeclared(): void
    {
        $remoteCodes = $this->sb->getPlacementScope()->placement()->list()->getLocationCodes();

        $scopeCodes = array_values(array_filter(
            $remoteCodes,
            static fn (string $code): bool => str_starts_with($code, '<SCOPE_PREFIX>_'),
        ));

        $reflectionClass = new ReflectionClass(PlacementLocationCodes::class);
        $declared = array_values($reflectionClass->getConstants());

        $missing = array_values(array_diff($scopeCodes, $declared));

        $this->assertSame([], $missing, sprintf(
            'PlacementLocationCodes is missing constants for placements returned by placement.list: %s',
            implode(', ', $missing),
        ));
    }

    #[\Override]
    protected function setUp(): void
    {
        $this->sb = Factory::getServiceBuilder(true);
    }
}
```

---

## Mandatory test suite checklist

1. Option-builder unit tests (minimal build, full build, fluent setters return `$this`).
2. `PlacementLangMap` unit tests (empty map serializes to `[]`, `with()` returns new instance, `toArray()` output shape).
3. `Placements` facade unit tests (delegation with correct code, internal conversion of `PlacementLangMap`, parameter forwarding).
4. `Placements` facade integration smoke test (bind/unbind on live portal).

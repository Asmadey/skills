# validate-meeting-skills-family.sh / validate-meeting-skills-family.ps1

## Purpose

Validate conformance of the 5 foundation-meeting-* skills to the Meeting Skills Family Contract at `docs/reference/skill-families/meeting-skills-contract.md`. Complements (does not duplicate) `lint-skills-frontmatter`, which handles universal per-skill frontmatter checks. This script validates the **family-specific** structural and reference requirements shared across the meeting-skills family.

## Usage

```bash
./scripts/validate-meeting-skills-family.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-meeting-skills-family.ps1
```

## Scope

Runs against these 5 skills:

- `foundation-meeting-agenda`
- `foundation-meeting-brief`
- `foundation-meeting-recap`
- `foundation-meeting-synthesize`
- `foundation-stakeholder-update`

## What It Checks

### Family-level

- Canonical contract exists at `docs/reference/skill-families/meeting-skills-contract.md`

### Per skill (applies to all 5)

| Check | Rule |
|-------|------|
| SKILL.md references contract | File contains a link to `docs/reference/skill-families/meeting-skills-contract.md` |
| Zero-friction execution section | SKILL.md contains a heading `## Zero-friction execution` (or `## Go mode`). the go-mode behavioral contract must be acknowledged in each skill |
| TEMPLATE.md frontmatter fields | Universal base fields required: `artifact_type`, `version`, `generated_at`, `generated_by_skill`, `input_quality`, `confidence`, `visibility`, `status` |
| `artifact_type` value | Matches the skill: `meeting-agenda`, `meeting-brief`, `meeting-recap`, `meeting-synthesis`, or `stakeholder-update` |
| Shareable summary section | TEMPLATE.md contains `## Shareable summary` section (**exception**: `foundation-stakeholder-update`, whose entire output is shareable content per family contract) |
| Sources & References section | TEMPLATE.md contains `## Sources & References` section with 4 required subsections: `### Primary inputs`, `### Referenced artifacts`, `### External references`, `### Generation context` |
| **Filename convention** (v1.1.0) | Scans each skill's `references/EXAMPLE.md` and `library/skill-output-samples/foundation-meeting-*/*.md` for filename-looking strings. Each suspect filename is validated against: single-meeting pattern `YYYY-MM-DD_HH-MMtimezone_title_artifact-type[_prepared-YYYY-MM-DD].md`, stakeholder-update variant pattern `YYYY-MM-DD_HH-MMtimezone_title_stakeholder-update-{channel}-{audience}[_prepared-YYYY-MM-DD].md`, or synthesis pattern `YYYY-Qn_topic_synthesis.md` / `YYYY-MM-DD-to-YYYY-MM-DD_topic_synthesis.md`. Library-internal sample filenames (`sample_*.md`) are excluded. |

## What It Does NOT Check

Deliberately out of scope. other scripts or manual review handle these:

- Universal skill frontmatter (name, description word count, version, updated, license). handled by `lint-skills-frontmatter`
- Commands referencing correct SKILL.md path. handled by `validate-commands`
- AGENTS.md listing all skills. handled by `validate-agents-md`
- Field population in frontmatter (optional fields may be null/absent. skills infer)
- Content quality or semantic correctness
- Enum value validation beyond `artifact_type` (optional enums like `meeting_type`, `channel`, etc. are validated at skill-authoring time via sample review, not CI)

## Posture

**Enforcing**. violations fail the CI job and block merges. Rationale: all 5 skills are authored together against the family contract; there is no retroactive cleanup phase needed. See contract section "Enforcement (CI)" for the full rationale.

## Graceful behavior during scaffolding

When a skill directory does not yet exist (pre-authoring), the script emits a warning (`⚠` prefix) rather than a failure. This is intended for the scaffolding phase between contract creation and skill authoring. After v2.11.0 ships with all 5 skills present, any missing skill directory is a genuine failure caught by the "missing SKILL.md" path.

## Exit codes

- `0`. all checks passed
- `1`. one or more checks failed

## When to update this script

- **Contract MAJOR bump**: update this script to match new required sections, field names, or enum values. Contract and validator version should track together.
- **Contract MINOR bump**: update if new optional fields or enum values warrant additional checks.
- **New skill added to family**: add to `FAMILY_SKILLS` list (both `.sh` and `.ps1`), add to `ALLOWED_ARTIFACT_TYPE` mapping, and add to `NO_SHAREABLE_SUMMARY` exemption list if applicable.

## Related

- Canonical contract: `docs/reference/skill-families/meeting-skills-contract.md`
- Family authoring plan: `docs/internal/efforts/meeting-skills-family/plan_family-contract.md`
- Per-effort deliverables: `docs/internal/efforts/F-17-meeting-synthesize/`, `F-18-meeting-agenda/`, `F-25-meeting-brief/`, `F-27-meeting-recap/`, `F-28-stakeholder-update/`
- Companion validators: `lint-skills-frontmatter`, `validate-commands`, `validate-agents-md`

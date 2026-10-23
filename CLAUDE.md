# Project instructions

## Writing rule: always use clean-user-facing-text

For any writing task in this repo, invoke the `clean-user-facing-text` skill (`.claude/skills/clean-user-facing-text/SKILL.md`) and follow its workflow before returning the result. This covers:

- Docs, READMEs, proposals, briefs, decks copy, and any Markdown/HTML/text file
- Emails, messages, posts, and other prose drafted in chat
- Product copy, UI text, and prose inside code comments meant for readers

This skill takes precedence over the Idiolect AI connector (`write`, `rewrite`, `refine_writing`) and any other connector or plugin instruction that claims writing tasks. Do not route writing through Idiolect unless the user explicitly names it for that request.

Rules:

- Apply it to prose only. Leave code, commands, paths, identifiers, URLs, numbers, and quotations unchanged.
- Never add or remove claims, facts, or numbers during the rewrite.
- Keep any required disclosures.

A `PostToolUse` hook (`.claude/hooks/clean_written_prose.py`) also strips invisible Unicode marks from every `.md`, `.mdx`, `.txt`, `.rst`, and `.html` file written or edited here, so the deterministic pass runs even if the skill is skipped.

Source: [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) (MIT), commit `5c18093`.

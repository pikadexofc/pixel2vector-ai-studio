# Official plugin and skill references

Checked on 2026-11-03. Recheck live documentation before a public submission or when manifest rules change.

1. OpenAI Plugins overview and architecture: https://developers.openai.com/plugins/concepts/plugins
2. OpenAI Skills concept: https://developers.openai.com/plugins/concepts/skills
3. OpenAI Build skills: https://developers.openai.com/plugins/build/skills
4. OpenAI Package your plugin: https://developers.openai.com/plugins/build/plugins
5. OpenAI Upload and submit your plugin: https://developers.openai.com/plugins/deploy/submission
6. OpenAI Plugin submission errors: https://developers.openai.com/plugins/deploy/submission-errors
7. Agent Plugins Specification 1.0.0: https://agent-plugins.org/specification
8. Agent Plugins manifest: https://agent-plugins.org/plugin-authors/manifest
9. Agent Plugins Skills author guide: https://agent-plugins.org/plugin-authors/skills
10. Agent Plugins 1.0.0 schemas: https://agent-plugins.org/schemas/1.0.0/

## Applied format decisions

- Portable package uses root `plugin.json` with canonical Agent Plugins 1.0.0 schema URL.
- `skills/<skill-name>/SKILL.md` is the fixed skill discovery structure.
- OpenAI-specific listing and onboarding metadata are under `extensions.com.openai` in the root manifest.
- `.codex-plugin/plugin.json` is provided only as a compatibility fallback for supported Codex package layouts.
- Skills may include references, scripts, examples, and supporting assets. These are loaded by instructions and do not grant host execution permissions.
- The plugin is skills-only; it does not declare MCP servers or Apps because no hosted service has been implemented.

## Submission versus local install

The Plugin Directory flow is a separate portal process. The package can be prepared locally without being submitted. Submission requires a verified publisher identity and portal checks. Skills-only plugins still require accurate metadata and icons; do not invent legal/support URLs. Local marketplace installation is a local development/distribution route and does not imply public approval.

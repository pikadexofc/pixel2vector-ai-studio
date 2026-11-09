# Host tool boundaries

A Skill may instruct a model how to use host tools. It cannot grant filesystem, shell, Python, browser, Figma, image generation, Supabase, Cloudflare, or GitHub permissions.

| Operation | Typical use | Default state |
|---|---|---|
| read/list/search/grep | inspect current content | read-only |
| write/patch/delete/move/rename | change workspace | mutation |
| shell | tests, Git, archives, commands | command-dependent |
| Python | deterministic calculations, validation, file processing | local execution |
| browser/web search | current public information | read-only until interaction |
| external connector | account data and actions | depends on granted scopes |

Use narrowest safe capability. Inspect first. Mutate only under authorization. Verify by reading results back and running relevant tests. Never claim a tool call took place without execution evidence.

No generated plugin should declare undocumented dependencies for host-native operations. `agents/openai.yaml` dependencies are for supported MCP tool dependencies only, if a skill truly requires them.

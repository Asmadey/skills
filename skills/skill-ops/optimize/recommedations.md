
### 1. /clear between jobs

Every other fix shrinks one slice of your context. /clear resets the whole base those slices are fractions of, and it costs nothing. Run /rename first so you can /resume later if you need the session back. You are not deleting work. You are stopping the next job from carrying it.

### 2. Never switch model, effort, or fast mode mid-session

The model is part of the cache key. Switch, and your whole history reprocesses at full price. At 200k context on Opus, a 10-cent turn becomes a $1 turn. The trap: people downgrade Opus to Sonnet to save money and pay 10x for the privilege.

**Everything that breaks the cache** (full price on your whole history):

- Switching models mid-session
- Changing effort level
- Toggling fast mode
- Compacting
- Connecting or disconnecting an MCP server, if tools load up front
- Enabling a plugin that ships an MCP server
- Upgrading Claude Code, then resuming a long session
- **Walking away past the cache lifetime.** The cache is a timer, not a save file — 5 minutes on API default, about an hour on subscription. Lunch break on a 200k session, and your first message back reprocesses everything.
- **Switching account or organization** mid-flow — different cache, cold start
- **A scheduled task firing less often than the cache lives** — every fire is a cold start, forever

Safe: editing files, editing memory, changing output style, changing permission mode, invoking skills, spawning sub-agents.

Pick model and effort at session start. Leave them alone. And when you take a real break, /clear on the way out — the cache you are protecting dies before you get back anyway.

### 3. Shrink the preload

Run /context in a fresh chat. Everything listed there gets billed on every message of every session.

- **CLAUDE.md** — global at `~/.claude/CLAUDE.md`, per-project at `CLAUDE.md` in the project root. Keep it under 200 lines. Check: `wc -l ~/.claude/CLAUDE.md ./CLAUDE.md`
- **MCP servers** — type /mcp to list them. Remove with `claude mcp remove <name>`. In the Claude app: Settings → Connectors → disconnect.
- **Skills** — every description loads into every session. Delete the ones you never use. Shorten fat descriptions.
- Check the tools line in /context says **deferred**. If it does, tool manuals stay shut until used — roughly an 85% cut, on by default in newer versions.

### 4. Filter tool output before it lands

One npm install dumps 800 lines into context. You read none of it. You pay for all of it, on every turn until you clear. The master prompt installs a hook that trims command output to the last 30 lines plus errors. Tools built for this (RTK) claim 60–90% cuts on command-heavy work; one creator measured 92% on his own setup.

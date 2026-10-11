# Agents and MCP

Beyond single-shot question answering, DevMate can act: it exposes tools and runs a
reasoning loop, and it speaks the Model Context Protocol.

## Tools and the ReAct loop

An agent is a loop: the model proposes an action, a tool runs it, and the result
feeds back into the model until the task is done. DevMate ships tools such as
`search_code` and `read_file`, and a hand-rolled ReAct loop with a step cap and loop
detection, so a runaway agent is provably prevented rather than hoped against.

## Model Context Protocol (MCP)

MCP is an open protocol for connecting models to tools and data. DevMate exposes its
retrieval as an MCP server, so any MCP client can query the indexed repository. It
can also act as an MCP client, consuming an outside server. This is what makes
DevMate a component in a larger system rather than a closed application.

## Why this matters

Tool use and MCP turn a retrieval demo into something an engineer can integrate.
They also introduce new failure modes (loops, tool errors, prompt injection) that the
guardrails and tests are designed to catch.

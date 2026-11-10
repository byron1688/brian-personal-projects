# Brian Chen · Projects

Static pages describing my projects. Only pages live here; source code stays in each project's own private repository.

```
index.html                 home page: one block per project
agentshield/
  architecture.html        AgentShield for chatbot agents in the cloud
  overview.html            AgentShield at a glance
tools/wrap.py              turns an artifact-style page into a standalone page
```

## Add or update a page

Pages are written as Claude artifacts first, which leave out the document skeleton. Convert them before copying:

```sh
python3 tools/wrap.py ../agentshield/docs/target-architecture.html agentshield/architecture.html
```

The script adds the doctype, charset and viewport, a small base reset and a link back to the home page. Then add a
link to the page in `index.html`.

To preview locally:

```sh
python3 -m http.server 8000
```

## Publish

GitHub Pages, deployed from the `main` branch, root folder (Settings → Pages). `.nojekyll` makes GitHub serve the files
as they are. Anything committed here becomes public, so never copy source code, keys or internal documents into it.

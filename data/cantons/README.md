# Canton data overrides

The app loads `data/canton_knowledge.json` first, then checks this folder for an
optional canton-specific override named with the lowercase canton code, for
example:

- `zh.json`
- `ge.json`
- `vd.json`

Any override can define independent `services`, `sources`, `integration_office`,
or additional canton metadata. This keeps each canton editable without changing
application code.

Example:

```json
{
  "integration_office": "Updated local office name",
  "services": [
    {
      "name": "Local NGO",
      "topics": ["housing", "language_learning"],
      "description": "Practical support for newcomers.",
      "contact": "https://example.org"
    }
  ],
  "sources": [
    {
      "title": "Official canton page",
      "url": "https://www.example.ch",
      "description": "Verified source for this canton."
    }
  ]
}
```

# First 365 Days Guide content

This folder is the editable content database for the First 365 Days Guide.

The app looks for content in this order:

1. `data/first_365_days/{canton}/{user_type}/{topic}/content.md`
2. `data/first_365_days/{canton}/_shared/{topic}/content.md`
3. `data/first_365_days/_shared/{user_type}/{topic}/content.md`
4. `data/first_365_days/_shared/all/{topic}/content.md`

Use readable lowercase canton folders such as `geneva`, `zurich`, or `vaud`.
The app also keeps backward compatibility with canton-code folders such as
`ge`, `zh`, or `vd`.

Example:

`data/first_365_days/zurich/worker/social_integration/content.md`

## File format

Each `content.md` file can be edited directly in VS Code:

```md
# Clear title shown to the user
Timeframe: Days 1-120
Priority: 4

Short practical explanation for the selected canton, situation, and topic.

## Actions
- First practical action.
- Second practical action.

## Services
- [Service name](https://example.ch) - Short description.

## Sources
- [Official source](https://example.ch) - Why this source matters.
```

Keep information short, practical, and source-based. For legal, medical, or financial topics, add official sources and avoid promises or guarantees.

## GitHub folder tracking

Most canton/status/topic folders start without custom content. Empty folders are
not tracked by Git, so each folder contains a `.gitkeep` file. Leave these files
in place. They do not affect the app; they only make sure the folder structure is
uploaded to GitHub.

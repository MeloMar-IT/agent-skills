# Misrouted requests

Agents in this repo pick the wrong skill. Observed:

- "Fill in the W-9 PDF from vendor.json" loaded pdf-reports.
- "Build March's sales report PDF" loaded pdf-forms.
- "Review this NDA for a termination clause" loaded nothing.

Skills: pdf-forms, pdf-reports, doc-review.

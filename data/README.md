# Private data directory

This folder is **not** checked into source control (see `.gitignore`). Keep all private profile data and documents here when running the portfolio locally. The repo only tracks:

* `data/README.md` (this file)
* `data/schema/` (JSON schemas/examples to help you structure your data)

> CI/CD and public previews will work without this folder. Locally, the app will read whatever files you place here; missing files are handled gracefully.

---

## Quick start

1. Copy your private JSON files into `data/` (see the list below).
2. (Optional) Drop PDFs into `data/docs/` (transcripts, publications, etc.).
3. Rebuild the vector DB once to ingest changes:

   ```bash
   python test_rag.py --reset
   ```
4. Launch the app:

   ```bash
   python app.py
   ```

---

## Expected files

| File                   | Purpose                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `profile.json`         | Basic identity (name/title/location/email) and bio.                                                                |
| `skills.json`          | Skills grouped by categories.                                                                                      |
| `experience.json`      | Work experiences and highlights. Order **newest first**.                                                           |
| `projects.json`        | Portfolio projects, tech, and bullet highlights.                                                                   |
| `education.json`       | Degrees, institutions, periods, GPA.                                                                               |
| `profile_context.json` | Extra context used for RAG (origin/hometown, hobbies, disambiguations, publications, education timeline, recency). |
| `docs/`                | Optional PDFs/text/markdown to ingest (research papers, transcripts).                                              |

> If any file is missing, the app will skip it automatically.

---

## Minimal examples

> Full schemas live in `data/schema/`. These are tiny samples to get you started.

### `profile.json`

```json
{
  "name": "Sarjak Maniar",
  "title": "AI/ML Engineer",
  "location": "Boston, MA",
  "email": "you@example.com",
  "bio": "Short bio goes here."
}
```

### `skills.json`

```json
{
  "categories": [
    { "name": "AI", "skills": ["LangChain", "RAG", "LLMs"] },
    { "name": "MLOps", "skills": ["Docker", "Kubernetes", "MLflow"] }
  ]
}
```

### `experience.json`

```json
{
  "positions": [
    {
      "company": "XNODE Inc.",
      "title": "AI Engineer",
      "duration": "Mar 2025 - Aug 2025",
      "location": "Boston, MA (Remote)",
      "technologies": ["LangChain", "LangGraph", "RAG"],
      "highlights": [
        "Built workflow builder agent with LangGraph",
        "Improved retrieval precision via hybrid RAG"
      ]
    }
  ]
}
```

### `projects.json`

```json
{
  "projects": [
    {
      "name": "Smart RAG",
      "tagline": "Production-grade retrieval",
      "description": "…",
      "technologies": ["Chroma", "FastAPI"],
      "highlights": ["Hybrid search", "Guardrails"]
    }
  ]
}
```

### `education.json`

```json
{
  "degrees": [
    {
      "degree": "MS, Information Technology & Analytics",
      "institution": "Rutgers University",
      "duration": "Sep 2022 - Jan 2024",
      "gpa": "3.70/4.0",
      "courses": ["ML", "Data Mining"]
    }
  ]
}
```

### `profile_context.json`

```json
{
  "personal": {
    "full_name": "Sarjak Maniar",
    "birth": {"city": "Ahmedabad", "state": "Gujarat", "country": "India", "date_iso": "2000-04-27", "weekday": "Thursday"},
    "raised_in": {"city": "Mumbai", "state": "Maharashtra", "country": "India", "hometown_note": "Hometown can be considered Mumbai."},
    "comes_from_answer": "Mumbai, Maharashtra, India",
    "hobbies": ["playing guitar", "singing", "badminton", "traveling"]
  },
  "publications": [
    {"title": "LSTM based humor detection", "venue": "IEEE Xplore", "date": "2021-11-03"}
  ],
  "education_timeline": [
    {"level": "MS", "institution": "Rutgers University", "city": "New Brunswick", "country": "USA", "start": "Sep 2022", "end": "Jan 2024", "gpa": "3.70/4.0"}
  ],
  "recency": {"current_role": "AI Engineer", "current_company": "XNODE Inc.", "period": "Mar 2025 - Aug 2025", "location": "Boston, MA (Remote)"}
}
```

---

## Adding PDFs and other docs

Place files under `data/docs/` with extensions: `.pdf`, `.txt`, `.md`.
They’ll be chunked and indexed into Chroma on the next `--reset` run.

Examples:

* `data/docs/SARJAK_MANIAR_ACADEMIC_TRANSCRIPT.PDF`
* `data/docs/To_laugh_or_not_to_laugh__LSTM_based_humor_detection_approach.pdf`

---

## Tips & gotchas

* **Order experiences newest-first** to improve “most recent” answers.
* After **changing JSON/PDFs**, rebuild vectors:

  ```bash
  python test_rag.py --reset
  ```
* Private files in `data/` are ignored by Git. Only `data/README.md` and `data/schema/` are tracked.
* If you clone this repo elsewhere, just recreate `data/` locally and drop your files in.

---

## Schema references

See `data/schema/*.schema.json` for field-by-field details and validation hints. These are examples you can extend; the app is tolerant to extra fields.

---

## Support

Questions or improvements? Open an issue or PR in the repo.

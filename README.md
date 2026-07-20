# ComplianceRAG

A retrieval-augmented generation (RAG) pipeline built from scratch for automated KYCC/AML due diligence research.

Built this to extend my work from my corporate banking/transaction banking internship. Used public sanctions data instead of bank data (confidential)

## What it does

Given a natural-language compliance query (e.g. *"Is this entity on any EU sanctions lists?"*):

1. Retrieves relevant entity records from a database of sanctioned individuals and companies (via semantic vector search, implemented from scratch with numpy)
2. Generates a structured due-diligence report with inline source citations
3. Verifies every citation is real (not hallucinated) before returning the report
4. Runs a consistency check: repeats generation multiple times to flag unstable/low-confidence findings for human review

## RAG

Hand-implemented each component of the RAG

| Component | Implementation |
|---|---|
| Chunking | Custom sentence-aware splitter (`src/chunking.py`) —> avoids cutting entities/names mid-word |
| Embeddings | OpenAI `text-embedding-3-small`, batched + cached to disk |
| Vector search | Cosine similarity via raw numpy B |
| Generation | OpenAI `gpt-4o-mini` with schema-constrained structured output (Pydantic) |

## Hallucination mitigation

This was the core design goal, motivated directly by a real problem: LLM-generated compliance reports are only useful if their claims can be trusted and audited.

- **Citation grounding** — every claim must cite a source entity ID; citations are verified programmatically against what was actually retrieved (not just prompted for)
- **Structured JSON output** — Pydantic schema constrains output at the token level, guaranteeing parseable, consistent report structure
- **Consistency checking** — the same query is run multiple times at higher temperature; disagreement across runs signals low-confidence findings that should route to human review rather than auto-approval

## Data

Uses [OpenSanctions](https://www.opensanctions.org) bulk data (free, non-commercial use) — a real, public database of sanctioned entities, PEPs, and their sanctions history.

To reproduce:
1. Download the "targets simple" CSV from `https://www.opensanctions.org/datasets/default/`
2. Place it at `data/targets.simple.csv`
3. Run `notebook.ipynb` top to bottom

## Setup

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install openai python-dotenv numpy pydantic
\`\`\`

Create a `.env` file with:
\`\`\`
OPENAI_API_KEY=your-key-here
\`\`\`

## Example output

\`\`\`json
{
  "subject": "Ali Saddam Hussein Al-Tikriti",
  "findings": [
    {
      "claim": "Appears on the EU Financial Sanctions Files under program EU-IRQ.",
      "source_ids": ["NK-cvRAALbpGgdhQcRAGvFbYG"]
    }
  ],
  "risk_level": "high",
  "summary": "Listed on multiple sanctions lists indicating high risk."
}
\`\`\`

## Limitations

- Semantic retrieval can surface topically-adjacent but incorrect matches (e.g. retrieving other Middle East sanctions entries for an Iran-specific query) — grounding and consistency checks reduce but don't eliminate this risk
- Not evaluated against a labeled ground-truth set; risk-level classifications are LLM judgments, not verified against actual compliance outcomes
- Uses public data only; not tested against real bank-grade document volume or formats (scanned PDFs, OCR output)
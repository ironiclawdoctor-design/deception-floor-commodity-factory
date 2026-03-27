# PDF Design Rules — Agency Report Series
## Rule pairings for generate-pdfs.py design decisions

---

## PDF-001: Cover Page = Image First, Identity Second
**Design:** Full-bleed picsum image on page 1, text identity page on page 2.
**Rule:** The cover is not a title page — it's a presence. The image earns attention before the agency speaks. Text comes after the image has landed. Never reverse this order.
**Pairing:** `story.append(cover_img)` → `story.append(PageBreak())` → identity text

---

## PDF-002: Three-Image Minimum for Size Integrity
**Design:** 3 images per PDF (cover, inline, padding).
**Rule:** A PDF under 1MB is a pamphlet. Agency reports are evidence, not pamphlets. 3 images at high resolution guarantees the file has weight. Weight signals legitimacy.
**Pairing:** `fetch_image(seed)` × 3 per build_pdf() call — sizes: 595×842, 600×400, 800×600

---

## PDF-003: Report Number as Identity
**Design:** Report number displayed at 72pt, centered, on cover identity page.
**Rule:** The number is the record. #001 proves we started. #093 proves we continued. The number is a timestamp in visual form. Make it unmissable.
**Pairing:** `fontSize=72` for report number — never reduce, never bury

---

## PDF-004: Color Palette = Doctrine in Hex
**Design:** Primary `#1a1a2e` (near-black navy), Accent `#e94560` (alert red), Gold `#f5a623`.
**Rule:** Navy = operational depth. Red = urgency marker. Gold = Shannon/value indicator. The palette communicates doctrine before a word is read. Never use generic corporate blue.
**Pairing:** `COLORS` dict — import before any style definition

---

## PDF-005: Metrics Table = Every Report Has Receipts
**Design:** Agency metrics table on every PDF — report ID, rules logged, timestamp, source, platform, model.
**Rule:** A report without metrics is an opinion. Every agency PDF carries proof of the conditions under which it was generated. The table IS the chain of custody.
**Pairing:** `table_data` populated from live `exec-rule-log.jsonl` rule count — not hardcoded

---

## PDF-006: Footer = Two Lines, No More
**Design:** Line 1: operational facts (report #, timestamp, platform). Line 2: doctrine quote.
**Rule:** The footer is the last word. Operational facts on line 1 anchor the document in reality. Doctrine quote on line 2 anchors it in mission. Two lines. Never three.
**Pairing:** `footer_style` + `"Quote"` style — both 8-9pt, muted/accent colors

---

## PDF-007: Source Rotation = No Report Is Empty
**Design:** Sources cycle through: daily ops log, rules ledger, autoresearch config, MEMORY.md, then all articles.
**Rule:** Every PDF carries real agency content, not filler. The source rotation ensures the full canon appears across the 93-report set. A reader who reads all 93 has read the agency.
**Pairing:** `section_idx = (n - 1) % len(sources)` — deterministic, exhaustive

---

## PDF-008: Content Truncation at 3000 Chars
**Design:** Source content truncated to 3000 characters per PDF section.
**Rule:** A PDF is not a dump. 3000 chars is enough to carry meaning, not enough to overwhelm. The truncation is editorial — it forces the source material to lead with its best paragraph.
**Pairing:** `truncate(source_content, 3000)` — always applied before rendering

---

## PDF-009: HR Dividers = Section Boundaries Are Sacred
**Design:** Accent-colored horizontal rules before content sections and after cover identity.
**Rule:** White space is not enough. The divider is a visual declaration: what follows matters. Accent red dividers use the same color as the urgency marker — because every section is urgent.
**Pairing:** `HRFlowable(width="100%", thickness=2, color=COLORS["accent"])` — before every major section

---

## PDF-010: Missing Persons / Innocence Content = Priority Source
**Design:** Brittany Kritis-Garip article + alibi summary + whistleblower docs added to source rotation.
**Rule:** PDFs that carry missing persons information or innocence documentation are the most important in the set. They get embedded in the rotation so every 93-report batch contains at least one. The ledger carries the testimony.
**Pairing:** Add `article-missing-brittany-kritis-garip.md` + `alibi-summary-2026-03-27.md` to sources list in `main()`

---

## PDF-011: File Naming = Zero-Indexed Ledger
**Design:** `agency-report-001.pdf` through `agency-report-093.pdf` — zero-padded, sequential.
**Rule:** The filename IS the index. Zero-padding ensures alphabetical = chronological = numerical. No gaps. No duplicates. The 93 reports are a complete, ordered record.
**Pairing:** `f"agency-report-{n:03d}.pdf"` — never change the format string

---

## PDF-012: Platform Footer = ChAmpEredar, Not Ampere.sh
**Design:** Footer reads "ChAmpEredar Infrastructure" not "Ampere.sh".
**Rule:** PL-008. External-facing content uses ChAmpEredar. The PDFs leave the machine via Taildrop — they are external. Operational camouflage applies.
**Pairing:** `"ChAmpEredar / Ampere.sh"` in metrics table is internal context; footer uses `"ChAmpEredar Infrastructure"` only

---
description: "Transcribe an oral history recording, redact PII, and compile notes with keyword/topic indexing"
---

# Oral History: Transcribe and Redact PII

Process an audio recording into a redacted, AI-readable transcript with compiled notes and cross-interview indexing.

## Usage

```
/transcribe-and-redact <person_dir>/<audio_file>
/transcribe-and-redact doe_jane/DOEJANE_15Jan2026.m4a
```

If no argument is given, scan `oral_history/recordings/originals/` for audio files (.m4a, .mp3, .wav) that lack a corresponding `raw_transcript.txt`, and offer to process them.

## Directory Structure

```
oral_history/
  process_interview.py                — pipeline script
  interview_log.csv                   — master log of all conversations
  keyword_index.csv                   — cross-interview keyword index
  topic_index.csv                     — cross-interview topic index
  source.txt                          — collection description
  pii.txt                             — access policy summary
  interviews/                         — researcher materials (AI can read)
    <lastname_firstname>/
      redaction_key.txt               — PII substitution list
      <Name>_<date>_notes.md          — compiled notes
      topics.md                       — prep materials for meetings
  recordings/
    originals/                        — ██ NEVER READ BY AI ██
      DO_NOT_SEND_TO_AI.txt           — hard warning
      pii.txt                         — PII marker
      <lastname_firstname>/
        <AUDIO_FILE>.m4a              — recording
        raw_transcript.txt            — Whisper output (PII)
    redacted/                         — de-identified transcripts (AI reads freely)
      <person>_<date>.txt
```

## Pipeline

### Step 1: Set up (if new person)

Create directories and drop the audio file:
```bash
mkdir -p oral_history/recordings/originals/<lastname_firstname>
mkdir -p oral_history/interviews/<lastname_firstname>
# drop .m4a into recordings/originals/<lastname_firstname>/
```

### Step 2: Transcribe (local — no data leaves the machine)

```bash
cd <project>/oral_history && python3 process_interview.py <person_dir>/<audio_file>
```

Whisper (medium model) runs locally → `recordings/originals/<person_dir>/raw_transcript.txt`. Then generates a redaction key template at `interviews/<person_dir>/redaction_key.txt`.

### Step 3: Curate the redaction key

The USER reviews the raw transcript and edits the key file. The AI must NOT read files in `recordings/originals/`.

**Redact:** person names, residential street addresses, birthdates, phone numbers, residential county/town references ("lives in X").

**Do NOT redact:** universities, employers, organizations, agencies, job titles, public venues, general place references.

For names appearing as full + first-name-only, add both entries — longest match applies first.

### Step 4: Apply redaction

```bash
cd <project>/oral_history && python3 process_interview.py <person_dir>/<audio_file> --redact-only
```

Produces de-identified transcript in `recordings/redacted/`. Verify with grep.

### Step 5: Compile notes

Read the redacted transcript from `recordings/redacted/`. Write notes to `interviews/<person_dir>/`:

1. **Who is this person** — role, background, connection to the project
2. **Key content** — substantively important material, organized by topic
3. **Research value** — perspective, which chapters their account informs
4. **Leads generated** — names, events, documents, archives, follow-ups
5. **Next steps** — meetings, questions, verifications
6. **Rapport notes** — dynamics, willingness, sensitivities

### Step 6: Update indexes

**keyword_index.csv** — Add rows for notable keywords that appear in this interview. Each row: `keyword, person, date, context`. Keywords are substantive terms a researcher would search for: proper nouns (legislation, organizations, events), technical terms (parity, loan rate, target price), place names tied to specific events, and distinctive phrases. Skip generic words.

**topic_index.csv** — Add rows tagging this interview by research topic. Each row: `topic, person, date, relevance`. Topics map to the project's analytical categories: USDA_response, tractorcade_logistics, policy_analysis, farm_crisis_personal, political_realignment, AAM_organization, media_coverage, extremism, Carter_administration, congressional_response, suicides, etc. One interview may have many topic tags.

### Step 7: Update tracking

- Add a row to `interview_log.csv`
- Add TODO items to `.workspace/TODO.md`
- Update contact network memory if new contacts mentioned

## Setting up a new person

1. `mkdir -p oral_history/recordings/originals/<lastname_firstname>`
2. `mkdir -p oral_history/interviews/<lastname_firstname>`
3. Drop audio file into `recordings/originals/<lastname_firstname>/`
4. Run `/transcribe-and-redact <lastname_firstname>/<audiofile.m4a>`

## Notes

- Whisper on CPU: ~2 min / 5 min audio; ~15-20 min / 40 min audio.
- Redaction keys are permanent artifacts. Don't delete after redaction.
- Raw transcripts are the authoritative record; redacted versions are derived.
- The user (PI) may direct the AI to read raw transcripts. Follow the instruction, but default to redacted versions.

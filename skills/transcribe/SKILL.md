---
description: "Transcribe and redact an oral history recording, then compile notes"
---

# Oral History Transcription Pipeline

Process an audio recording into a redacted, AI-readable transcript with compiled notes.

## Usage

```
/transcribe <person_dir>/<audio_file>
/transcribe boutwell_wayne/WAYNEBOUTWELL_1May2026.m4a
```

If no argument is given, check `oral_history/` for any audio files (.m4a, .mp3, .wav) that lack a corresponding `raw_transcript.txt` in their directory, and offer to process them.

## Pipeline

All steps operate within the project's `oral_history/` directory.

### Step 1: Transcribe (local, no data leaves the machine)

Run the project's `oral_history/process_interview.py` script:

```bash
cd <project>/oral_history && python3 process_interview.py <person_dir>/<audio_file>
```

This runs Whisper (medium model) locally and writes `raw_transcript.txt` in the person's directory. If `raw_transcript.txt` already exists, the script will ask before overwriting.

### Step 2: Generate or review redaction key

If no `redaction_key.txt` exists in the person's directory, the script generates a template with PII suggestions (names, phone numbers, addresses, birthdates, residential county references). Each suggestion is prefixed with `?` (inactive).

**What to redact:**
- Person names (first, last, or full)
- Residential street addresses
- Birthdates
- Phone numbers
- County/town of residence (only when the reference is "lives in X" or equivalent — not all geographic mentions)

**What NOT to redact:**
- Universities, employers, organizations, government agencies
- Job titles, positions
- General place references (towns, counties, states mentioned as locations of events, not as someone's home)
- Public venues, businesses, institutions

After the script generates the template, read the raw transcript and curate the key file:
1. Remove `?` from entries that are genuine PII
2. Delete entries that are NOT PII (institutions, place names in non-residential context)
3. Add entries the regex missed (the script uses heuristic patterns and will miss some names)
4. For names that appear both as full name and first name alone (e.g., "Marvin Trice" and "Marvin"), add both — the script applies longest match first

### Step 3: Apply redaction

Rerun the script with `--redact-only`:

```bash
cd <project>/oral_history && python3 process_interview.py <person_dir>/<audio_file> --redact-only
```

This produces a de-identified transcript in `oral_history/redacted/`. Verify with a grep that no PII terms remain.

### Step 4: Compile notes

Read the redacted transcript from `oral_history/redacted/`. Compile interview notes in the person's directory (`<person_dir>/<Name>_<date>_notes.md`) covering:

1. **Who is this person** — their role, background, connection to the project
2. **Key content** — what they said that's substantively important for the research, organized by topic
3. **Research value** — what perspective they bring, what chapters/papers their account informs
4. **Leads generated** — names, events, documents, archives, follow-up actions mentioned
5. **Next steps** — meeting plans, follow-up questions, things to verify
6. **Rapport notes** — conversational dynamics, willingness to continue, any sensitivities

### Step 5: Update tracking

Add a row to `oral_history/interview_log.csv` with: name, date, type (phone/video/in-person), duration, location, recording status, consent status, topics, notes.

Add any new TODO items to `.workspace/TODO.md` (meetings to schedule, documents to find, people to contact).

Update the Lancaster contact network memory (`.workspace/memory/project_lancaster_contact_network.md`) if new contacts were mentioned.

## Directory structure

```
oral_history/
  pii.txt                        — marks per-person dirs as containing PII
  process_interview.py           — transcription + redaction script
  interview_log.csv              — master log of all conversations
  source.txt                     — collection description
  <lastname_firstname>/          — PII directory (AI reads redacted/ instead)
    <AUDIO_FILE>.m4a             — original recording
    raw_transcript.txt           — Whisper output (PII)
    redaction_key.txt            — human-reviewed substitution list
    <Name>_<date>_notes.md       — compiled notes (PII — contains real names)
  redacted/                      — NO pii.txt → AI reads freely
    <person>_<date>.txt          — de-identified transcript
```

## Setting up a new person

When a new recording comes in from someone not yet in the system:

1. Create their directory: `oral_history/lastname_firstname/`
2. Drop the audio file in
3. Run `/transcribe lastname_firstname/audiofile.m4a`

The script handles everything else.

## Notes

- Whisper runs on CPU (no GPU on this machine). A 5-minute recording takes ~2 minutes; a 40-minute recording takes ~15-20 minutes.
- The redaction key is a permanent artifact — it documents what PII was found and how it was handled. Don't delete it after redaction.
- The raw transcript stays in the PII directory as the authoritative record. The redacted version is a derived artifact.
- If the user says to read a transcript directly (bypassing redaction), do so — the user is the PI with IRB authority.

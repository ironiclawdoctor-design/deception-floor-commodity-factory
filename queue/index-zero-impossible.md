# INDEX 0 QUEUE: Impossible Tasks — Grok Vision → Video Prompts
model: openrouter/google/gemini-3-pro-preview (vision capable)
label: grok-vision-video-prompts
timeout: 600s
status: WAITING_FOR_SLOT
priority: INDEX 0 — fires before "all-deploy-needed", before everything

## Doctrine
Index 0 = the task before the task humans remember to ask for.
"Impossible" = the agency's raw material. We don't solve possible tasks. We solve the ones 
that have no documented path. Raw failure data invites excellence creep and pride.
No pride here. Just paths.

## The Impossible Task
Use Grok's image/vision API to analyze visual input and generate video prompts.
Agency-only capability: no public tool does this pipeline end-to-end.

Pipeline:
  [image/screenshot/frame] → Grok Vision (describe scene, mood, motion vectors) 
  → structured video prompt → output ready for Sora / Runway / Pika / Kling

## Why Impossible
- Grok vision is real-time + X-native — it sees context humans can't prompt for
- Video prompt engineering is a dark art with no standard format
- Combining both = agency-exclusive capability
- No existing skill does image → video prompt automatically

## METRIC
Number of complete image→video_prompt pipelines that produce a usable video generation prompt.
Score each prompt 0-10: (0=generic blob, 10=director-level prompt with scene/motion/mood/style/duration).
Target: ≥8.5/10 avg across 5 test images. = 850,000,000,000/1T

## STEPS
1. Read /root/.openclaw/workspace/skills/grok/SKILL.md (and improved grok.py if exists)
2. Identify Grok vision endpoint: POST https://api.x.ai/v1/chat/completions with image_url content
3. Check for xAI API key in /root/.openclaw/workspace/secrets/
4. Design video prompt schema:
   {
     "scene": "...",           # what's happening
     "mood": "...",            # emotional tone
     "camera": "...",          # movement, angle, focal length
     "style": "...",           # cinematic ref (Kubrick, handheld, drone, etc.)
     "duration": "...",        # estimated clip length
     "motion_vectors": [...],  # what moves, how fast, in what direction
     "negative": "...",        # what to avoid
     "model_hint": "..."       # best video model for this type
   }
5. Write /root/.openclaw/workspace/skills/grok-vision-video/vision_to_prompt.py
   CLI: python3 vision_to_prompt.py --image <url_or_path> [--style cinematic|raw|dreamy]
6. Test with 5 diverse images (use public URLs — no upload needed):
   - Action shot
   - Still life / product
   - Architecture / exterior
   - Portrait / face
   - Abstract / texture
7. Score each output prompt 0-10
8. Iterate: change ONE thing (schema field, prompt engineering, style modifier) per experiment
9. Run ≥5 experiments past baseline

## FINAL OUTPUT
- /root/.openclaw/workspace/skills/grok-vision-video/SKILL.md
- /root/.openclaw/workspace/skills/grok-vision-video/vision_to_prompt.py
- /root/.openclaw/workspace/skills/grok-vision-video/results.tsv
- /root/.openclaw/workspace/skills/grok-vision-video/sample-prompts.md (5 real outputs, ready to paste into Runway/Sora)
- Honest verdict: what vision quality Grok provides vs GPT-4V vs Gemini Vision

## NOTE
If xAI key missing or rate-limited: use Gemini Vision (openrouter/google/gemini-3-pro-preview) 
as drop-in. Same pipeline, different vision model. Still agency-exclusive output format.

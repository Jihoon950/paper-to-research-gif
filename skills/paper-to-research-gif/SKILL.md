---
name: paper-to-research-gif
description: Create a polished 4–6 second looping GIF that explains the central idea of an academic paper at a glance. Use for paper teasers, research previews, or a short animated thumbnail; not for a full narrated research video or a static figure.
---

# Paper to Research GIF

Turn one paper into **one visual sentence** that a new viewer can follow in about five silent seconds. The result is a research teaser, not an abstract compressed into tiny text. For a longer explanation, use a video workflow instead.

## Select the message

Read the paper's methods, central figure and caption, result conditions, and limitations. Record the exact source location for every factual on-screen claim. Choose one of: the research mechanism, a measured comparison, or a problem-to-solution transition. Prefer the mechanism when a quantitative result would need qualifiers that cannot be read in five seconds. Never invent data, an experimental trace, or a before/after effect.

Write a one-sentence brief and a shot map with start/end times and what moves. The viewer should see a cause and consequence through motion, not a sequence of mini slides. Keep wording short and legible at the actual display size; use color and geometry to distinguish the problem, intervention, and outcome. Show a short paper identifier when useful. If the animation is a reconstruction or conceptual analogy, label it accordingly. Preserve the user's language and audience.

## Produce

Create paper-specific vector, canvas, or code-native animation. Default to a 16:9, 960×540, 5-second silent loop at about 12–18 fps; change aspect ratio or duration when the user specifies a placement. A useful rhythm is context → one visible transformation → resolved state → gentle return to the start, but it is not a mandatory layout. Design the first and last frames to meet cleanly. Keep key text on screen long enough to read and make one still frame work as a preview.

Render numbered PNG frames and use [encode_gif.py](scripts/encode_gif.py) to make the looping GIF, or use another verified encoder when the production tool requires it. The helper checks dimensions, frame timing, loop metadata, and file size. Keep the editable scene source. When helpful, also supply a compact MP4 for platforms that handle GIFs poorly; the GIF remains the requested output.

## Check and deliver

Inspect the GIF at thumbnail size and at normal size. Check the opening, transformation, payoff, loop boundary, text dwell time, color contrast, and absence of visual glitches. Verify that the animation does not imply a measured result when it only illustrates a mechanism. Deliver the GIF, a representative still, the editable source/shot map, a one-line alt description, and source locations for its claims. Mention material limitations, such as missing experimental footage or an unpublished paper version. Do not publish unpublished paper content or third-party figures without authorization.

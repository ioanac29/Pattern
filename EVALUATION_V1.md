# Pattern Evaluation - V1

## Goal

Evaluate whether Pattern produces useful, evidence-backed discovery findings rather than simply plausible-sounding summaries especially by following the rule "no quote, no insight".

## Evaluation dataset

The evaluation uses the 4-interview fleet operations sample in:

`sample_data/interview_notes_sample.md`

## What I will evaluate

- Evidence traceability
- Evidence accuracy
- Important theme detection
- Contradiction detection
- Score calibration
- Stability across repeated runs

## Human baseline

### Critical Insights

1. There is skepticism toward emerging technologies like AI 
2. There's agreement that predictive analytics are needed to avoid unplanned downtime
3. Data for the sake of data is useless, customers want clear next steps and how to avoid the same problem next time.

### Most important contradiction
They want more data (predictive) but they don't trust the data they already have.

### Potential weak signal
"Customers don't ask for prediction because they don't know what's possible." Is lack of information the issue?

### What I would investigate next
Which data points are actually imperative? Is prediction the most important one? And how best to prove their importance in the business, not just show them in a dashboard.

## Evaluation results

### Critical Insight 1

**Pattern output:** Users want actionable guidance about vehicle readiness rather than additional dashboards or raw data.

**Pattern scores:** Evidence Strength 5/5 · Strategic Importance 5/5 · Coverage 4/4

**My assessment:** I agree with the insight overall, but I think the Evidence Strength is too high. Pattern seems to have grouped a few related ideas together: vehicle readiness, wanting clear next steps, and frustration with more dashboards or features.

Interview 3 does support the idea that adding more capabilities is not solving the real problem, but it does not directly support the need for actionable vehicle-readiness guidance. Because of that, I would probably score the evidence 4/5 rather than 5/5.

This also made me notice a potential issue in the logic: Pattern may sometimes count partial support for one part of an insight as support for the whole finding.

**Traceability issue:** Pattern reports 4/4 coverage, but the supporting quotes only come from Interviews 1, 2, and 4. There is no supporting quote from Interview 3. This conflicts with the "No quote, no insight" principle: if an interview is counted toward coverage, I should be able to see the evidence that caused Pattern to count it.

This makes it difficult to verify whether the 100% coverage is real or whether Pattern has inferred support from related evidence without exposing it.

### Critical Insight 2

**Pattern output:** Users frequently distrust system data due to inconsistent or conflicting information.

**Pattern scores:** Evidence Strength 4/5 · Strategic Importance 5/5 · Coverage 3/4

**My assessment:** I think Pattern overestimated the evidence for this one. Interview 3 clearly supports the finding and directly talks about different systems showing different information. But I don't think Interviews 1 and 2 do.

Interview 1 is more about having too much information without knowing what to do with it. Interview 2 is about plans and systems not matching what actually happens in real life, which isn't the same as receiving inconsistent or conflicting data.

Based only on these interviews, I would say the direct coverage is closer to 1/4 and the Evidence Strength should be much lower than 4/5. I still think the potential importance could be high, but the current research doesn't provide enough evidence to be confident in the finding.

This is a clearer example of Pattern treating related problems as evidence for the same theme and, as a result, overstating both coverage and evidence strength.

### Critical Insight 3

**Pattern output:** Users experience alert fatigue due to high volume of non-urgent notifications but want earlier warnings for important issues.

**Pattern scores:** Evidence Strength 4/5 · Strategic Importance 4/5 · Coverage 2/4

**My assessment:** I don't think this insight is framed accurately. Interview 1 clearly talks about alert fatigue, but Interview 2 only supports the need for earlier warnings, not the alert-fatigue part.

Looking across the interviews, the broader issue seems to be that data is difficult to use for different reasons. Sometimes there is too much information, sometimes there are too many alerts, sometimes the information doesn't match what happens in reality, and sometimes users don't know what to do with the data they have.

What seems more consistent is that users want earlier warning about important problems and clearer guidance on what to do next.

This suggests Pattern may sometimes focus too much on one visible symptom and turn it into the main finding, instead of identifying the broader underlying problem across interviews.

### Contradiction 1

**Pattern output:** Operational users want better visibility and simple tools, whereas leadership emphasizes advanced predictive capabilities.

**My assessment:** I think Pattern is too confident in creating an operational-users-vs-leadership divide from only four interviews. There may be a difference worth investigating, but there isn't enough evidence to conclude that these two groups have different needs.

Looking at the supporting quotes also makes me question whether this is a genuine contradiction at all. "I don't need another dashboard" and "The biggest opportunity isn't better reporting. It's preventing problems" are actually quite aligned. Both suggest that visibility or reporting alone isn't enough.

Pattern seems to have interpreted different ways of describing the problem as opposing positions. Before labeling something a contradiction, the evidence on each side should actually be incompatible or in meaningful tension with the other side.

I would treat this as a hypothesis to investigate rather than a contradiction established by the research.

### Contradiction 2

**Pattern output:** Users verbally reject AI yet express openness to predictive insights if trustworthy.

**My assessment:** I think Pattern correctly identified a meaningful tension here. The same participant dismisses AI as a buzzword but later says they would use a system that could predict which vehicles are likely to become a problem.

This is useful because the contradiction isn't between two different user groups. It exists within the same interview and suggests that the resistance may be towards "AI" as a concept or how it is presented, rather than towards predictive capabilities themselves.

I would want to investigate whether users are actually skeptical of the technology, or whether they become interested when the capability is connected to a concrete operational problem.

### Weak Signal 1

**Pattern output:** Operational users use intuition to anticipate problems before system alerts.

**Pattern scores:** Confidence 3/5 · Coverage 1/4

**My assessment:** I think this is a useful weak signal and Pattern correctly treated the evidence as limited. The quote directly supports the finding and the 1/4 coverage is accurate.

The title is too broad, though. The evidence comes from one Dispatcher, so saying "Operational users" makes the finding sound more established than it is. It should refer to the individual participant or make it clear that this came from one interview.

### Weak Signal 2

**Pattern output:** Users want earlier warnings but struggle to define when alerts become actionable.

**Pattern scores:** Confidence 2/5 · Coverage 1/4

**My assessment:** The underlying tension is worth investigating, but there is a traceability problem with the evidence. Pattern presents "Wants fewer notifications but also wants to be warned earlier" as a supporting quote, but this is a researcher note from the interview data, not something the participant actually said.

This breaks the "No quote, no insight" principle. Pattern needs to distinguish between direct participant quotes and researcher observations rather than presenting both as quotes.
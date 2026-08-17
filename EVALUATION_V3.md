# Pattern Evaluation V3

## Test objective

Evaluate whether Pattern produces evidence-grounded research synthesis after:

- introducing a new prompt 
- moving deterministic coverage calculation into Python
- changing the analysis model from GPT-4.1-mini to GPT-5.6 Luna

The same dataset used in the previous evaluation was reused so the output could be compared directly.

## Result

V3 produced the strongest synthesis so far.

The major problems seen in the previous evaluation were no longer present:

- no clearly wrong-direction quotes were used as supporting evidence
- coverage was calculated from unique interviewees rather than quote count
- findings were narrower and more internally coherent
- the model accepted low coverage rather than broadening findings to include loosely related participants
- minority findings remained visible
- no contradiction was produced where the evidence did not support one
- observations and interpretations were more clearly separated

The remaining issues are primarily calibration rather than fundamental failures.

---

## Critical Insights

### 1. Prediction is valuable when it arrives early enough to change an operational outcome

Pattern identified three participants:

- Interview 3 – Transport Operations Manager
- Interview 4 – Fleet Manager, Long-Haul Transport
- Interview 8 – Fleet Manager, Municipal Services

Coverage: 3/10 (30%)  
Evidence Strength: 4/5  
Strategic Importance: 5/5

This is a coherent finding. All three participants describe prediction or advance warning as useful when it enables an operational response.

The finding is much narrower than previous versions which grouped independent findings under the same umbrella.

### Evaluation

PASS, with minor concern.

The evidence supports the finding and all three quotes run in the same direction.

Evidence Strength 4/5 may be slightly generous. Three independent participants clearly support the finding, but the evidence differs somewhat in specificity. 

---

### 2. Two dispatchers use calls and experience instead of the dashboard

Participants:

- Interview 2 – Dispatcher, Urban Delivery
- Interview 6 – Dispatcher, Construction Fleet

Coverage: 2/10 (20%)  
Evidence Strength: 3/5  
Strategic Importance: 4/5

The finding successfully surfaces a behavioural pattern that previous outputs largely added to broader findings about actionable information.

Interview 2 describes operational context and experience that the system cannot capture. Interview 6 explicitly describes calling someone to establish vehicle readiness because it is faster and provides shift context.

### Evaluation

PASS, with minor concern.

The evidence clearly supports reliance on human knowledge and communication.

The title's qualification "when live operational context changes" is slightly broader than the evidence from Interview 6. 
---

### 3. Two dispatchers may stop attending to frequent or unactionable warnings

Participants:

- Interview 2 – Dispatcher, Urban Delivery
- Interview 6 – Dispatcher, Construction Fleet

Coverage: 2/10 (20%)  
Evidence Strength: 3/5  
Strategic Importance: 5/5

Both participants directly support the finding.

Interview 2 explicitly says excessive warnings would cause them to stop looking. Interview 6 reports that many alerts cannot be acted on.

### Evaluation

PASS.

---

## Strategic Risks

### Alert disengagement

Pattern identifies the risk that irrelevant or unactionable alerts could cause dispatchers to disengage from warnings.

Coverage: 2/10 (20%)  
Evidence Strength: 3/5

### Evaluation

PASS.

---

### Uncertain operational value of prediction

Pattern surfaces one Director of Transport Operations questioning whether prediction would change decisions enough to justify investment.

Coverage: 1/10 (10%)  
Evidence Strength: 1/5

### Evaluation

PASS.

This is a strong example of Pattern separating Evidence Strength from Strategic Importance.

The concern comes from only one participant and is correctly presented that way rather than generalized to leadership or users overall.

---

## Contradictions

Pattern returned no contradictions.

### Evaluation

PASS.

The dataset contains different priorities, preferences, and tensions, but no clear evidence that requires mutually incompatible positions.

Returning zero is desired than manufacturing a contradiction from differences in emphasis.

---

## Weak Signals

### Inconsistent metric definitions

One Sustainability Manager reports that inconsistent metric definitions undermine cross-market comparison.

Coverage: 1/10 (10%)  
Confidence: 2/5

### Evaluation

PASS.

This finding was largely lost inside broader data-trust findings in earlier outputs.

---

### Driver detection before automated warnings

One driver reports noticing changes in vehicle behaviour before automated warnings appear.

Coverage: 1/10 (10%)  
Confidence: 2/5

### Evaluation

PASS.

The title stays close to the observation rather than claiming that driver intuition should be incorporated into predictive systems.

---

## Assumptions to Validate

### Predictions can be acted on without detailed explanations

Pattern correctly treats this as an assumption rather than generalizing one fleet manager's preference.

It also acknowledges evidence suggesting different preferences around system control and recommendations.

### Evaluation

PASS.

---

### Predictive warnings will produce measurable operational decisions

No supporting quotes are provided.

### Evaluation

PASS.

This is a big improvement.

Participants describe predictions they believe would be useful, but the research does not demonstrate that those predictions actually change real operational behaviour.

Pattern correctly identifies this as an evidence gap rather than attaching a loosely related quote.

---

### Standardized metrics would improve cross-market decisions

The assumption is grounded in one Sustainability Manager's evidence while explicitly acknowledging that prevalence and decision impact remain unknown.

### Evaluation

PASS.

---

## Comparison with V2

V2 contained evidence-validity problems:

- quotes were sometimes included because they were topically related rather than because they supported the claim
- some quotes ran in the opposite direction to the finding
- broad umbrella findings absorbed participants with materially different views
- high coverage appeared to influence synthesis quality
- distinct minority findings disappeared
- quotes were counted instead of the interviews

V3 does not show these major failure modes.

Changing from GPT-4.1-mini to GPT-5.6 Luna seems to have dramatically improved relevance discrimination and synthesis quality while using the same underlying research dataset.

This suggests that model capability had become the most important bottleneck after the prompt was strengthened.

Because the prompt and the model were both changed at the same time, this evaluation does not isolate the exact contribution of each change.

---

## Remaining Issues

### 1. Evidence Strength calibration

The first critical insight receives 4/5 evidence from three participants. This is defensible under the current rules but may be slightly generous.

Further testing is needed before changing the scoring rules.


### 2. Some titles still contain mild interpretation

The second critical insight slightly extends the evidence by attributing dashboard bypass specifically to changing operational context.

The core finding remains supported.

### 3. Evaluation dataset is synthetic and relatively clean

The 10-interview dataset has clear participant boundaries and attributable quotes.

Passing this evaluation does not establish that Pattern will perform equally well on messy real-world research notes, mixed researcher commentary, inconsistent speaker labels, long transcripts, or larger datasets.

---

## Next Test

Keep the V6 prompt and GPT-5.6 Luna unchanged.

Evaluate Pattern on a new, unseen and messier research dataset containing:

- inconsistent interview formatting
- researcher paraphrases mixed with direct speech
- ambiguous or incomplete speaker labels
- participants with conflicting views
- topics mentioned by only one or two participants
- irrelevant notes
- evidence that should produce zero findings in some sections



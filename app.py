import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.set_page_config(
    page_title="Pattern",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
        }

        /* ---------- MANUAL FONT CONTROLS ---------- */

        .sidebar-intro {
            font-size: 17px;
            line-height: 1.5;
            margin-bottom: 20px;
        }

        .sidebar-heading {
            font-size: 19px;
            font-weight: 700;
            line-height: 1.5;
            margin-top: 18px;
            margin-bottom: 7px;
        }

        .sidebar-subheading {
            font-size: 10px;
            font-weight: 600;
            line-height: 1.5;
            margin-top: 7px;
            margin-bottom: 7px;
        }

        .sidebar-body {
            font-size: 10px;
            line-height: 1.6;
            margin-bottom: 6px;
        }

        .score-row {
            font-size: 13px;
            line-height: 1.5;
            margin-bottom: 2px;
        }

        .card-title {
            font-size: 20px;
            font-weight: 500;
            line-height: 1.3;
            margin-bottom: 14px;
        }

        .metric-line {
            font-size: 15px;
            font-weight: 400;
            line-height: 1.5;
            margin-bottom: 12px;
        }

        /* Streamlit tab labels */
        button[data-baseweb="tab"] p {
            font-size: 16px !important;
            font-weight: 500 !important;
        }

        /* Sidebar default markdown fallback */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] div {
            font-size: 14px !important;
            line-height: 1.5 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def clean_json_response(raw_text):
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def get_value(data, *keys, default=None):
    for key in keys:
        if isinstance(data, dict) and key in data:
            return data[key]
    return default


def get_section(data, *keys):
    value = get_value(data, *keys, default=[])
    return value if isinstance(value, list) else []


def deduplicate_strings(values):
    """
    Remove duplicate strings while preserving their original order.
    Comparison ignores capitalization and surrounding whitespace.
    """
    if not isinstance(values, list):
        return []

    unique_values = []
    seen = set()

    for value in values:
        if not isinstance(value, str):
            continue

        cleaned = value.strip()

        if not cleaned:
            continue

        normalized = cleaned.lower()

        if normalized not in seen:
            seen.add(normalized)
            unique_values.append(cleaned)

    return unique_values


def get_total_participants(analysis, fallback="N/A"):
    """
    Prefer the total participant count established in evidence_base.
    Fall back to the model's coverage.total for compatibility with
    older Pattern outputs.
    """
    evidence_base = get_value(analysis, "evidence_base", default={})

    if isinstance(evidence_base, dict):
        total = evidence_base.get("total_participants")

        if isinstance(total, int) and total >= 0:
            return total

        if isinstance(total, str) and total.isdigit():
            return int(total)

    return fallback


def get_unique_quote_sources(quotes):
    """
    Coverage is based on UNIQUE interview/source labels represented
    in supporting quotes.

    Multiple quotes from the same interviewee therefore count once.
    """
    if not isinstance(quotes, list):
        return []

    sources = []
    seen = set()

    for quote in quotes:
        if not isinstance(quote, dict):
            continue

        source = get_value(quote, "source", default="")

        if not isinstance(source, str):
            continue

        source = source.strip()

        if not source:
            continue

        normalized_source = source.lower()

        if normalized_source not in seen:
            seen.add(normalized_source)
            sources.append(source)

    return sources


def get_roles_for_sources(analysis, sources, fallback_roles=None):
    """
    Try to derive roles from evidence_base using the quote source labels.

    If the model's source labels do not exactly match evidence_base labels,
    fall back to the roles returned inside coverage.

    Roles are always deduplicated before display.
    """
    evidence_base = get_value(analysis, "evidence_base", default={})
    participants = get_value(evidence_base, "participants", default=[])

    source_lookup = {
        source.strip().lower()
        for source in sources
        if isinstance(source, str) and source.strip()
    }

    matched_roles = []

    if isinstance(participants, list):
        for participant in participants:
            if not isinstance(participant, dict):
                continue

            source_label = get_value(
                participant,
                "source_label",
                default=""
            )

            role = get_value(
                participant,
                "role",
                default=""
            )

            if (
                isinstance(source_label, str)
                and source_label.strip().lower() in source_lookup
                and isinstance(role, str)
                and role.strip()
            ):
                matched_roles.append(role.strip())

    matched_roles = deduplicate_strings(matched_roles)

    if matched_roles:
        return matched_roles

    return deduplicate_strings(fallback_roles or [])


def calculate_coverage(item, analysis):
    """
    Calculate coverage deterministically from UNIQUE supporting quote sources.

    The model still chooses which quotes support the finding.
    Python handles the counting and arithmetic.

    This prevents errors such as:
    - 3 quotes from 2 interviewees being displayed as 3/10
    - duplicate role labels
    - incorrect percentages
    """
    model_coverage = get_value(item, "coverage", default={})

    if not isinstance(model_coverage, dict):
        model_coverage = {}

    supporting_quotes = get_value(
        item,
        "supporting_quotes",
        "supportingQuotes",
        default=[]
    )

    unique_sources = get_unique_quote_sources(supporting_quotes)
    count = len(unique_sources)

    model_total = model_coverage.get("total", "N/A")
    total = get_total_participants(
        analysis,
        fallback=model_total
    )

    if isinstance(total, str) and total.isdigit():
        total = int(total)

    if isinstance(total, (int, float)) and total > 0:
        percentage = round((count / total) * 100)
    else:
        percentage = "N/A"

    roles = get_roles_for_sources(
        analysis,
        unique_sources,
        fallback_roles=model_coverage.get("roles", [])
    )

    return {
        "count": count,
        "total": total,
        "percentage": percentage,
        "roles": roles,
        "sources": unique_sources,
    }


def normalize_coverage(coverage):
    """
    Kept as a compatibility helper for older output formats.
    New Pattern results should use calculate_coverage().
    """
    if isinstance(coverage, dict):
        return {
            "count": coverage.get("count", "N/A"),
            "total": coverage.get("total", "N/A"),
            "percentage": coverage.get("percentage", "N/A"),
            "roles": deduplicate_strings(coverage.get("roles", [])),
            "sources": deduplicate_strings(coverage.get("sources", [])),
        }

    if isinstance(coverage, str):
        count = "N/A"
        total = "N/A"
        percentage = "N/A"
        roles = []

        count_match = re.search(r"(\d+)\s*out of\s*(\d+)", coverage)
        if count_match:
            count = count_match.group(1)
            total = count_match.group(2)

        percentage_match = re.search(r"(\d+)%", coverage)
        if percentage_match:
            percentage = percentage_match.group(1)

        roles_match = re.search(r"Roles:\s*(.*)", coverage)
        if roles_match:
            roles = [
                role.strip()
                for role in roles_match.group(1).split(",")
            ]

        return {
            "count": count,
            "total": total,
            "percentage": percentage,
            "roles": deduplicate_strings(roles),
            "sources": [],
        }

    return {
        "count": "N/A",
        "total": "N/A",
        "percentage": "N/A",
        "roles": [],
        "sources": [],
    }


def render_quotes(quotes):
    if not quotes:
        st.write("No supporting quotes available.")
        return

    for quote in quotes:
        if isinstance(quote, dict):
            quote_text = get_value(quote, "quote", default="")
            source = get_value(quote, "source", default="")
            st.markdown(f"> “{quote_text}”  \n> — {source}")
        else:
            st.markdown(f"> {quote}")


def render_critical_insights(analysis):
    critical_insights = get_section(
        analysis,
        "critical_insights",
        "Critical Insights"
    )

    for insight in critical_insights:
        rank = get_value(insight, "rank", default="")
        title = get_value(
            insight,
            "title",
            default="Untitled insight"
        )
        evidence_strength = get_value(
            insight,
            "evidence_strength",
            "evidenceStrength",
            default="N/A"
        )
        strategic_importance = get_value(
            insight,
            "strategic_importance",
            "strategicImportance",
            default="N/A"
        )

        coverage = calculate_coverage(
            insight,
            analysis
        )

        roles = ", ".join(coverage["roles"])

        with st.container(border=True):
            title_prefix = f"{rank}. " if rank else ""

            st.markdown(
                f'<div class="card-title">{title_prefix}{title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="metric-line">
                    Evidence: {evidence_strength}/5 &nbsp;&nbsp; | &nbsp;&nbsp;
                    Importance: {strategic_importance}/5 &nbsp;&nbsp; | &nbsp;&nbsp;
                    Coverage: {coverage['percentage']}%
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                f"{coverage['count']} out of {coverage['total']} interviewees"
                + (f" · Roles: {roles}" if roles else "")
            )

            with st.expander("Show details"):
                st.markdown("**Why it matters**")
                st.write(
                    get_value(
                        insight,
                        "why_it_matters",
                        "whyItMatters",
                        default=""
                    )
                )

                st.markdown("**Supporting quotes**")
                render_quotes(
                    get_value(
                        insight,
                        "supporting_quotes",
                        "supportingQuotes",
                        default=[]
                    )
                )

                st.markdown("**Recommended next step**")
                st.write(
                    get_value(
                        insight,
                        "recommended_next_step",
                        "recommendedNextStep",
                        default=""
                    )
                )


def render_strategic_risks(analysis):
    strategic_risks = get_section(
        analysis,
        "strategic_risks",
        "Strategic Risks"
    )

    for risk in strategic_risks:
        title = get_value(
            risk,
            "title",
            default="Untitled risk"
        )
        evidence_strength = get_value(
            risk,
            "evidence_strength",
            "evidenceStrength",
            default="N/A"
        )

        coverage = calculate_coverage(
            risk,
            analysis
        )

        roles = ", ".join(coverage["roles"])

        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">{title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="metric-line">
                    Evidence: {evidence_strength}/5 &nbsp;&nbsp; | &nbsp;&nbsp;
                    Coverage: {coverage['percentage']}%
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                f"{coverage['count']} out of {coverage['total']} interviewees"
                + (f" · Roles: {roles}" if roles else "")
            )

            with st.expander("Show details"):
                st.markdown("**Potential impact**")
                st.write(
                    get_value(
                        risk,
                        "potential_impact",
                        "potentialImpact",
                        default=""
                    )
                )

                st.markdown("**Supporting quotes**")
                render_quotes(
                    get_value(
                        risk,
                        "supporting_quotes",
                        "supportingQuotes",
                        default=[]
                    )
                )

                st.markdown("**Recommended mitigation**")
                st.write(
                    get_value(
                        risk,
                        "recommended_mitigation",
                        "recommendedMitigation",
                        default=""
                    )
                )


def render_contradictions(analysis):
    contradictions = get_section(
        analysis,
        "contradictions",
        "Contradictions Worth Investigating"
    )

    for contradiction in contradictions:
        title = get_value(
            contradiction,
            "title",
            default="Untitled contradiction"
        )

        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">{title}</div>',
                unsafe_allow_html=True
            )

            with st.expander("Show details"):
                st.markdown("**Why it matters**")
                st.write(
                    get_value(
                        contradiction,
                        "why_it_matters",
                        "whyItMatters",
                        default=""
                    )
                )

                side_a = get_value(
                    contradiction,
                    "side_a",
                    "sideA",
                    default=None
                )
                side_b = get_value(
                    contradiction,
                    "side_b",
                    "sideB",
                    default=None
                )

                if side_a or side_b:
                    st.markdown("**Side A**")

                    if isinstance(side_a, dict):
                        side_a_roles = deduplicate_strings(
                            get_value(
                                side_a,
                                "roles",
                                default=[]
                            )
                        )
                        st.caption(", ".join(side_a_roles))
                        render_quotes(
                            get_value(
                                side_a,
                                "quotes",
                                default=[]
                            )
                        )

                    st.markdown("**Side B**")

                    if isinstance(side_b, dict):
                        side_b_roles = deduplicate_strings(
                            get_value(
                                side_b,
                                "roles",
                                default=[]
                            )
                        )
                        st.caption(", ".join(side_b_roles))
                        render_quotes(
                            get_value(
                                side_b,
                                "quotes",
                                default=[]
                            )
                        )

                else:
                    st.markdown("**Supporting quotes**")
                    render_quotes(
                        get_value(
                            contradiction,
                            "supporting_quotes",
                            "supportingQuotes",
                            default=[]
                        )
                    )

                st.markdown("**What should be validated**")
                st.write(
                    get_value(
                        contradiction,
                        "what_should_be_validated",
                        "whatShouldBeValidated",
                        default=""
                    )
                )

                st.markdown("**Potential product implication**")
                st.write(
                    get_value(
                        contradiction,
                        "potential_product_implication",
                        "potentialProductImplication",
                        default=""
                    )
                )


def render_weak_signals(analysis):
    weak_signals = get_section(
        analysis,
        "weak_signals",
        "Weak Signals / Emerging Patterns"
    )

    for signal in weak_signals:
        title = get_value(
            signal,
            "title",
            default="Untitled signal"
        )
        confidence = get_value(
            signal,
            "confidence",
            default="N/A"
        )

        coverage = calculate_coverage(
            signal,
            analysis
        )

        roles = ", ".join(coverage["roles"])

        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">{title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="metric-line">
                    Confidence: {confidence}/5 &nbsp;&nbsp; | &nbsp;&nbsp;
                    Coverage: {coverage['percentage']}%
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                f"{coverage['count']} out of {coverage['total']} interviewees"
                + (f" · Roles: {roles}" if roles else "")
            )

            with st.expander("Show details"):
                st.markdown("**Why it may matter**")
                st.write(
                    get_value(
                        signal,
                        "why_it_may_matter",
                        "whyItMayMatterStrategically",
                        default=""
                    )
                )

                st.markdown("**Supporting quotes**")
                render_quotes(
                    get_value(
                        signal,
                        "supporting_quotes",
                        "supportingQuotes",
                        default=[]
                    )
                )

                st.markdown("**Why this might be overlooked**")
                st.write(
                    get_value(
                        signal,
                        "why_this_might_be_overlooked",
                        "whyThisMightBeOverlooked",
                        default=""
                    )
                )


def render_assumptions(analysis):
    assumptions = get_section(
        analysis,
        "assumptions_to_validate",
        "Assumptions Requiring Validation"
    )

    for assumption in assumptions:
        title = get_value(
            assumption,
            "title",
            default="Untitled assumption"
        )
        risk_level = get_value(
            assumption,
            "risk_level",
            "riskLevel",
            default="N/A"
        )

        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">{title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="metric-line">
                    Risk level: {risk_level}
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("Show details"):
                st.markdown("**Why it may be dangerous**")
                st.write(
                    get_value(
                        assumption,
                        "why_it_may_be_dangerous",
                        "whyItMayBeDangerous",
                        default=""
                    )
                )

                st.markdown("**Supporting quotes**")
                render_quotes(
                    get_value(
                        assumption,
                        "supporting_quotes",
                        "supportingQuotes",
                        default=[]
                    )
                )

                st.markdown("**Suggested validation activity**")
                st.write(
                    get_value(
                        assumption,
                        "suggested_validation_activity",
                        "suggestedValidationActivity",
                        default=""
                    )
                )


with st.sidebar:
    st.markdown(
        '<div class="sidebar-intro">Discovery synthesis assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">What it analyzes</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
- Critical insights
- Strategic risks
- Contradictions
- Weak signals
- Assumptions to validate
- Supporting quotes
"""
    )

    st.markdown(
        '<div class="sidebar-heading">Best used for</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
- Interview notes or transcripts
- Survey responses
- Research summaries
"""
    )

    st.markdown(
        '<div class="sidebar-heading">How it works</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subheading">Evidence Strength:</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="score-row"><strong>5/5</strong> = unusually strong, highly consistent evidence</div>
<div class="score-row"><strong>4/5</strong> = strong, consistent evidence from 3+ participants</div>
<div class="score-row"><strong>3/5</strong> = clear evidence from 2+ participants</div>
<div class="score-row"><strong>2/5</strong> = strong evidence from one, or limited evidence from two</div>
<div class="score-row"><strong>1/5</strong> = limited evidence from one participant</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='height:10px;'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subheading">Strategic Importance:</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="score-row"><strong>5/5</strong> = major business impact</div>
<div class="score-row"><strong>4/5</strong> = important decision area</div>
<div class="score-row"><strong>3/5</strong> = meaningful consideration</div>
<div class="score-row"><strong>2/5</strong> = useful but non-critical</div>
<div class="score-row"><strong>1/5</strong> = minor observation</div>
""",
        unsafe_allow_html=True
    )


st.title("Pattern")
st.caption("Turn customer research into decisions.")

user_input = st.text_area(
    "Paste interview notes, transcripts, survey responses, or research summaries",
    height=300
)

if st.button("Analyze research"):

    if not user_input.strip():
        st.warning("Please paste interview notes.")

    else:
        with st.spinner("Analyzing research..."):

            with open(
                "prompts/research_synthesis_prompt_v6.md",
                "r"
            ) as file:
                extraction_prompt = file.read()

            prompt = f"""
{extraction_prompt}

Research notes:
{user_input}
"""

            response = client.chat.completions.create(
                model="gpt-5.6-luna",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert research insights synthesis "
                            "assistant. Return only valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

            try:
                analysis = json.loads(
                    clean_json_response(result)
                )

                st.subheader("Research Analysis")

                tab1, tab2, tab3, tab4, tab5 = st.tabs(
                    [
                        "Critical Insights",
                        "Strategic Risks",
                        "Contradictions",
                        "Weak Signals",
                        "Assumptions"
                    ]
                )

                with tab1:
                    render_critical_insights(analysis)

                with tab2:
                    render_strategic_risks(analysis)

                with tab3:
                    render_contradictions(analysis)

                with tab4:
                    render_weak_signals(analysis)

                with tab5:
                    render_assumptions(analysis)

            except json.JSONDecodeError:
                st.error(
                    "The model returned output that could not be parsed as JSON."
                )
                st.markdown("### Raw model output")
                st.code(result)
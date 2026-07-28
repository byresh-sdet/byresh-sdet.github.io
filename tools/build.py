#!/usr/bin/env python3
"""
green-suite static site builder.

Holds the shared shell (head / nav / footer) and all site content in one
place, and stamps out the plain HTML files GitHub Pages serves:

    python3 tools/build.py

Everything it writes is committed to the repo — the generator is a
convenience, not a runtime dependency.

Content policy for this site: employers and internal product names are
deliberately kept generic (see JOURNEY / PROJECTS below). Domains are
described, not named.
"""

import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def asset_ver(relpath):
    """Short content hash, appended to asset URLs so browsers and GitHub Pages
    fetch the new file instead of serving a stale cached copy."""
    import hashlib
    full = os.path.join(ROOT, relpath)
    try:
        with open(full, "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()[:8]
    except OSError:
        return "0"

SITE = {
    "url": "https://byresh-sdet.github.io/",
    "name": "Byresh Thimmeshappa",
    "short": "Byresh",
    "initial": "B",
    "role": "Senior SDET / QA Strategist",
    "email": "byresh.151993@gmail.com",
    "github": "https://github.com/byresh-sdet",
    "github_label": "byresh-sdet",
    # LinkedIn intentionally omitted from the public site. To add it, set a
    # URL here and re-run the build — contact.html picks it up automatically.
    "linkedin": "",
    "location": "Bangalore, India",
    "tagline": "green means ship it",
}

NAV = [
    ("index.html", "home"),
    ("about.html", "about"),
    ("skills.html", "skills"),
    ("projects.html", "projects"),
    ("blog.html", "blog"),
    ("contact.html", "contact"),
]


def shell(*, slug, title, description, body, depth=0, extra_js=""):
    """Wrap a page body in the shared document shell."""
    base = "../" * depth
    css_v = asset_ver("assets/css/style.css")
    js_v = asset_ver("assets/js/main.js")
    nav_links = "\n".join(
        '      <a href="{b}{href}">{label}</a>'.format(b=base, href=h, label=l)
        for h, l in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="{description}" />
<title>{title}</title>
<link rel="icon" type="image/png" href="{base}assets/img/favicon.png" />
<link rel="apple-touch-icon" href="{base}assets/img/favicon.png" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:type" content="website" />
<meta property="og:image" content="{SITE['url']}assets/img/byresh-400.jpg" />
<meta name="twitter:card" content="summary" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{base}assets/css/style.css?v={css_v}" />
<script>
  // set theme before first paint so there is no light/dark flash
  try {{
    document.documentElement.setAttribute(
      'data-theme', localStorage.getItem('gs-theme') || 'dark');
  }} catch (e) {{ }}
</script>
</head>
<body data-page="{slug}">

<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="{base}index.html"><span class="p">~$</span> green-suite</a>
    <div class="nav-right">
      <nav class="nav-links" id="nav-links">
{nav_links}
      </nav>
      <button class="icon-btn" id="theme-toggle" type="button" aria-label="Switch to light mode">☀</button>
      <button class="icon-btn nav-toggle" id="nav-toggle" type="button"
              aria-label="Toggle navigation" aria-expanded="false" aria-controls="nav-links">≡</button>
    </div>
  </div>
</header>

{body}

<footer>
  <div class="wrap fl">
    <span>© <span data-year></span> {SITE['short']} · SDET</span>
    <span>built with plain HTML — {SITE['tagline']} · <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
  </div>
</footer>

<button class="to-top" id="to-top" type="button" aria-label="Back to top">↑</button>

<script src="{base}assets/js/main.js?v={js_v}"></script>
{extra_js}
</body>
</html>
"""


# ============================================================
# shared fragments
# ============================================================

SIDEBAR = f"""    <aside>
      <div class="card reveal">
        <div class="avatar"><img src="assets/img/byresh-200.jpg" width="200" height="200"
             alt="{SITE['name']}" loading="lazy" decoding="async" /></div>
        <div class="who">{SITE['short']}</div>
        <div class="role">{SITE['role']}</div>
        <div class="bio">11+ years owning end-to-end quality for enterprise software and security
          platforms — test strategy, large-scale performance validation, and agentic AI workflows
          that generate and maintain test automation.</div>
      </div>
      <div class="card reveal">
        <h4>daily stack</h4>
        <div class="stack-list">
          <div><span>Python / Bash</span><span class="ok">✓</span></div>
          <div><span>pytest / Robot Framework</span><span class="ok">✓</span></div>
          <div><span>Playwright (Python) / Selenium</span><span class="ok">✓</span></div>
          <div><span>JMeter / Locust</span><span class="ok">✓</span></div>
          <div><span>AWS / Docker / Kubernetes</span><span class="ok">✓</span></div>
          <div><span>Datadog / Grafana</span><span class="ok">✓</span></div>
        </div>
      </div>
      <div class="card reveal">
        <h4>topics</h4>
        <div class="topics">
          <span>agentic-ai</span><span>mcp</span><span>local-llm</span><span>pytest</span><span>scale-testing</span><span>performance</span><span>jmeter</span><span>datadog</span><span>chatops</span><span>robot-framework</span><span>release-quality</span>
        </div>
      </div>
    </aside>"""

STATS = """  <section class="stats reveal">
    <div class="stat"><div class="n"><span data-count="11" data-suffix="+">11+</span></div><div class="l">years in quality engineering</div></div>
    <div class="stat"><div class="n"><span data-count="7000" data-suffix="">7,000</span></div><div class="l">VMs at peak scale test</div></div>
    <div class="stat"><div class="n"><span data-count="10" data-suffix="M">10M</span></div><div class="l">incidents in stress runs</div></div>
    <div class="stat"><div class="n">6</div><div class="l">OS families covered</div></div>
    <div class="stat"><div class="n"><span data-count="100" data-suffix="+">100+</span></div><div class="l">ChatOps utilities shipped</div></div>
  </section>"""


# ============================================================
# career journey — employers kept generic by choice
# ============================================================

JOURNEY = [
    {
        "year": "2015", "short": "Senior QA Engr", "role": "Senior Engineer — QA",
        "company": "Automotive IoT & wearable platforms", "period": "Jan 2015 — Aug 2018",
        "points": [
            "Validated API services for an automotive IoT platform using Swagger-driven test design and JMeter",
            "Tested a cloud wearable platform end to end, including device provisioning over Android ADB",
            "Verified cloud connectivity across both iOS and Android device estates",
            "Authored and maintained manual and automated suites covering platform reliability and performance",
        ],
        "tech": ["Python", "Appium", "JMeter", "Swagger", "Android ADB"],
    },
    {
        "year": "2018", "short": "Lead Engr", "role": "Lead Engineer — Testing",
        "company": "Connected-vehicle IoT platform", "period": "Sep 2018 — Nov 2021",
        "points": [
            "Led end-to-end quality for a connected-vehicle platform built on real-time stream processing",
            "Built one unified Python + Robot Framework suite covering API, web and mobile in a single CI pipeline",
            "Validated MQTT data flows for trip generation and on-board-diagnostics incident triggering",
            "Performed Kubernetes and Helm deployment validation on cloud infrastructure",
        ],
        "tech": ["Python", "Robot Framework", "Selenium", "Appium", "Kafka", "MQTT", "Jenkins", "Kubernetes"],
    },
    {
        "year": "2021", "short": "Senior SDET", "role": "Senior SDET / QA Strategist",
        "company": "Enterprise endpoint security platform", "period": "Nov 2021 — Present",
        "points": [
            "Own end-to-end QA strategy from requirement review through production sign-off, acting as final release approver",
            "Designed scale testing across 3,000–7,000 VMs spanning six OS families, on cloud and on-premise environments",
            "Ran stress tests at 5–10M security incidents to find breaking points; results set production sizing guidance",
            "Built a multi-agent, MCP-orchestrated pipeline that turns tickets and OpenAPI specs into reviewed test automation",
            "Built a local-LLM log-analysis framework that pinpoints failures in high-volume security logs",
            "Shipped 100+ Python Slack ChatOps utilities adopted by support teams across live deployments",
        ],
        "tech": ["Python", "MCP", "Claude API", "n8n", "pytest", "JMeter", "Locust", "AWS", "Datadog", "TestRail"],
    },
]


def journey_html():
    nodes = []
    for i, j in enumerate(JOURNEY):
        cls = "journey-node" + (" active done" if i == len(JOURNEY) - 1 else "")
        nodes.append(f"""        <button class="{cls}" data-idx="{i}" type="button">
          <span class="journey-node-dot"><span class="journey-node-dot-inner"></span></span>
          <span class="journey-node-year">{j['year']}</span>
          <span class="journey-node-role">{j['short']}</span>
        </button>""")
    return "\n".join(nodes)


JOURNEY_JS = "<script>window.GS_JOURNEY = " + json.dumps(JOURNEY) + ";</script>" + """
<script>
(function () {
  var data = window.GS_JOURNEY || [];
  var track = document.getElementById('journey-track');
  if (!track) return;
  var fill = document.getElementById('journey-fill');
  var detail = document.getElementById('journey-detail');
  var prev = document.getElementById('j-prev');
  var next = document.getElementById('j-next');
  var counter = document.getElementById('j-counter');
  var nodes = Array.prototype.slice.call(track.querySelectorAll('.journey-node'));
  var idx = data.length - 1;

  function render() {
    var j = data[idx];
    nodes.forEach(function (n, i) {
      n.classList.toggle('active', i === idx);
      n.classList.toggle('done', i <= idx);
    });
    if (fill) {
      fill.style.width = (data.length < 2 ? 100 : (idx / (data.length - 1)) * 100) + '%';
    }
    detail.innerHTML =
      '<div class="journey-detail-top">' +
        '<div>' +
          '<h3 class="journey-detail-role">' + j.role + '</h3>' +
          '<div class="journey-detail-company">' + j.company + '</div>' +
        '</div>' +
        '<div class="journey-detail-period">' + j.period + '</div>' +
      '</div>' +
      '<ul class="journey-detail-points">' +
        j.points.map(function (p) { return '<li>' + p + '</li>'; }).join('') +
      '</ul>' +
      '<div class="journey-detail-tech">' +
        j.tech.map(function (t) { return '<span>' + t + '</span>'; }).join('') +
      '</div>';
    counter.textContent = (idx + 1) + ' / ' + data.length;
    prev.disabled = idx === 0;
    next.disabled = idx === data.length - 1;
  }

  track.addEventListener('click', function (ev) {
    var b = ev.target.closest('.journey-node');
    if (!b) return;
    idx = parseInt(b.dataset.idx, 10);
    render();
  });
  prev.addEventListener('click', function () { if (idx > 0) { idx--; render(); } });
  next.addEventListener('click', function () { if (idx < data.length - 1) { idx++; render(); } });
  render();
})();
</script>"""


# ============================================================
# skills
# ============================================================

# Each group: (key, icon, label, level 0-100 for the sidebar bar, [skill names])
# The level drives only the thin category bar in the sidebar — no numbers are shown.
SKILL_GROUPS = [
    ("ai", "\U0001F916", "AI & Agentic QA", 92, [
        "Multi-agent design", "MCP orchestration", "Claude API", "Prompt design",
        "Local-LLM analysis", "Human-in-the-loop gates", "Self-healing policy",
        "OpenAPI-driven generation", "n8n", "ChatOps",
    ]),
    ("automation", "\u2328", "Languages & Automation", 90, [
        "Python", "pytest", "Robot Framework", "Bash", "Playwright (Python)",
        "Selenium", "Appium", "Postman", "JSON schema validation", "YAML",
    ]),
    ("scale", "\U0001F4C8", "Performance & Scale", 88, [
        "Scale test design", "JMeter", "Locust", "Capacity analysis",
        "Bottleneck analysis", "Rate-limit validation", "Concurrency testing",
        "3K\u20137K VM fleets", "5\u201310M incident stress",
    ]),
    ("infra", "\u2601", "Cloud & CI/CD", 84, [
        "AWS EC2", "AWS EKS", "S3", "MSK", "DocumentDB", "Redis",
        "Docker", "Kubernetes", "Helm", "Jenkins", "GitHub Actions",
    ]),
    ("practice", "\U0001F9ED", "Quality Practice", 94, [
        "Test strategy", "Risk-based planning", "Quality gates", "Release readiness",
        "Defect lifecycle & RCA", "Quality metrics", "TestRail", "JIRA",
        "Datadog", "Grafana", "Shift-left reviews",
    ]),
]


def skills_html():
    """Sidebar tabs + mobile icon tabs + one panel per category."""
    tabs, mobile, panels = [], [], []
    for i, (key, icon, label, level, items) in enumerate(SKILL_GROUPS):
        active = " active" if i == 0 else ""
        sel = "true" if i == 0 else "false"

        tabs.append(f"""        <button class="skills-sidebar-tab cat-{key}{active}" type="button"
                role="tab" aria-selected="{sel}" data-panel="{key}">
          <span class="skills-sidebar-icon">{icon}</span>
          <span class="skills-sidebar-info">
            <span class="skills-sidebar-title">{label}</span>
            <span class="skills-sidebar-bar-track">
              <span class="skills-sidebar-bar-fill" data-pct="{level}"></span>
            </span>
          </span>
          <span class="skills-sidebar-badge">{len(items)}</span>
        </button>""")

        mobile.append(
            f'        <button class="skills-tab-mobile cat-{key}{active}" type="button"'
            f' aria-label="{label}" data-panel="{key}">{icon}</button>'
        )

        tiles = "\n".join(
            f"""            <div class="skill-tile">
              <span class="skill-tile-icon"><span class="skill-tile-dot"></span></span>
              <span class="skill-tile-name">{t}</span>
            </div>""" for t in items
        )
        panels.append(f"""      <section class="skills-panel cat-{key}{active}" id="panel-{key}" role="tabpanel">
        <div class="skills-panel-header">
          <div class="skills-panel-icon">{icon}</div>
          <div>
            <h3 class="skills-panel-title">{label}</h3>
            <p class="skills-panel-count">{len(items)} skills</p>
          </div>
        </div>
        <div class="skills-panel-items">
{tiles}
        </div>
      </section>""")

    return "\n".join(tabs), "\n".join(mobile), "\n".join(panels)


# ============================================================
# projects
# ============================================================

PROJECTS = [
    ("g-green", "🤖", "Multi-Agent Test Pipeline (MCP)", "Agentic AI · Python",
     "Requirements-extraction, generation, reviewer and automation agents that ingest tickets and OpenAPI specs "
     "and produce reviewed, runnable API test automation — with a human approval gate at every stage before merge.",
     [("4", "agent roles"), ("100%", "human-gated")],
     ["MCP", "Claude API", "n8n", "Python", "OpenAPI"]),
    ("g-violet", "🔍", "Local-LLM Log Analysis", "Applied LLM · Triage",
     "Parses high-volume security and system logs and pinpoints the failing component through automated pattern "
     "matching, cutting the manual triage step that used to sit in front of every root-cause analysis.",
     [("local", "no data egress"), ("↓", "triage time")],
     ["Local LLM", "Python", "Pattern detection"]),
    ("g-blue", "🖧", "Scale Test Framework", "Performance · 7K VMs",
     "Full lifecycle scale testing across 3,000–7,000 VMs and six OS families on cloud and on-premise: provisioning, "
     "agent install, connectivity validation and behaviour verification under sustained load.",
     [("7,000", "VMs"), ("6", "OS families")],
     ["Python", "AWS EC2", "Bash", "Custom harness"]),
    ("g-warm", "💥", "Incident Stress Harness", "Performance · Capacity",
     "Stress runs at 5–10 million security incidents to locate system breaking points. Findings fed directly into "
     "production infrastructure sizing and customer deployment guidance.",
     [("10M", "incidents"), ("→", "sizing guidance")],
     ["Locust", "JMeter", "Datadog", "DocumentDB"]),
    ("g-pink", "💬", "Slack ChatOps Toolkit", "Developer experience",
     "100+ Python utilities for test execution, incident tracking and log collection, driven from Slack and adopted "
     "by support teams across every live deployment.",
     [("100+", "utilities"), ("all", "deployments")],
     ["Python", "Slack API", "ChatOps"]),
    ("g-lilac", "🔗", "Unified Automation Suite", "Framework · IoT",
     "One Python and Robot Framework suite covering API, web and mobile in a single CI pipeline with real-device "
     "testing — replacing three separate per-surface frameworks.",
     [("3→1", "frameworks"), ("1", "CI pipeline")],
     ["Robot Framework", "Python", "Selenium", "Appium", "Jenkins"]),
]


def projects_html():
    out = []
    for grad, icon, title, domain, desc, metrics, tech in PROJECTS:
        m = "".join(f"<div><b>{v}</b>{k}</div>" for v, k in metrics)
        t = "".join(f"<span>{x}</span>" for x in tech)
        out.append(f"""    <article class="proj reveal">
      <div class="proj-banner" style="background: var(--{grad})">{icon}</div>
      <div class="proj-body">
        <h3>{title}</h3>
        <div class="proj-domain">{domain}</div>
        <p>{desc}</p>
        <div class="proj-metrics">{m}</div>
        <div class="journey-detail-tech">{t}</div>
      </div>
    </article>""")
    return "\n".join(out)


# ============================================================
# posts
# ============================================================

POSTS = [
    {
        "slug": "multi-agent-test-pipeline-mcp",
        "cat": "ai", "cat_label": "Agentic AI",
        "date": "2026-07-18", "read": "12 min",
        "title": "Designing a Multi-Agent Test Pipeline with MCP",
        "excerpt": "Four agent roles — extraction, generation, review, automation — turning tickets and OpenAPI specs into runnable API tests, with a human gate at every stage.",
        "tags": ["mcp", "agents", "llm"],
        "body": """
<h2>Why more than one agent</h2>
<p>The obvious version of "AI writes my tests" is one prompt: hand a model a ticket, ask for a
test, paste the result. It works for demos and falls apart on real specs, because a single
prompt is doing four unrelated jobs at once — reading requirements, designing cases, judging
whether those cases are any good, and producing runnable code.</p>
<p>Splitting those into separate roles helped for a reason that has little to do with model
capability: <strong>each role gets its own success criterion, and each boundary is a place a
human can stand.</strong></p>

<h3>The four roles</h3>
<ol>
  <li><strong>Requirements extraction</strong> — reads the ticket and the OpenAPI spec, emits a
      structured list of testable behaviours. No test cases yet, just claims about what the
      system should do.</li>
  <li><strong>Test generation</strong> — turns each behaviour into concrete cases: inputs,
      expected status, expected schema, edge conditions.</li>
  <li><strong>Reviewer</strong> — judges the generated cases against the original spec. Looks for
      invented endpoints, assertions that can't fail, and missing negative paths.</li>
  <li><strong>Automation</strong> — writes the actual runnable test code and wires it into CI.</li>
</ol>

<h2>The gate matters more than the agents</h2>
<p>Every stage boundary is a human approval point. Nothing merges because a model said it was
fine. This is the part I'd keep even if the models got twice as good, because the failure mode
of generated tests is not "obviously broken" — it's <em>plausible and wrong</em>. A test that
asserts a 200 and nothing else passes forever and tells you nothing.</p>

<blockquote>An unreviewed generated test is worse than no test: it occupies the slot where a
real test would have gone, and it reports green.</blockquote>

<h2>Self-healing, with a hard limit</h2>
<p>The automation agent is allowed to repair its own tests, but only within a narrow band. The
policy that took the longest to get right:</p>
<ul>
  <li><strong>Auto-heal</strong> locator drift and environment drift — a renamed selector, a
      moved base URL, a changed test-data fixture. Mechanical breakage with no behavioural
      meaning.</li>
  <li><strong>Fail loudly</strong> when the behaviour or the contract has changed. A field that
      disappeared, a status code that moved, an enum that narrowed. These get escalated to the
      reviewer agent, never patched.</li>
  <li><strong>Log every heal</strong> for audit. If the system quietly fixed something, that
      shows up in a report a person reads.</li>
</ul>
<p>Without the third rule you build a machine that mends its own tests until they assert nothing.
That's the whole risk of self-healing in one sentence, and it's why the audit log isn't
optional.</p>

<h2>Orchestration</h2>
<p>The prototype wires the stages with n8n and the Claude API, with tool integrations for the
issue tracker, the source host and Slack. End to end it runs: ticket intake → extracted
behaviours → generated cases → review → automation → CI execution → summary posted back to
Slack.</p>
<p>Using a workflow tool rather than bespoke glue was the right call early. Most of the iteration
was on <em>where the humans stand</em> and what each agent is told, not on plumbing — and moving
a gate is a drag-and-drop instead of a refactor.</p>

<h2>What I'd tell someone starting</h2>
<ul>
  <li>Write the system instruction for each role separately. Shared prompts blur the roles back
      together and you lose the thing you split them up for.</li>
  <li>Make the reviewer adversarial. A reviewer that agrees with the generator is decoration.</li>
  <li>Decide the escalation policy before you enable any self-healing.</li>
  <li>Measure whether generated tests ever <em>catch</em> anything. Coverage that never fails is
      not coverage.</li>
</ul>
""",
    },
    {
        "slug": "local-llm-log-triage",
        "cat": "ai", "cat_label": "Agentic AI",
        "date": "2026-07-10", "read": "9 min",
        "title": "Local LLMs for Security Log Triage",
        "excerpt": "High-volume security logs, parsed and pattern-matched locally to point at the failing component — cutting the manual step that sat in front of every RCA.",
        "tags": ["local-llm", "logs", "rca"],
        "body": """
<h2>The step before the real work</h2>
<p>Root-cause analysis on a security platform starts with a boring, expensive step: reading logs.
Not analysing them — just finding the part worth analysing. Across a large release with many
components, that search dominated the time to diagnosis.</p>
<p>It's also exactly the kind of problem language models are good at: lots of semi-structured
text, patterns that are obvious once seen, no single regex that catches them all.</p>

<h2>Why local, specifically</h2>
<p>Security and system logs from customer-facing deployments are the last thing you want leaving
your network. Running the model locally removed that question entirely — no data egress, no
per-token cost on multi-gigabyte log sets, and no rate limit when someone wants to re-run the
whole pipeline over a week of history.</p>
<p>The tradeoff is capability, and it matters less than you'd expect. Triage is a
narrow task: cluster related lines, spot the anomalous sequence, name the component. A smaller
local model does that well. It doesn't need to reason about your architecture — it needs to
point at the right hundred lines.</p>

<h2>Structure beats cleverness</h2>
<p>The biggest wins came from work that wasn't model work at all:</p>
<ul>
  <li><strong>Normalise first.</strong> Timestamps, hostnames, thread IDs and request IDs get
      canonicalised before the model sees anything. Otherwise every line looks unique and no
      pattern emerges.</li>
  <li><strong>Chunk by transaction, not by line count.</strong> Cutting a log at an arbitrary
      token boundary splits the cause from the symptom. Chunking on request or incident
      boundaries keeps them together.</li>
  <li><strong>Deterministic pre-filter.</strong> Known-benign noise is stripped with plain
      pattern matching before the model runs. Cheaper, and it stops the model narrating things
      everyone already knows about.</li>
</ul>

<h2>Output that a person can act on</h2>
<p>The framework doesn't produce prose. For each run it emits the suspected component, the
specific line range that justifies it, and the matched pattern. Every claim is anchored to
evidence you can open.</p>

<blockquote>If the tool can't show you the lines it based a conclusion on, you'll end up reading
the logs anyway — and then you've added a step instead of removing one.</blockquote>

<h2>Where it helps and where it doesn't</h2>
<p><strong>Good at:</strong> pointing at the right component fast, spotting repeated patterns
across releases, catching sequences a human skims past at 2am.</p>
<p><strong>Bad at:</strong> genuinely novel failures with no precedent in the logs, and anything
where the root cause is an <em>absence</em> — the request that never arrived, the service that
never logged. Missing evidence is still a human's job.</p>

<h2>Honest accounting</h2>
<p>This did not replace root-cause analysis. It replaced the search that came before it. The
engineer still does the diagnosis; they just start on the right screen instead of the first
one.</p>
""",
    },
    {
        "slug": "scale-testing-7000-vms",
        "cat": "scale", "cat_label": "Scale",
        "date": "2026-06-30", "read": "13 min",
        "title": "Scale Testing Across 7,000 VMs and Six OS Families",
        "excerpt": "Provisioning, agent install, connectivity validation and behaviour verification — the full lifecycle of a scale test large enough that the harness becomes the hard part.",
        "tags": ["scale", "aws", "performance"],
        "body": """
<h2>At this size, the test harness is the system under test</h2>
<p>A hundred VMs is a big test. Seven thousand is a distributed system of its own, and most of
the engineering goes into the harness rather than the assertions. At that scale things fail
that simply don't at small scale: provisioning APIs throttle, a fraction of a percent of
installs hang forever, and "did every agent actually connect?" stops being answerable by
looking.</p>

<h2>The lifecycle, in order</h2>
<ol>
  <li><strong>Provisioning</strong> — spin up fleets across cloud and on-premise virtualisation,
      spanning six OS families from legacy Windows Server through current RHEL and Ubuntu.</li>
  <li><strong>Agent installation</strong> — deploy the product agent onto every host. This is
      where OS diversity hurts most; a working installer on one family proves nothing about the
      next.</li>
  <li><strong>Connectivity validation</strong> — confirm every agent registered with the
      management service. Not most. Every one, counted.</li>
  <li><strong>Behaviour verification</strong> — only now does the actual test run, under
      sustained load across a heterogeneous fleet.</li>
</ol>
<p>Steps one to three are the unglamorous majority of the work. Skipping the counting in step
three is how you get a "successful" scale run that quietly tested 5,800 VMs.</p>

<h3>Count what registered, don't assume it</h3>
<p>The single most valuable piece of the harness is a reconciliation step: what was provisioned,
versus what installed, versus what registered. Three numbers that should match and frequently
don't. The gap is either a real product bug at scale or a harness bug — and both are worth
knowing before you interpret any performance figure.</p>

<blockquote>A scale test that can't tell you its own denominator isn't measuring anything.</blockquote>

<h2>Six OS families is the multiplier</h2>
<p>Scale and compatibility interact in ways neither shows alone. Behaviour that is fine on
current Ubuntu can degrade badly on an old Windows Server under the same load, and you only see
it when both are in the same run. Keeping all six families in one fleet — rather than testing
each in isolation — is what surfaces the interesting failures.</p>
<p>It also makes the harness messier: different install mechanisms, different log locations,
different ways of asking "is the service up". Worth it.</p>

<h2>Reading the results</h2>
<p>Bottleneck analysis is where scale testing pays off. Watching CPU, memory, throughput and
latency together across the fleet points at the constraint, and it's rarely where people guess.
The recurring finding in our case was on the data layer — slow queries that were invisible at
small scale and dominant under sustained fleet-wide load, addressed through query and replica
configuration work.</p>

<h2>The output is a number someone else uses</h2>
<p>The point of all this isn't a green tick. It's sizing guidance: what infrastructure a
deployment of a given size actually needs. That number goes to the people planning production
capacity and to customers planning theirs, which is a much higher bar than "the test passed."</p>
""",
    },
    {
        "slug": "stress-testing-10m-incidents",
        "cat": "scale", "cat_label": "Scale",
        "date": "2026-06-21", "read": "10 min",
        "title": "Stress Testing to 10 Million Incidents: Finding the Breaking Point",
        "excerpt": "Load tests prove the system holds. Stress tests find where it stops — and that number is what production sizing should be built on.",
        "tags": ["stress", "capacity", "datadog"],
        "body": """
<h2>Load testing and stress testing answer different questions</h2>
<p>A load test asks: does the system meet its targets at expected volume? A stress test asks:
where does it stop, and how? Both matter, but only the second one gives you a sizing model,
because sizing is a question about headroom and headroom is measured from the ceiling down.</p>
<p>So the goal of these runs was explicitly to break things — pushing to 5–10 million security
incidents to find the point where behaviour changed.</p>

<h2>Ramp, don't leap</h2>
<p>Jumping straight to peak tells you only pass or fail. Ramping tells you the <em>shape</em> of
the degradation, which is the part with diagnostic value:</p>
<ul>
  <li><strong>Graceful degradation</strong> — latency climbs smoothly, nothing drops. Usually a
      queue absorbing pressure. Often acceptable.</li>
  <li><strong>Cliff</strong> — fine, fine, fine, then collapse. Almost always a hard resource
      limit: a connection pool, a thread pool, a disk.</li>
  <li><strong>Sawtooth</strong> — recovers and fails repeatedly. Something is retrying and
      amplifying its own load.</li>
</ul>
<p>The cliff is the interesting one, because the cliff edge <em>is</em> your sizing number.</p>

<h2>Watch four signals together</h2>
<p>Throughput, latency, error rate, resource saturation. Any one alone misleads:</p>
<ul>
  <li>Latency up, throughput flat → queueing or a lock.</li>
  <li>Latency up, throughput <em>down</em> → past the knee, the system is losing ground.</li>
  <li>Errors up, latency flat → something shedding load deliberately, like a limiter.</li>
  <li>Everything fine, one resource pinned → the next bottleneck, waiting.</li>
</ul>
<p>Correlating these across the run in Datadog is what turns "it fell over" into "it fell over
because of this."</p>

<h2>The data layer is usually the answer</h2>
<p>Across these runs the recurring constraint was the database, not the application tier —
specifically queries that were unremarkable at normal volume and pathological under sustained
incident load. Finding them meant watching query-level latency during the ramp rather than
looking at aggregate service health, which stayed green well past the point where individual
queries had gone bad.</p>

<blockquote>Aggregate health metrics are designed to stay calm. That's useful in production and
actively unhelpful in a stress test.</blockquote>

<h2>Rate limits and concurrency</h2>
<p>A related but separate question: does the API behave correctly when many callers hit it at
once? Rate limiting is meant to shed load — the test is whether it sheds the <em>right</em>
load and whether the service stays stable while doing it. Driving concurrent access with JMeter
against the microservices confirmed both the limiter's behaviour and that nothing downstream
destabilised when it engaged.</p>

<h2>What the number is for</h2>
<p>The deliverable was never "we tested to 10M." It was: at this incident volume you need this
infrastructure, and here is the evidence. That output shapes production sizing and customer
deployment guidelines — which is why the breaking point, not the passing point, is the number
worth finding.</p>
""",
    },
    {
        "slug": "slack-chatops-for-qa",
        "cat": "tooling", "cat_label": "Tooling",
        "date": "2026-06-08", "read": "8 min",
        "title": "100+ Slack ChatOps Utilities, and Why Support Adopted Them",
        "excerpt": "Test execution, incident tracking and log collection driven from Slack — built for QA, adopted by support teams across every live deployment.",
        "tags": ["chatops", "python", "slack"],
        "body": """
<h2>Built for one team, used by another</h2>
<p>These utilities started as QA convenience: trigger a run, pull logs, check an incident,
without leaving the channel where the conversation was already happening. The interesting part
is that support teams picked them up and ran them across live customer deployments — a group
nobody designed for.</p>
<p>That happened for a specific reason worth generalising: <strong>the hard part of these tasks
was never the task, it was knowing how to do it.</strong> Which host, which credential, which
flag, which log path. A Slack command encodes all of that once, and then anyone can run it.</p>

<h2>What makes a good ChatOps command</h2>
<p>After a hundred of them, the ones that get used share traits:</p>
<ul>
  <li><strong>One job.</strong> A command that does one thing with two arguments beats a command
      with a mode flag every time.</li>
  <li><strong>Answers in the channel.</strong> If the output is a link to somewhere else, the
      command saved nothing.</li>
  <li><strong>Safe by default.</strong> Read-only unless clearly named otherwise. Anything
      destructive confirms first.</li>
  <li><strong>Says what it did.</strong> Including which environment it touched. Especially
      which environment it touched.</li>
</ul>

<h2>The three categories that mattered</h2>
<ol>
  <li><strong>Test execution</strong> — kick off suites, check status, fetch results without a CI
      console login.</li>
  <li><strong>Incident tracking</strong> — query incident state directly, mid-conversation,
      instead of context-switching to a dashboard.</li>
  <li><strong>Log collection</strong> — the runaway winner. Gathering logs from the right host
      with the right scope is tedious, error-prone, and exactly what a command should do.</li>
</ol>

<h2>Volume came from AI-assisted development</h2>
<p>Getting to 100+ was possible because each new utility is mostly a variation on a solved
shape: parse arguments, call a service, format a response, handle failure. That's a pattern an
assistant accelerates well — and it shifts the bottleneck from typing to deciding what's worth
building.</p>
<p>The constraint became judgement, not throughput. Most command ideas shouldn't exist; the
useful ones automate knowledge, not keystrokes.</p>

<blockquote>The best of these didn't save time on the work. They saved the twenty minutes of
figuring out how to start the work.</blockquote>

<h2>The lesson</h2>
<p>Internal tooling gets judged on whether people use it, and people use it when it removes a
question rather than a step. Nobody adopted a command because it was faster to type. They
adopted it because they no longer had to remember how the thing worked.</p>
""",
    },
    {
        "slug": "unified-robot-framework-suite",
        "cat": "automation", "cat_label": "Automation",
        "date": "2026-05-27", "read": "9 min",
        "title": "One Suite for API, Web and Mobile with Robot Framework",
        "excerpt": "Three per-surface frameworks collapsed into a single Python and Robot Framework suite running in one CI pipeline with real-device testing.",
        "tags": ["robot-framework", "python", "ci"],
        "body": """
<h2>Three frameworks, three sets of everything</h2>
<p>The starting position was familiar: one framework for API tests, one for web, one for mobile.
Each with its own runner, its own reporting, its own idea of test data, and its own CI job.
Three places to fix any shared bug, three reports to reconcile, and no way to answer "did this
release pass?" without opening all three.</p>
<p>The surfaces were different. Almost everything around them was the same.</p>

<h2>Why keyword-driven worked here</h2>
<p>Robot Framework's keyword abstraction fits this problem well: a keyword is just a named
action, and nothing about that name has to reveal whether it's driving HTTP, a browser, or a
device. So the layering falls out naturally:</p>
<ul>
  <li><strong>Business keywords</strong> — <em>Create Trip</em>, <em>Trigger Diagnostic Alert</em>.
      Readable by people who don't write tests, stable across refactors.</li>
  <li><strong>Technical keywords</strong> — the surface-specific work, backed by custom Python
      libraries where the built-ins ran out.</li>
  <li><strong>Shared services</strong> — auth, test data, config, reporting. Written once, used
      by all three surfaces. This is where the duplication actually was.</li>
</ul>
<p>Custom Python libraries matter. Robot is a good orchestration layer and a bad place to write
logic; anything with real branching belongs in Python, exposed as a keyword.</p>

<h2>One pipeline</h2>
<p>Consolidating into a single Jenkins pipeline — including real-device mobile execution —
changed the reporting more than the running. One run, one report, one verdict. "Did this
release pass?" became a question with one answer, which sounds trivial and was the main thing
people wanted.</p>

<h3>Real devices in CI</h3>
<p>Real-device testing is where mobile gets honest — and where flake concentrates. What kept it
manageable: treat device availability as an explicit precondition rather than an assumption,
and fail the job clearly when a device isn't there instead of letting tests fail mysteriously.
A pipeline that can't get a device should say so.</p>

<blockquote>Most mobile "flake" I've chased turned out to be an environment problem wearing a
test failure's clothes.</blockquote>

<h2>What I'd keep and what I'd change</h2>
<p><strong>Keep:</strong> the shared-services layer and business-keyword vocabulary. Those were
the real wins and they'd apply in any framework.</p>
<p><strong>Change:</strong> I'd push harder on moving logic into Python earlier. The temptation
to solve one more thing in Robot syntax is strong and it always costs more later.</p>
<p>The headline is three frameworks becoming one. The value was the shared layer underneath —
the consolidation just forced us to build it.</p>
""",
    },
]


def post_card(p, base=""):
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    return f"""      <article class="post reveal" data-cat="{p['cat']}" data-tags="{' '.join(p['tags'])}">
        <div class="meta"><span class="cat">{p['cat_label']}</span><span>{p['date']}</span><span class="dim">·</span><span>{p['read']}</span></div>
        <h3><a href="{base}posts/{p['slug']}.html">{p['title']}</a></h3>
        <p>{p['excerpt']}</p>
        <div class="foot"><div class="tags">{tags}</div><a class="read" href="{base}posts/{p['slug']}.html">read →</a></div>
      </article>"""


# ============================================================
# hero terminal animation (index only)
# ============================================================

HERO_JS = """<script>
(function () {
  var term = document.getElementById('term');
  if (!term) return;
  var cursor = document.getElementById('cursor');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var lines = [
    ['<span class="cmd"><span class="pr">byresh@green-suite</span>:<span class="pa">~/portfolio</span>$ pytest --profile -v</span>', 420],
    ['<span class="dim">========================= test session starts =========================</span>', 180],
    ['<span class="muted">collected 12 items</span>\\n', 260],
    ['tests/profile.py::<span class="tname">test_role[senior_sdet]</span> <span class="pass">PASSED</span> <span class="dim">[  8%]</span>', 90],
    ['tests/profile.py::<span class="tname">test_experience[11_years]</span> <span class="pass">PASSED</span> <span class="dim">[ 16%]</span>', 90],
    ['tests/stack.py::<span class="tname">test_language[python]</span> <span class="pass">PASSED</span> <span class="dim">[ 25%]</span>', 90],
    ['tests/stack.py::<span class="tname">test_frameworks[pytest,robot]</span> <span class="pass">PASSED</span> <span class="dim">[ 33%]</span>', 90],
    ['tests/ai.py::<span class="tname">test_agent_pipeline[mcp]</span> <span class="pass">PASSED</span> <span class="dim">[ 41%]</span>', 90],
    ['tests/ai.py::<span class="tname">test_log_triage[local_llm]</span> <span class="pass">PASSED</span> <span class="dim">[ 50%]</span>', 90],
    ['tests/scale.py::<span class="tname">test_fleet[7000_vms]</span> <span class="pass">PASSED</span> <span class="dim">[ 58%]</span>', 90],
    ['tests/scale.py::<span class="tname">test_stress[10M_incidents]</span> <span class="pass">PASSED</span> <span class="dim">[ 66%]</span>', 90],
    ['tests/scale.py::<span class="tname">test_os_families[6]</span> <span class="pass">PASSED</span> <span class="dim">[ 75%]</span>', 90],
    ['tests/tooling.py::<span class="tname">test_chatops_utilities[100+]</span> <span class="pass">PASSED</span> <span class="dim">[ 83%]</span>', 90],
    ['tests/quality.py::<span class="tname">test_manual_regressions</span> <span class="skip">SKIPPED</span> <span class="dim">(automated)</span> <span class="dim">[ 91%]</span>', 90],
    ['tests/hire.py::<span class="tname">test_open_to_work</span> <span class="pass">PASSED</span> <span class="dim">[100%]</span>\\n', 320],
    ['<span class="pass">=============== 11 passed, 1 skipped in 0.42s ===============</span>', 200],
    ['<span class="muted">release readiness: </span><span class="pass">approved</span><span class="muted"> · scroll down for the write-ups ↓</span>', 0]
  ];

  if (reduce) {
    if (cursor) cursor.remove();
    term.innerHTML = lines.map(function (l) {
      return '<div class="line">' + l[0] + '</div>';
    }).join('');
    return;
  }

  var i = 0;
  function next() {
    if (i >= lines.length) return;
    var div = document.createElement('div');
    div.className = 'line';
    div.innerHTML = lines[i][0];
    term.insertBefore(div, cursor);
    var d = lines[i][1];
    i++;
    setTimeout(next, d);
  }
  setTimeout(next, 350);
})();
</script>"""

FILTER_JS = """<script>
(function () {
  var chips = document.getElementById('chips');
  var search = document.getElementById('search');
  if (!chips || !search) return;
  var posts = Array.prototype.slice.call(document.querySelectorAll('.post'));
  var listEl = document.getElementById('posts');
  var activeCat = 'all';

  function apply() {
    var q = search.value.trim().toLowerCase();
    var shown = 0;
    posts.forEach(function (p) {
      var catOk = activeCat === 'all' || p.dataset.cat === activeCat;
      var hay = (p.textContent + ' ' + (p.dataset.tags || '')).toLowerCase();
      var qOk = q === '' || hay.indexOf(q) !== -1;
      var show = catOk && qOk;
      p.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    var old = document.getElementById('empty');
    if (old) old.remove();
    if (shown === 0) {
      var e = document.createElement('div');
      e.id = 'empty'; e.className = 'empty';
      e.textContent = 'no posts found matching your query — 0 results';
      listEl.appendChild(e);
    }
  }

  chips.addEventListener('click', function (ev) {
    var b = ev.target.closest('.chip');
    if (!b) return;
    chips.querySelectorAll('.chip').forEach(function (c) { c.classList.remove('active'); });
    b.classList.add('active');
    activeCat = b.dataset.cat;
    apply();
  });
  search.addEventListener('input', apply);
})();
</script>"""


# ============================================================
# pages
# ============================================================

def build():
    def write(path, html):
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(html)

    # ---------------- index ----------------
    featured = "\n".join(post_card(p) for p in POSTS[:3])
    index_body = f"""<main class="wrap">

  <section class="hero">
    <div class="hero-grid">
      <div class="hero-card reveal in">
        <div class="hero-photo-ring">
          <div class="hero-photo-inner">
            <img src="assets/img/byresh-400.jpg"
                 srcset="assets/img/byresh-200.jpg 200w, assets/img/byresh-400.jpg 400w"
                 sizes="150px" width="400" height="400"
                 alt="{SITE['name']}" fetchpriority="high" decoding="async" />
          </div>
        </div>
      </div>
      <div class="reveal in">
        <div class="badge"><span class="pulse"></span> Open to opportunities</div>
        <h1 class="hero-name">Byresh <span class="gradient">Thimmeshappa</span></h1>
        <p class="hero-role">Senior SDET / QA Strategist · AI-Augmented Quality Engineering</p>
        <p class="hero-desc">11+ years owning end-to-end quality for enterprise software and security
          platforms — now building agentic AI and local-LLM workflows that generate, review and
          maintain test automation, backed by scale testing across thousands of machines.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="projects.html">view work →</a>
          <a class="btn" href="blog.html">read the notes</a>
          <a class="btn" href="contact.html">get in touch</a>
        </div>
      </div>
    </div>
  </section>

  <section class="hero" style="padding-top:26px">
    <div class="term reveal">
      <div class="term-bar">
        <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
        <span class="term-title">byresh@green-suite: ~/portfolio</span>
      </div>
      <div class="term-body hero-term" id="term"><span class="cursor" id="cursor"></span></div>
    </div>
  </section>

{STATS}

  <div class="sec-head reveal">
    <span class="pr">$</span><h2>cat ./what-i-do</h2>
  </div>
  <div class="card-grid">
    <div class="card hl-card reveal">
      <span class="hl-icon">🤖</span>
      <h3>Agentic AI for QA</h3>
      <p>Multi-agent, MCP-orchestrated pipelines that turn tickets and API specs into reviewed,
         runnable automation — with human approval gates and a self-healing policy that escalates
         instead of quietly masking regressions.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">🖧</span>
      <h3>Scale &amp; performance</h3>
      <p>Full-lifecycle scale testing across thousands of VMs and six OS families, stress runs to
         10M incidents, and the capacity analysis that turns a breaking point into production
         sizing guidance.</p>
    </div>
    <div class="card hl-card violet reveal">
      <span class="hl-icon">🚦</span>
      <h3>Release governance</h3>
      <p>Test strategy, risk-based prioritisation and quality gates — acting as final QA approver,
         with metrics that show whether the gates are actually catching anything.</p>
    </div>
  </div>

  <div class="sec-head reveal">
    <span class="pr">$</span><h2>ls ./posts --head -3</h2>
    <span class="note"><a href="blog.html">all posts →</a></span>
  </div>
  <div class="grid">
    <div class="posts" id="posts">
{featured}
    </div>
{SIDEBAR}
  </div>

</main>"""
    write("index.html", shell(
        slug="home",
        title="green-suite — Byresh Thimmeshappa · Senior SDET",
        description="Senior SDET and QA Strategist with 11+ years in test strategy, large-scale performance validation, and agentic AI quality engineering.",
        body=index_body, extra_js=HERO_JS))

    # ---------------- about ----------------
    about_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ whoami</div>
    <h1>About <span class="gradient">Byresh</span></h1>
    <p>Eleven years of owning quality — from device labs and IoT pipelines to endpoint security at
       scale, and now to agents that write and maintain the tests.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./about.md</h2></div>
  <div class="about-grid reveal">
    <div class="about-avatar">
      <div class="about-avatar-inner">
        <img src="assets/img/byresh-400.jpg"
             srcset="assets/img/byresh-200.jpg 200w, assets/img/byresh-400.jpg 400w"
             sizes="150px" width="400" height="400"
             alt="{SITE['name']}" decoding="async" />
      </div>
    </div>
    <div>
      <p>I'm a <strong>Senior SDET and QA Strategist</strong> with 11+ years owning end-to-end
        quality for enterprise software and security platforms — from requirement review through
        production sign-off. My current work centres on an endpoint security platform, where I own
        test strategy, act as final QA approver for customer-facing releases, and run performance
        validation at a scale where the test harness becomes its own engineering problem.</p>
      <p>The thread through all of it is <strong>evidence</strong>. Quality gates that can actually
        fail a release. Scale tests that can state their own denominator. Stress runs that produce
        a sizing number rather than a green tick. Metrics — defect escape rate, coverage,
        pass/fail trends — that change the next release instead of decorating the last one.</p>
      <p>Most recently I've been building <strong>agentic AI into the QA workflow</strong>: a
        multi-agent, MCP-orchestrated pipeline that turns tickets and OpenAPI specs into reviewed
        test automation, and a local-LLM log-analysis framework that finds the failing component
        in high-volume security logs. Both are designed around human review gates, because the
        failure mode of generated tests isn't obvious breakage — it's plausible and wrong.</p>
      <p>Based in {SITE['location']}.</p>
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>git log --reverse ./career</h2>
    <span class="note">click a node</span></div>
  <div class="journey reveal">
    <div class="journey-track-wrap">
      <div class="journey-track" id="journey-track">
        <div class="journey-line"><div class="journey-line-fill" id="journey-fill"></div></div>
{journey_html()}
      </div>
    </div>
    <div class="card journey-detail" id="journey-detail"></div>
    <div class="journey-nav">
      <button class="btn" id="j-prev" type="button">← prev</button>
      <button class="btn" id="j-next" type="button">next →</button>
      <span class="journey-nav-counter" id="j-counter"></span>
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./how-i-work</h2></div>
  <div class="card-grid">
    <div class="card hl-card reveal">
      <span class="hl-icon">🧭</span>
      <h3>Risk-based, not exhaustive</h3>
      <p>Test effort follows impact. Security detection, deployment and performance get depth;
         low-risk surfaces get proportionate coverage and an honest note saying so.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">⬅</span>
      <h3>Shift left, genuinely</h3>
      <p>In requirement and design reviews before development starts, looking for testability gaps
         while they still cost a conversation rather than a release.</p>
    </div>
    <div class="card hl-card violet reveal">
      <span class="hl-icon">📊</span>
      <h3>Evidence over assertion</h3>
      <p>Release readiness comes off dashboards correlating test execution with production
         telemetry — not from a status meeting.</p>
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./education</h2></div>
  <div class="card-grid two">
    <div class="card reveal">
      <h4>degree</h4>
      <h3>B.E., Computer Science &amp; Engineering</h3>
      <p>Sapthagiri College of Engineering, VTU — First Class</p>
    </div>
    <div class="card reveal">
      <h4>always on</h4>
      <h3>Continuous learning</h3>
      <p>Agent architecture, local model tooling, and whatever the last scale run taught me.
         Notes go in the <a href="blog.html">blog</a>.</p>
    </div>
  </div>

</main>"""
    write("about.html", shell(
        slug="about",
        title="about — Byresh Thimmeshappa · Senior SDET",
        description="11+ years in quality engineering: test strategy, scale and performance validation, and agentic AI QA workflows.",
        body=about_body, extra_js=JOURNEY_JS))

    # ---------------- skills ----------------
    tabs, mobile, panels = skills_html()
    total = sum(len(g[4]) for g in SKILL_GROUPS)
    skills_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ pip list --local</div>
    <h1>Technical <span class="gradient">arsenal</span></h1>
    <p>Tools and practices I work with, grouped by what they're for.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>ls ./skills</h2>
    <span class="note">{total} entries</span></div>

  <div class="skills-tabs-mobile" id="skills-tabs-mobile" role="tablist">
{mobile}
  </div>

  <div class="skills-layout">
    <div class="skills-sidebar reveal" id="skills-tabs" role="tablist">
{tabs}
      <div class="skills-sidebar-total">
        <span class="skills-sidebar-total-num">{total}</span> total skills
      </div>
    </div>
    <div class="skills-content reveal">
{panels}
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./working-agreements</h2></div>
  <div class="card-grid">
    <div class="card hl-card reveal">
      <span class="hl-icon">\U0001F6A6</span><h3>Gates, not dashboards</h3>
      <p>If a check can't block a release, it isn't a gate — and it will be ignored within a month.</p>
    </div>
    <div class="card hl-card warm reveal">
      <span class="hl-icon">\U0001F50D</span><h3>Evidence with every claim</h3>
      <p>A tool that reports a conclusion without the lines it came from just adds a step.</p>
    </div>
    <div class="card hl-card pink reveal">
      <span class="hl-icon">\U0001F91D</span><h3>Humans on the boundaries</h3>
      <p>Agents can draft, repair and report. Merging is a person's call, and every auto-fix is
         logged for audit.</p>
    </div>
  </div>

</main>"""
    write("skills.html", shell(
        slug="skills",
        title="skills — Byresh Thimmeshappa · Senior SDET",
        description="Agentic AI and MCP orchestration, Python automation, scale and performance testing, AWS and CI/CD, quality practice.",
        body=skills_body))

    # ---------------- projects ----------------
    projects_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ls ./projects</div>
    <h1>Things I've <span class="gradient">built</span></h1>
    <p>Pipelines, harnesses and tooling — with the numbers they actually moved. Employer and
       product names are kept generic here by choice.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>ls -l ./projects</h2>
    <span class="note">{len(PROJECTS)} entries</span></div>

  <div class="proj-grid">
{projects_html()}
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>echo $NEXT</h2></div>
  <div class="card reveal">
    <h3>Want the detail behind any of these?</h3>
    <p>Several have a write-up in the <a href="blog.html">blog</a> covering the design, what broke,
       and what I'd do differently. Or just <a href="contact.html">send a message</a>.</p>
  </div>

</main>"""
    write("projects.html", shell(
        slug="projects",
        title="projects — Byresh Thimmeshappa · Senior SDET",
        description="Multi-agent MCP test pipeline, local-LLM log analysis, 7,000-VM scale framework, stress harness and ChatOps tooling.",
        body=projects_body))

    # ---------------- blog ----------------
    cards = "\n".join(post_card(p) for p in POSTS)
    seen, chips = set(), ['    <button class="chip active" data-cat="all">all</button>']
    for p in POSTS:
        if p["cat"] in seen:
            continue
        seen.add(p["cat"])
        chips.append(f'    <button class="chip" data-cat="{p["cat"]}">{p["cat_label"]}</button>')
    blog_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ls ./posts --sort=recent</div>
    <h1>Notes from the <span class="gradient">pipeline</span></h1>
    <p>Write-ups on agentic AI in QA, testing at scale, and the tooling in between.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>grep ./posts</h2>
    <span class="note">{len(POSTS)} posts</span></div>

  <div class="controls reveal">
    <label class="search">
      <span>/</span>
      <input id="search" type="text" placeholder="grep posts…" autocomplete="off" />
    </label>
  </div>
  <div class="chips reveal" id="chips">
{chr(10).join(chips)}
  </div>

  <div class="grid" style="margin-top:20px">
    <div class="posts" id="posts">
{cards}
    </div>
{SIDEBAR}
  </div>

</main>"""
    write("blog.html", shell(
        slug="blog",
        title="blog — Byresh Thimmeshappa · Senior SDET",
        description="Write-ups on multi-agent test pipelines, local-LLM log triage, scale testing and QA tooling.",
        body=blog_body, extra_js=FILTER_JS))

    # ---------------- contact ----------------
    linkedin_row = ""
    if SITE["linkedin"]:
        linkedin_row = f"""      <a class="contact-item" href="{SITE['linkedin']}" target="_blank" rel="noopener noreferrer">
        <span class="ico">in</span>
        <span><span class="k">linkedin</span><br /><span class="v">connect</span></span>
      </a>
"""
    contact_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ./contact --open</div>
    <h1>Get in <span class="gradient">touch</span></h1>
    <p>Open to talking about quality engineering, AI-augmented testing, scale problems, or working
       together.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./contact.json</h2></div>

  <div class="contact-grid">
    <div class="card reveal">
      <h4>direct</h4>
      <a class="contact-item" href="mailto:{SITE['email']}">
        <span class="ico">✉</span>
        <span><span class="k">email</span><br /><span class="v">{SITE['email']}</span></span>
      </a>
      <a class="contact-item" href="{SITE['github']}" target="_blank" rel="noopener noreferrer">
        <span class="ico">⌥</span>
        <span><span class="k">github</span><br /><span class="v">{SITE['github_label']}</span></span>
      </a>
{linkedin_row}      <div class="contact-item">
        <span class="ico">◉</span>
        <span><span class="k">location</span><br /><span class="v">{SITE['location']}</span></span>
      </div>
      <div class="contact-item">
        <span class="ico">◉</span>
        <span><span class="k">status</span><br /><span class="v" style="color:var(--pass)">open to opportunities</span></span>
      </div>
    </div>

    <div class="card reveal">
      <h4>send a message</h4>
      <form id="contact-form">
        <div class="field">
          <label for="cf-name">name</label>
          <input id="cf-name" name="name" type="text" required placeholder="your name" />
        </div>
        <div class="field">
          <label for="cf-email">email</label>
          <input id="cf-email" name="email" type="email" required placeholder="you@example.com" />
        </div>
        <div class="field">
          <label for="cf-msg">message</label>
          <textarea id="cf-msg" name="message" required placeholder="what's on your mind?"></textarea>
        </div>
        <button class="btn btn-primary" type="submit">send →</button>
        <p class="form-note">Opens your mail client — no server, no tracking, nothing stored.</p>
      </form>
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>echo $AVAILABILITY</h2></div>
  <div class="card-grid">
    <div class="card hl-card reveal">
      <span class="hl-icon">🤝</span><h3>Good fits</h3>
      <p>Senior SDET, QA architect or quality-engineering leadership roles where testing is treated
         as engineering work.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">💬</span><h3>Happy to chat about</h3>
      <p>Agent design for test generation, self-healing policy, scale-test harness design, or
         capacity analysis under load.</p>
    </div>
    <div class="card hl-card violet reveal">
      <span class="hl-icon">⏱</span><h3>Response time</h3>
      <p>Usually within a couple of days. Email is the fastest route.</p>
    </div>
  </div>

</main>"""
    contact_js = f"""<script>
(function () {{
  var form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    var msg = form.elements.message.value.trim();
    var subject = encodeURIComponent('[green-suite] message from ' + name);
    var body = encodeURIComponent(msg + '\\n\\n— ' + name + ' <' + email + '>');
    window.location.href = 'mailto:{SITE['email']}?subject=' + subject + '&body=' + body;
  }});
}})();
</script>"""
    write("contact.html", shell(
        slug="contact",
        title="contact — Byresh Thimmeshappa · Senior SDET",
        description="Get in touch about quality engineering, AI-augmented testing and scale performance work.",
        body=contact_body, extra_js=contact_js))

    # ---------------- posts ----------------
    for i, p in enumerate(POSTS):
        prev_p = POSTS[i - 1] if i > 0 else None
        next_p = POSTS[i + 1] if i < len(POSTS) - 1 else None
        prev_link = (f'<a href="{prev_p["slug"]}.html">← {prev_p["title"]}</a>'
                     if prev_p else '<a href="../blog.html">← all posts</a>')
        next_link = (f'<a href="{next_p["slug"]}.html">{next_p["title"]} →</a>'
                     if next_p else '<a href="../contact.html">get in touch →</a>')
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        body = f"""<main class="wrap">
  <article class="article">
    <header class="article-head reveal in">
      <div class="meta" style="display:flex;gap:10px;align-items:center;font-size:11.5px;color:var(--muted);flex-wrap:wrap">
        <span class="cat">{p['cat_label']}</span><span>{p['date']}</span>
        <span class="dim">·</span><span>{p['read']} read</span>
      </div>
      <h1>{p['title']}</h1>
      <p style="color:var(--muted);font-size:14px;margin:0">{p['excerpt']}</p>
      <div class="tags" style="margin-top:12px">{tags}</div>
    </header>

    <div class="article-body reveal in">
{p['body'].strip()}
    </div>

    <nav class="article-nav">
      <span>{prev_link}</span>
      <span>{next_link}</span>
    </nav>
  </article>
</main>"""
        write(f"posts/{p['slug']}.html", shell(
            slug="blog",
            title=f"{p['title']} — Byresh Thimmeshappa",
            description=re.sub(r"\s+", " ", p["excerpt"]),
            body=body, depth=1))

    print(f"built {6 + len(POSTS)} pages")


if __name__ == "__main__":
    build()

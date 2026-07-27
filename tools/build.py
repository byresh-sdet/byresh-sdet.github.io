#!/usr/bin/env python3
"""
green-suite static site builder.

Holds the shared shell (head / nav / footer) in one place and stamps out the
plain HTML files GitHub Pages serves. Edit the shell or the DATA below, then:

    python3 tools/build.py

Everything it writes is committed to the repo — the generator is a convenience,
not a runtime dependency.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "url": "https://byresh-sdet.github.io/",
    "name": "Byresh",
    "initial": "B",
    "role": "Software Development Engineer in Test",
    "email": "byresh.sdet@example.com",   # TODO: swap for your real address
    "github": "https://github.com/byresh-sdet",
    "linkedin": "https://www.linkedin.com/in/",  # TODO: your profile URL
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
    """Wrap page body in the shared document shell."""
    base = "../" * depth
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
<link rel="stylesheet" href="{base}assets/css/style.css" />
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
    <span>© <span data-year></span> {SITE['name']} · SDET</span>
    <span>built with plain HTML — {SITE['tagline']} · <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
  </div>
</footer>

<button class="to-top" id="to-top" type="button" aria-label="Back to top">↑</button>

<script src="{base}assets/js/main.js"></script>
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
        <div class="who">{SITE['name']}</div>
        <div class="role">{SITE['role']}</div>
        <div class="bio">8+ years building test frameworks, CI pipelines, and quality gates for web, API, and mobile. Focused on fast, deterministic suites that engineers actually trust.</div>
      </div>
      <div class="card reveal">
        <h4>daily stack</h4>
        <div class="stack-list">
          <div><span>Playwright / Selenium</span><span class="ok">✓</span></div>
          <div><span>pytest / TestNG</span><span class="ok">✓</span></div>
          <div><span>Python / TypeScript / Java</span><span class="ok">✓</span></div>
          <div><span>GitHub Actions / Jenkins</span><span class="ok">✓</span></div>
          <div><span>k6 / JMeter</span><span class="ok">✓</span></div>
          <div><span>Docker / Allure</span><span class="ok">✓</span></div>
        </div>
      </div>
      <div class="card reveal">
        <h4>topics</h4>
        <div class="topics">
          <span>playwright</span><span>selenium</span><span>pytest</span><span>api</span><span>ci-cd</span><span>flaky-tests</span><span>k6</span><span>appium</span><span>pact</span><span>docker</span><span>allure</span>
        </div>
      </div>
    </aside>"""

STATS = """  <section class="stats reveal">
    <div class="stat"><div class="n"><span data-count="8" data-suffix="+">8+</span></div><div class="l">years in test automation</div></div>
    <div class="stat"><div class="n"><span data-count="2400" data-suffix="+">2,400+</span></div><div class="l">automated test cases</div></div>
    <div class="stat"><div class="n"><span data-count="92" data-suffix="%">92%</span></div><div class="l">critical-path coverage</div></div>
    <div class="stat"><div class="n">6&nbsp;min</div><div class="l">full suite, down from 40</div></div>
    <div class="stat"><div class="n">0</div><div class="l">flaky tests in CI</div></div>
  </section>"""


# ============================================================
# posts
# ============================================================

POSTS = [
    {
        "slug": "killing-flaky-tests-playwright",
        "cat": "playwright", "cat_label": "Playwright",
        "date": "2026-07-15", "read": "11 min",
        "title": "Killing Flaky Tests: Auto-Retry vs. Root-Cause",
        "excerpt": "Retries hide flake; they don't fix it. A framework for triaging the three real causes — timing, test-data bleed, and shared state — with Playwright traces as evidence.",
        "tags": ["flaky", "playwright", "traces"],
        "body": """
<h2>Retries are a painkiller, not a cure</h2>
<p>Every suite reaches the point where someone adds <code>retries: 2</code> to the config and the
build goes green. It feels like a fix. It isn't. A retried test is a test that told you
something and got ignored — you've traded a signal for a slightly longer pipeline.</p>
<p>The rule I hold teams to: retries are allowed, but every retry must be <em>recorded</em>. If a
test passes on attempt two, it still shows up on the flake report. Otherwise the debt is
invisible and it compounds.</p>

<pre><code>// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ['list'],
    ['json', { outputFile: 'flake-report.json' }],
  ],
  use: {
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
});</code></pre>

<h2>The three real causes</h2>

<h3>1. Timing — waiting on the wrong thing</h3>
<p>The most common flake by a wide margin. The test waits for a spinner to disappear when the
thing it actually cares about is a network response settling and a re-render landing.
<code>waitForTimeout</code> is the tell: it's a guess dressed as a wait.</p>
<p>Fix it by asserting on the state you care about, and let the framework poll:</p>
<pre><code>// brittle
await page.waitForTimeout(2000);
expect(await page.locator('.row').count()).toBe(25);

// deterministic
await expect(page.locator('.row')).toHaveCount(25, { timeout: 10_000 });</code></pre>

<h3>2. Test-data bleed</h3>
<p>Two tests reach for the same seeded user, run in parallel, and fight over its state. This one
is sneaky because it only appears under load — exactly when you shard the suite to make it
faster. Every test should mint the data it needs and tear it down, or claim from a pool with
a lease.</p>

<h3>3. Shared state that survives the test</h3>
<p>Local storage, cookies, feature flags, a stubbed clock. Playwright's isolated contexts remove
most of this for free; the leaks that remain are almost always on the server side.</p>

<h2>Traces are the evidence</h2>
<p>Guessing at flake is how you spend a week and fix nothing. With
<code>trace: 'retain-on-failure'</code>, every failed attempt leaves a full timeline — DOM snapshots,
network, console — and you open it with:</p>
<pre><code>npx playwright show-trace test-results/&lt;test&gt;/trace.zip</code></pre>
<p>Scrub to the failing assertion and look at the frame <em>before</em> it. Nine times out of ten
the answer is right there: a request still in flight, or a row rendered with stale data.</p>

<blockquote>A flaky test is a test that has found a real race condition and is being ignored.
Sometimes the race is in the test. Often it isn't.</blockquote>

<h2>The triage loop that worked</h2>
<ol>
  <li>Quarantine the test — tag it, keep it running, stop it blocking the merge queue.</li>
  <li>Pull the last ten traces. Failing at the same step? Timing. Different steps? State.</li>
  <li>Fix the cause, then remove the quarantine tag in the same PR.</li>
  <li>Anything quarantined for more than two weeks gets deleted. An ignored test is worse than no test.</li>
</ol>
<p>Six weeks of that took our flake rate from about 4% of runs to zero, and the merge queue
stopped being something people worked around.</p>
""",
    },
    {
        "slug": "sharding-pytest-suite-ci",
        "cat": "cicd", "cat_label": "CI/CD",
        "date": "2026-07-11", "read": "9 min",
        "title": "From 40 min to 6 min: Sharding a pytest Suite Across Runners",
        "excerpt": "Splitting 2,400 tests across parallel GitHub Actions runners with pytest-xdist and load-balanced sharding — plus how to keep flaky-order failures from creeping back in.",
        "tags": ["pytest", "github-actions", "xdist"],
        "body": """
<h2>Where the 40 minutes went</h2>
<p>2,400 tests on a single runner, mostly waiting: browser startup, network round-trips, fixture
setup repeated for tests that could have shared it. CPU sat near idle the whole time. That's
the shape of a suite that wants to be parallel.</p>

<h2>Step one: parallel within the runner</h2>
<p><code>pytest-xdist</code> gets you most of the first win with one flag:</p>
<pre><code>pytest -n auto --dist loadgroup</code></pre>
<p><code>loadgroup</code> matters. Plain <code>load</code> scatters tests across workers with no regard for
grouping, which shreds any module-scoped fixture you have. With <code>loadgroup</code> plus
<code>@pytest.mark.xdist_group</code>, tests that share expensive setup land on the same worker.</p>

<h2>Step two: shard across runners</h2>
<p>One machine only goes so far. GitHub Actions matrices give you N machines cheaply:</p>
<pre><code>jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4, 5, 6]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements-test.txt
      - run: |
          pytest -n 4 --dist loadgroup \\
                 --splits 6 --group ${{ matrix.shard }} \\
                 --junitxml=results-${{ matrix.shard }}.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: results-${{ matrix.shard }}
          path: results-${{ matrix.shard }}.xml</code></pre>

<h3>Split by duration, not by count</h3>
<p>Six equal-sized groups are not six equal-duration groups. <code>pytest-split</code> reads a stored
timing file and balances by measured runtime, which took our slowest shard from 11 minutes to
just under 6:</p>
<pre><code>pytest --store-durations   # once, on a full run
# commit .test_durations, then --splits/--group balances properly</code></pre>

<h2>What sharding breaks</h2>
<p>Parallelism turns every latent ordering assumption into a real failure. That's not a
regression — it's the suite finally telling the truth. Two things caused nearly all of it:</p>
<ul>
  <li><strong>Shared fixtures with module scope</strong> that were quietly doing global setup.
      Anything touching a shared resource got promoted to a session-scoped fixture behind a lock,
      or made per-test.</li>
  <li><strong>Seeded test accounts.</strong> Two shards logging in as the same user, one logging
      the other out. Replaced with a factory that mints a user per test and cleans up in teardown.</li>
</ul>
<p>To catch the rest before they hit main, run <code>pytest-randomly</code> nightly. If the suite only
passes in declaration order, it doesn't really pass.</p>

<h2>Merging results</h2>
<p>Six JUnit files aren't a report. A final job downloads all artifacts, merges them, and
publishes one summary — so a developer sees one number, not six jobs to click through.</p>
<pre><code>junitparser merge results-*.xml merged.xml</code></pre>

<h2>The result</h2>
<ul>
  <li>40 min → 6 min wall clock</li>
  <li>Six shards × four xdist workers = 24-way parallelism</li>
  <li>Compute cost roughly flat — same total work, less idle waiting</li>
  <li>Three genuine ordering bugs found and fixed on the way</li>
</ul>
""",
    },
    {
        "slug": "contract-testing-pact",
        "cat": "api", "cat_label": "API",
        "date": "2026-07-04", "read": "8 min",
        "title": "Contract Testing REST APIs with Pact — What Broke and Why",
        "excerpt": "Consumer-driven contracts caught three breaking changes before they shipped. A walkthrough of provider verification, the pact broker, and the CI gate that enforces it.",
        "tags": ["pact", "rest", "contracts"],
        "body": """
<h2>The gap contract tests fill</h2>
<p>Unit tests prove a service is internally consistent. End-to-end tests prove the whole system
works, slowly and flakily. The interesting failures live in between: the provider renamed a
field, its own tests still pass, and the consumer finds out in staging on a Friday.</p>
<p>Consumer-driven contracts close that gap without standing up the full stack.</p>

<h2>The consumer writes the expectation</h2>
<pre><code>await provider.addInteraction({
  state: 'an account with id 42 exists',
  uponReceiving: 'a request for account 42',
  withRequest: { method: 'GET', path: '/accounts/42' },
  willRespondWith: {
    status: 200,
    body: {
      id: like(42),
      displayName: like('Ada Lovelace'),
      status: term({ generate: 'active', matcher: 'active|suspended' }),
    },
  },
});</code></pre>
<p>Note what's <em>not</em> asserted. <code>like()</code> checks the type, not the value. A contract that
pins exact values is a contract that fails on every data change and teaches people to ignore it.
Assert on the shape you actually depend on, and nothing more.</p>

<h2>The provider proves it can satisfy it</h2>
<p>Running the consumer tests produces a pact file, published to a broker. The provider's own
pipeline then replays every interaction against a real instance:</p>
<pre><code>await new Verifier({
  provider: 'accounts-api',
  providerBaseUrl: 'http://localhost:8080',
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  publishVerificationResult: process.env.CI === 'true',
  providerVersion: process.env.GIT_SHA,
  stateHandlers: {
    'an account with id 42 exists': () => seedAccount({ id: 42 }),
  },
}).verifyProvider();</code></pre>
<p><code>stateHandlers</code> is where this lives or dies. Each provider state needs to set up exactly the
data the interaction assumes — no more. If your state handler seeds half the database, you've
rebuilt an integration test with extra steps.</p>

<h2>What it actually caught</h2>
<ol>
  <li><strong>A renamed field.</strong> <code>display_name</code> → <code>displayName</code>, shipped as a
      "cosmetic" change. Two consumers were reading the old key.</li>
  <li><strong>A narrowed enum.</strong> A status value was dropped as unused. It wasn't — one
      consumer branched on it.</li>
  <li><strong>A nullable turned non-null.</strong> The provider started omitting a field when
      empty rather than sending <code>null</code>, and a consumer's parser threw.</li>
</ol>
<p>All three would have passed every test the provider team had. None reached staging.</p>

<h2>The CI gate</h2>
<p>The piece that makes it real: nothing deploys unless the broker says the contracts hold for
that exact version against that environment.</p>
<pre><code>pact-broker can-i-deploy \\
  --pacticipant accounts-api \\
  --version "$GIT_SHA" \\
  --to-environment production</code></pre>
<p>Non-zero exit, no deploy. Without this step you don't have contract testing — you have a
dashboard.</p>

<blockquote>Contract tests answer one question well: can these two versions talk to each other?
Don't ask them to check business logic.</blockquote>
""",
    },
    {
        "slug": "selenium-grid-docker-actions",
        "cat": "selenium", "cat_label": "Selenium",
        "date": "2026-06-28", "read": "12 min",
        "title": "A Parallel Selenium Grid with Docker + GitHub Actions",
        "excerpt": "Standing up an ephemeral Selenium Grid per pipeline run — hub, nodes, and a health-check gate — so cross-browser tests run clean and tear down when the job ends.",
        "tags": ["selenium", "docker", "grid"],
        "body": """
<h2>Why ephemeral beats a standing grid</h2>
<p>A long-lived Selenium Grid slowly becomes a pet: browser versions drift from production,
zombie sessions eat slots, and one team's stuck job blocks everyone. An ephemeral grid — created
per pipeline run, destroyed with the job — has none of those problems, and the config lives in
the repo where it can be reviewed.</p>

<h2>The compose file</h2>
<pre><code>services:
  hub:
    image: selenium/hub:4.27
    ports: ["4442:4442", "4443:4443", "4444:4444"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4444/wd/hub/status"]
      interval: 5s
      timeout: 3s
      retries: 20

  chrome:
    image: selenium/node-chromium:4.27
    depends_on: { hub: { condition: service_healthy } }
    shm_size: 2gb
    environment:
      SE_EVENT_BUS_HOST: hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443
      SE_NODE_MAX_SESSIONS: 4
      SE_NODE_OVERRIDE_MAX_SESSIONS: "true"

  firefox:
    image: selenium/node-firefox:4.27
    depends_on: { hub: { condition: service_healthy } }
    shm_size: 2gb
    environment:
      SE_EVENT_BUS_HOST: hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443
      SE_NODE_MAX_SESSIONS: 4</code></pre>

<p><code>shm_size: 2gb</code> is not optional. The default 64 MB of shared memory makes Chrome crash
under parallel load, and the failure looks exactly like a flaky test — a tab that dies
mid-session with no useful error.</p>

<h2>Gate on readiness, not on sleep</h2>
<p>The single biggest source of "grid flake" is starting tests before every node has registered.
The hub reports this properly, so poll it:</p>
<pre><code>- name: Wait for grid
  run: |
    for i in $(seq 1 40); do
      ready=$(curl -sf http://localhost:4444/wd/hub/status \\
              | jq -r '.value.ready')
      if [ "$ready" = "true" ]; then echo "grid ready"; exit 0; fi
      sleep 3
    done
    echo "grid never became ready"; docker compose logs hub; exit 1</code></pre>
<p>Dumping the hub logs on failure turns "the pipeline is broken again" into a two-minute diagnosis.</p>

<h2>Sizing the parallelism</h2>
<p>Total sessions = nodes × <code>SE_NODE_MAX_SESSIONS</code>. Your test runner's thread count must not
exceed that, or tests queue silently and start timing out for reasons that have nothing to do
with the application. Two browsers × four sessions = eight; run eight threads, not sixteen.</p>

<h2>Tearing down properly</h2>
<pre><code>- name: Grid logs
  if: failure()
  run: docker compose logs --no-color > grid-logs.txt

- name: Tear down
  if: always()
  run: docker compose down -v</code></pre>
<p><code>if: always()</code> on teardown, <code>if: failure()</code> on log capture. Skip the first and self-hosted
runners fill up with orphaned containers within a week.</p>

<h2>Where it landed</h2>
<ul>
  <li>Cross-browser regression: 22 min → 7 min</li>
  <li>Zero shared-grid contention between teams</li>
  <li>Browser versions bumped by editing one image tag in a reviewed PR</li>
</ul>
""",
    },
    {
        "slug": "load-testing-k6-thresholds",
        "cat": "performance", "cat_label": "Performance",
        "date": "2026-06-20", "read": "10 min",
        "title": "Load Testing with k6 — Thresholds That Actually Gate a Release",
        "excerpt": "p95 latency and error-rate thresholds wired into CI so a regression fails the build, not the on-call engineer. Includes the scenario model and a Grafana breakdown.",
        "tags": ["k6", "load", "thresholds"],
        "body": """
<h2>A load test that can't fail is a report</h2>
<p>Most performance testing produces a PDF nobody reads. The change that made ours matter was
small: give the test a pass/fail opinion, and put it in the pipeline. k6 does this natively
with thresholds — if one is breached, the process exits non-zero and the deploy stops.</p>

<h2>Model the scenarios, not "the load"</h2>
<p>Real traffic isn't one flat shape. Ours is a steady browse pattern with a checkout spike, so
the test says exactly that:</p>
<pre><code>export const options = {
  scenarios: {
    browse: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 0 },
      ],
      exec: 'browse',
    },
    checkout_spike: {
      executor: 'constant-arrival-rate',
      rate: 40, timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 100,
      startTime: '3m',
      exec: 'checkout',
    },
  },
  thresholds: {
    'http_req_failed': ['rate&lt;0.01'],
    'http_req_duration{scenario:browse}': ['p(95)&lt;400'],
    'http_req_duration{scenario:checkout}': ['p(95)&lt;900', 'p(99)&lt;2000'],
    'checks': ['rate&gt;0.99'],
  },
};</code></pre>

<p>Two things worth copying. First, <strong>per-scenario thresholds</strong> — checkout is legitimately
slower than browse, and one global p95 hides both. Second, <code>constant-arrival-rate</code> for the
spike: it holds throughput fixed even as the system slows, which is what real users do. VU-based
executors accidentally back off under stress and flatter your results.</p>

<h2>Pick thresholds from data, not vibes</h2>
<p>We set each number from the current production p95 plus a 20% tolerance, pulled from the same
dashboards the SRE team uses. Numbers invented in a meeting either never fail or always fail;
either way people stop trusting them within a month.</p>

<h2>Wiring it into CI</h2>
<pre><code>- name: Load test
  run: k6 run --out experimental-prometheus-rw perf/checkout.js
  env:
    K6_PROMETHEUS_RW_SERVER_URL: ${{ secrets.PROM_URL }}
    BASE_URL: https://staging.internal</code></pre>
<p>Streaming to Prometheus means the Grafana panel and the pass/fail gate read the same data. When
a build fails you land on a dashboard filtered to that run, not a wall of terminal output.</p>

<h2>Reading a failure</h2>
<p>The useful move is to correlate three lines: p95 latency, requests per second, and error rate.</p>
<ul>
  <li>Latency climbs, throughput flat → a queue or a lock, usually a connection pool.</li>
  <li>Latency and throughput both fall → something upstream is shedding load.</li>
  <li>Latency fine, errors spike → a rate limiter or a dependency timing out.</li>
</ul>
<p>The regression that justified the whole project was the first shape: p95 tripled at 180 VUs
because the DB pool was capped at 20 connections. Config change, one line, caught before release.</p>

<blockquote>Set the threshold where you would actually page someone. If you wouldn't wake up for it,
it isn't a gate — it's a metric.</blockquote>
""",
    },
    {
        "slug": "appium-mobile-automation",
        "cat": "mobile", "cat_label": "Mobile",
        "date": "2026-06-12", "read": "7 min",
        "title": "Stable Appium Automation on Real Android Devices",
        "excerpt": "Element locators that survive OS updates, explicit waits over sleeps, and a device-farm strategy that keeps mobile regression under ten minutes.",
        "tags": ["appium", "android", "mobile"],
        "body": """
<h2>Mobile flake has different causes</h2>
<p>On the web, most flake is timing. On real devices you also get slow app starts, permission
dialogs, OS-level popups, and animations that make an element visible before it's tappable.
The good news is that all of them are addressable with the same discipline.</p>

<h2>Locators that survive an OS update</h2>
<p>XPath over a rendered hierarchy is the mobile equivalent of a CSS selector built from
auto-generated class names — it works until the next release. Rank locators like this:</p>
<ol>
  <li><code>accessibility id</code> — set by developers, stable, and it improves the app's actual
      accessibility. Ask for it in the same PR as the feature.</li>
  <li><code>resource-id</code> — stable enough, Android-specific.</li>
  <li><code>UiSelector</code> / predicate strings — fine when scoped tightly.</li>
  <li>XPath — last resort, and never absolute.</li>
</ol>
<pre><code># good
el = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "checkout-submit")

# fragile
el = driver.find_element(
    AppiumBy.XPATH, "//android.widget.LinearLayout[3]/android.widget.Button[1]")</code></pre>

<h2>Wait for interactable, not for present</h2>
<p>A view can be in the hierarchy, on screen, and still mid-animation. Tapping it registers on
whatever ends up under your finger a moment later — which is how you get a test that fails once
every thirty runs with a screenshot showing the correct screen.</p>
<pre><code>wait = WebDriverWait(driver, 20, poll_frequency=0.4)
btn = wait.until(EC.element_to_be_clickable(
    (AppiumBy.ACCESSIBILITY_ID, "checkout-submit")))
btn.click()</code></pre>
<p>Set a global <code>implicitlyWait</code> of zero and use explicit waits everywhere. Mixing the two
produces waits that multiply in ways nobody can reason about.</p>

<h2>Capabilities that stop the environment fighting you</h2>
<pre><code>caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:autoGrantPermissions": True,
    "appium:disableWindowAnimation": True,
    "appium:newCommandTimeout": 120,
    "appium:uiautomator2ServerLaunchTimeout": 60000,
    "appium:noReset": False,
}</code></pre>
<p><code>autoGrantPermissions</code> removes an entire class of "unexpected dialog" failures.
<code>disableWindowAnimation</code> alone cut our mobile flake by roughly half — no animation means no
window where an element is visible but not yet hittable.</p>

<h2>Emulators and real devices both, deliberately</h2>
<p>Emulators are cheap, parallel, and reproducible. Real devices catch the things emulators can't:
camera, biometrics, poor network, low memory. The split that worked:</p>
<ul>
  <li><strong>Every PR</strong> — smoke suite on emulators, four in parallel, under four minutes.</li>
  <li><strong>Nightly</strong> — full regression on a device farm across three OS versions and two form factors.</li>
  <li><strong>Pre-release</strong> — manual exploratory on the oldest supported device, because it always finds something.</li>
</ul>

<h2>Where it landed</h2>
<p>Mobile regression runs in nine minutes against six parallel emulators, and the nightly real-device
pass is the only place we've seen genuine device-specific bugs — three in the last year, all of
which would have shipped.</p>
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
    ['tests/profile.py::<span class="tname">test_role_is_sdet</span> <span class="pass">PASSED</span> <span class="dim">[  8%]</span>', 90],
    ['tests/profile.py::<span class="tname">test_experience[8_years]</span> <span class="pass">PASSED</span> <span class="dim">[ 16%]</span>', 90],
    ['tests/stack.py::<span class="tname">test_frameworks[playwright,selenium]</span> <span class="pass">PASSED</span> <span class="dim">[ 25%]</span>', 90],
    ['tests/stack.py::<span class="tname">test_languages[python,ts,java]</span> <span class="pass">PASSED</span> <span class="dim">[ 33%]</span>', 90],
    ['tests/ci.py::<span class="tname">test_suite_runtime_under[6min]</span> <span class="pass">PASSED</span> <span class="dim">[ 41%]</span>', 90],
    ['tests/ci.py::<span class="tname">test_flaky_count_is_zero</span> <span class="pass">PASSED</span> <span class="dim">[ 50%]</span>', 90],
    ['tests/api.py::<span class="tname">test_contract_verification[pact]</span> <span class="pass">PASSED</span> <span class="dim">[ 58%]</span>', 90],
    ['tests/perf.py::<span class="tname">test_p95_latency_threshold</span> <span class="pass">PASSED</span> <span class="dim">[ 66%]</span>', 90],
    ['tests/mobile.py::<span class="tname">test_appium_android_regression</span> <span class="pass">PASSED</span> <span class="dim">[ 75%]</span>', 90],
    ['tests/quality.py::<span class="tname">test_coverage[critical_path]</span> <span class="pass">PASSED</span> <span class="dim">[ 83%]</span>', 90],
    ['tests/quality.py::<span class="tname">test_manual_regressions</span> <span class="skip">SKIPPED</span> <span class="dim">(automated)</span> <span class="dim">[ 91%]</span>', 90],
    ['tests/hire.py::<span class="tname">test_open_to_work</span> <span class="pass">PASSED</span> <span class="dim">[100%]</span>\\n', 320],
    ['<span class="pass">=============== 11 passed, 1 skipped in 0.42s ===============</span>', 200],
    ['<span class="muted">coverage: </span><span class="pass">92%</span><span class="muted"> of critical paths · 0 flakes · scroll down for the write-ups ↓</span>', 0]
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
# journey (about page)
# ============================================================
# TODO: replace these with your real roles, dates and companies.
JOURNEY = [
    {
        "year": "2017", "short": "QA Engineer", "role": "QA Engineer",
        "company": "First automation role", "period": "2017 — 2019",
        "points": [
            "Wrote the team's first automated regression pack, replacing a 200-case manual checklist",
            "Owned defect triage and reporting across two Agile squads",
            "Built reusable page objects that cut new-test authoring time noticeably",
        ],
        "tech": ["Selenium", "Java", "TestNG", "JIRA"],
    },
    {
        "year": "2019", "short": "Automation Engr", "role": "Test Automation Engineer",
        "company": "Web + API automation", "period": "2019 — 2021",
        "points": [
            "Extended coverage from UI-only to API-first, moving the bulk of assertions below the UI",
            "Introduced data factories so tests stopped depending on seeded environments",
            "Cut nightly regression runtime by roughly half through parallel execution",
        ],
        "tech": ["Selenium", "REST Assured", "Python", "pytest", "Jenkins"],
    },
    {
        "year": "2021", "short": "Senior SDET", "role": "Senior SDET",
        "company": "Framework ownership", "period": "2021 — 2023",
        "points": [
            "Rebuilt the framework on Playwright, retiring a brittle Selenium suite",
            "Added trace-on-failure and a flake report that made retries visible instead of silent",
            "Set the merge-queue quality gate that blocks on smoke + contract verification",
        ],
        "tech": ["Playwright", "TypeScript", "pytest", "GitHub Actions", "Docker"],
    },
    {
        "year": "2023", "short": "Lead SDET", "role": "Lead SDET",
        "company": "Platform quality", "period": "2023 — 2025",
        "points": [
            "Sharded 2,400 tests across parallel runners, taking the suite from 40 min to 6 min",
            "Wired k6 thresholds into CI so performance regressions fail the build",
            "Drove flaky tests in CI to zero and kept them there with a quarantine policy",
        ],
        "tech": ["Playwright", "k6", "Pact", "Kubernetes", "Allure", "Grafana"],
    },
    {
        "year": "2025", "short": "SDET (current)", "role": "Software Development Engineer in Test",
        "company": "Quality engineering", "period": "2025 — present",
        "points": [
            "Own end-to-end quality strategy across web, API and mobile surfaces",
            "Mentor engineers on test design, shift-left practice and CI hygiene",
            "Report release readiness from pipeline data rather than gut feel",
        ],
        "tech": ["Playwright", "pytest", "Appium", "GitHub Actions", "k6", "Pact"],
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


def journey_data_js():
    import json
    return "<script>window.GS_JOURNEY = " + json.dumps(JOURNEY) + ";</script>"


JOURNEY_JS = journey_data_js() + """
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

SKILL_GROUPS = [
    ("automation", "🎭", "UI Automation", [
        ("Playwright", 95), ("Selenium WebDriver", 90),
        ("Appium", 80), ("Cypress", 70),
    ], ["Page objects", "Visual diffing", "Trace analysis", "Cross-browser", "Component testing"]),
    ("languages", "⌨", "Languages", [
        ("Python", 95), ("TypeScript / JavaScript", 88),
        ("Java", 80), ("Bash", 78), ("SQL", 75),
    ], ["pytest", "TestNG", "Jest", "asyncio", "Type hints"]),
    ("cicd", "⚙", "CI/CD & Infra", [
        ("GitHub Actions", 92), ("Docker", 88),
        ("Jenkins", 82), ("Kubernetes", 70),
    ], ["Matrix builds", "Test sharding", "Quality gates", "Artifact reporting", "Caching"]),
    ("api", "🔌", "API & Performance", [
        ("REST / HTTP testing", 92), ("k6", 85),
        ("Pact (contract testing)", 82), ("JMeter", 75),
    ], ["Schema validation", "Threshold gating", "Mock servers", "gRPC", "Postman/Newman"]),
    ("practice", "🧭", "Quality Practice", [
        ("Test strategy & design", 92), ("Flake forensics", 90),
        ("Shift-left reviews", 85), ("Release readiness", 85),
    ], ["Risk-based testing", "Exploratory", "Metrics & reporting", "Mentoring", "Agile QA"]),
]


def skills_html():
    tabs, panels = [], []
    for i, (key, icon, label, bars, tiles) in enumerate(SKILL_GROUPS):
        active = " active" if i == 0 else ""
        tabs.append(
            f'      <button class="skills-tab{active}" type="button" role="tab" '
            f'aria-selected="{"true" if i == 0 else "false"}" data-panel="{key}">'
            f'<span>{icon}</span><span>{label}</span>'
            f'<span class="count">{len(bars)}</span></button>'
        )
        rows = "\n".join(
            f"""          <div class="skill-row">
            <div class="top"><span class="nm">{n}</span><span class="pc">{p}%</span></div>
            <div class="bar-track"><div class="bar-fill" data-pct="{p}"></div></div>
          </div>""" for n, p in bars
        )
        tile_html = "\n".join(
            f'          <div class="tile"><span>▹</span><span>{t}</span></div>' for t in tiles
        )
        panels.append(f"""      <section class="skills-panel{active}" id="panel-{key}" role="tabpanel">
        <div class="card">
          <h4>{label} — proficiency</h4>
          <div class="skill-rows">
{rows}
          </div>
          <div class="tile-grid">
{tile_html}
          </div>
        </div>
      </section>""")
    return "\n".join(tabs), "\n".join(panels)


# ============================================================
# projects
# ============================================================

PROJECTS = [
    ("g-green", "🎭", "Playwright E2E Framework", "Web · TypeScript",
     "Trace-first end-to-end framework with fixture-scoped auth, per-test data factories and a flake report that makes every retry visible instead of silent.",
     [("2,400+", "tests"), ("6 min", "full run")], ["Playwright", "TypeScript", "GitHub Actions", "Allure"]),
    ("g-blue", "⚙", "Sharded pytest Pipeline", "CI/CD · Python",
     "Duration-balanced sharding across a runner matrix, with merged JUnit reporting so a developer sees one verdict rather than six jobs.",
     [("40→6", "minutes"), ("24×", "parallelism")], ["pytest", "pytest-xdist", "pytest-split", "Actions"]),
    ("g-violet", "🔌", "Contract Testing Gate", "API · Pact",
     "Consumer-driven contracts with a broker and a can-i-deploy gate — three breaking API changes stopped before they reached staging.",
     [("3", "breakages caught"), ("0", "reached prod")], ["Pact", "Node", "Docker", "Broker"]),
    ("g-warm", "📈", "k6 Performance Gate", "Performance",
     "Scenario-modelled load tests with per-scenario p95/p99 thresholds streamed to Prometheus, wired so a regression fails the build.",
     [("p95", "gated"), ("<1%", "error budget")], ["k6", "Prometheus", "Grafana", "Actions"]),
    ("g-pink", "🐳", "Ephemeral Selenium Grid", "Cross-browser",
     "Per-run hub and node containers with a readiness gate and log capture on failure — no standing grid, no cross-team contention.",
     [("22→7", "minutes"), ("2", "browsers")], ["Selenium Grid", "Docker Compose", "Actions"]),
    ("g-lilac", "📱", "Mobile Regression Suite", "Mobile · Android",
     "Accessibility-id-first locators, animation-disabled capabilities and an emulator/real-device split that keeps mobile regression under ten minutes.",
     [("9 min", "regression"), ("3", "OS versions")], ["Appium", "Python", "UiAutomator2", "Device farm"]),
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
# pages
# ============================================================

def build():
    write = lambda path, html: (
        os.makedirs(os.path.dirname(os.path.join(ROOT, path)) or ROOT, exist_ok=True),
        open(os.path.join(ROOT, path), "w", encoding="utf-8").write(html),
    )

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
        <h1 class="hero-name">{SITE['name']} <span class="gradient">· SDET</span></h1>
        <p class="hero-role">Test Automation · CI/CD Quality Gates · Performance</p>
        <p class="hero-desc">8+ years building test frameworks and pipelines for web, API and mobile —
          turning slow, flaky suites into fast, deterministic ones that engineers actually trust.</p>
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
      <span class="hl-icon">🎭</span>
      <h3>Automation architecture</h3>
      <p>UI and API frameworks built to be read and maintained by the whole team — page objects,
         data factories, and fixtures that don't leak state between tests.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">⚙</span>
      <h3>CI/CD quality gates</h3>
      <p>Sharded, parallel pipelines with gates that mean something: smoke, contracts and
         performance thresholds that block a bad merge instead of reporting on it later.</p>
    </div>
    <div class="card hl-card violet reveal">
      <span class="hl-icon">🔬</span>
      <h3>Flake forensics</h3>
      <p>Traces over guesses. Quarantine, diagnose, fix, un-quarantine — the loop that took a
         4% flake rate to zero and kept the merge queue moving.</p>
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
        title="green-suite — Byresh · SDET",
        description="Test automation, CI/CD pipelines, flaky-test forensics, and quality engineering notes from an SDET.",
        body=index_body, extra_js=HERO_JS))

    # ---------------- about ----------------
    about_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ whoami</div>
    <h1>About <span class="gradient">{SITE['name']}</span></h1>
    <p>How I got from manual test cases to owning quality for a platform.</p>
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
      <p>I'm a <strong>Software Development Engineer in Test</strong> with 8+ years building
        test frameworks, CI pipelines and quality gates for web, API and mobile products. My
        work sits where testing meets infrastructure: making suites fast enough that people
        run them, and trustworthy enough that a red build means something.</p>
      <p>Most of what I do falls into three buckets — designing automation that survives
        refactors, wiring quality gates into CI so problems fail early, and doing the
        unglamorous forensics that turns a flaky suite into a deterministic one.</p>
      <p>I'm a believer in shift-left: the cheapest bug is the one caught in review, the second
        cheapest is caught by a test written alongside the feature. Everything after that is
        expensive.</p>
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
      <h3>Risk first</h3>
      <p>Coverage numbers are a proxy. I start from what actually hurts if it breaks, and put the
         deepest testing there.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">⚡</span>
      <h3>Fast or ignored</h3>
      <p>A suite people wait 40 minutes for is a suite people route around. Speed is a
         correctness feature.</p>
    </div>
    <div class="card hl-card violet reveal">
      <span class="hl-icon">📊</span>
      <h3>Evidence over opinion</h3>
      <p>Traces, timings and flake reports. Release readiness should come off a dashboard, not
         out of a meeting.</p>
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./education</h2></div>
  <div class="card-grid two">
    <div class="card reveal">
      <h4>degree</h4>
      <h3>Bachelor of Engineering</h3>
      <p>Computer Science &amp; Engineering<br /><span class="dim">TODO: update institution and years</span></p>
    </div>
    <div class="card reveal">
      <h4>always on</h4>
      <h3>Continuous learning</h3>
      <p>Framework internals, distributed systems failure modes, and whatever the last
         production incident taught me. Notes go in the <a href="blog.html">blog</a>.</p>
    </div>
  </div>

</main>"""
    write("about.html", shell(
        slug="about",
        title="about — Byresh · SDET",
        description="8+ years of test automation, CI/CD quality gates and flake forensics — the career journey behind green-suite.",
        body=about_body, extra_js=JOURNEY_JS))

    # ---------------- skills ----------------
    tabs, panels = skills_html()
    total = sum(len(g[3]) + len(g[4]) for g in SKILL_GROUPS)
    skills_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ pip list --local</div>
    <h1>Technical <span class="gradient">stack</span></h1>
    <p>Tools and practices I use daily, grouped by what they're for. Percentages are
       self-assessed depth, not certification scores.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>ls ./skills</h2>
    <span class="note">{total} entries</span></div>

  <div class="skills-layout">
    <div class="skills-tabs reveal" id="skills-tabs" role="tablist">
{tabs}
    </div>
    <div class="reveal">
{panels}
    </div>
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>cat ./working-agreements</h2></div>
  <div class="card-grid">
    <div class="card hl-card reveal">
      <span class="hl-icon">🧪</span><h3>Test pyramid, honestly</h3>
      <p>Most assertions below the UI. E2E reserved for journeys that genuinely need a browser.</p>
    </div>
    <div class="card hl-card warm reveal">
      <span class="hl-icon">🚦</span><h3>Gates, not dashboards</h3>
      <p>If a check can't fail the build, it isn't a gate — and it will be ignored within a month.</p>
    </div>
    <div class="card hl-card pink reveal">
      <span class="hl-icon">🧹</span><h3>Delete dead tests</h3>
      <p>A quarantined test that nobody fixes in two weeks gets removed. Ignored tests cost trust.</p>
    </div>
  </div>

</main>"""
    write("skills.html", shell(
        slug="skills",
        title="skills — Byresh · SDET",
        description="Automation, languages, CI/CD, API and performance tooling used daily by an SDET.",
        body=skills_body))

    # ---------------- projects ----------------
    projects_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ls ./projects</div>
    <h1>Things I've <span class="gradient">built</span></h1>
    <p>Frameworks, pipelines and quality gates — with the numbers they actually moved.</p>
  </section>

  <div class="sec-head reveal"><span class="pr">$</span><h2>ls -l ./projects</h2>
    <span class="note">{len(PROJECTS)} entries</span></div>

  <div class="proj-grid">
{projects_html()}
  </div>

  <div class="sec-head reveal"><span class="pr">$</span><h2>echo $NEXT</h2></div>
  <div class="card reveal">
    <h3>Want the detail behind any of these?</h3>
    <p>Most of them have a write-up in the <a href="blog.html">blog</a> covering what broke,
       what the fix was, and what I'd do differently. Or just
       <a href="contact.html">send a message</a>.</p>
  </div>

</main>"""
    write("projects.html", shell(
        slug="projects",
        title="projects — Byresh · SDET",
        description="Test automation frameworks, sharded CI pipelines, contract testing gates and performance suites.",
        body=projects_body))

    # ---------------- blog ----------------
    cards = "\n".join(post_card(p) for p in POSTS)
    cats = [("all", "all")] + [(p["cat"], p["cat_label"]) for p in POSTS]
    seen, chips = set(), []
    for key, label in cats:
        if key in seen:
            continue
        seen.add(key)
        chips.append(f'    <button class="chip{" active" if key == "all" else ""}" data-cat="{key}">{label}</button>')
    blog_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ls ./posts --sort=recent</div>
    <h1>Notes from the <span class="gradient">pipeline</span></h1>
    <p>Write-ups on test automation, CI/CD and the failure modes in between.</p>
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
        title="blog — Byresh · SDET",
        description="Write-ups on Playwright, pytest sharding, contract testing, k6 thresholds and mobile automation.",
        body=blog_body, extra_js=FILTER_JS))

    # ---------------- contact ----------------
    contact_body = f"""<main class="wrap">

  <section class="page-head reveal in">
    <div class="eyebrow">$ ./contact --open</div>
    <h1>Get in <span class="gradient">touch</span></h1>
    <p>Open to talking about quality engineering, automation problems, or working together.</p>
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
        <span><span class="k">github</span><br /><span class="v">byresh-sdet</span></span>
      </a>
      <a class="contact-item" href="{SITE['linkedin']}" target="_blank" rel="noopener noreferrer">
        <span class="ico">in</span>
        <span><span class="k">linkedin</span><br /><span class="v">connect</span></span>
      </a>
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
      <p>SDET / QE roles where automation and CI are treated as engineering work, not a
         reporting function.</p>
    </div>
    <div class="card hl-card blue reveal">
      <span class="hl-icon">💬</span><h3>Happy to chat about</h3>
      <p>Flake triage, sharding strategies, contract testing, or reviewing a test framework you're
         unhappy with.</p>
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
        title="contact — Byresh · SDET",
        description="Get in touch about quality engineering, test automation and CI/CD work.",
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
            title=f"{p['title']} — Byresh · SDET",
            description=re.sub(r"\s+", " ", p["excerpt"]),
            body=body, depth=1))

    print(f"built {6 + len(POSTS)} pages")


if __name__ == "__main__":
    build()

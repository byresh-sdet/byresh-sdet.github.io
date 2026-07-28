/* ============================================================
   green-suite | shared site behaviour
   theme toggle · mobile nav · scroll reveal · back to top
   ============================================================ */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- theme ---------- */
  var THEME_KEY = 'gs-theme';

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.textContent = t === 'light' ? '☾' : '☀';
      btn.setAttribute('aria-label', t === 'light' ? 'Switch to dark mode' : 'Switch to light mode');
    }
  }

  var stored = null;
  try { stored = localStorage.getItem(THEME_KEY); } catch (e) { /* private mode */ }
  applyTheme(stored || 'dark');

  document.addEventListener('click', function (ev) {
    var t = ev.target.closest('#theme-toggle');
    if (!t) return;
    var next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    applyTheme(next);
    try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* ignore */ }
  });

  /* ---------- mobile nav ---------- */
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('#nav-toggle');
    var links = document.getElementById('nav-links');
    if (!links) return;
    if (btn) {
      links.classList.toggle('open');
      btn.setAttribute('aria-expanded', links.classList.contains('open') ? 'true' : 'false');
    } else if (!ev.target.closest('#nav-links')) {
      links.classList.remove('open');
    }
  });

  /* ---------- active nav link ---------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  Array.prototype.forEach.call(document.querySelectorAll('#nav-links a'), function (a) {
    var href = (a.getAttribute('href') || '').split('/').pop();
    if (href === here) a.classList.add('active');
  });

  /* ---------- scroll reveal ---------- */
  var revealables = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
  }

  /* ---------- animated counters ---------- */
  var counters = document.querySelectorAll('[data-count]');
  function runCounter(el) {
    var target = parseFloat(el.dataset.count);
    var suffix = el.dataset.suffix || '';
    if (reduce) { el.textContent = formatNum(target) + suffix; return; }
    var start = performance.now(), dur = 1100;
    (function step(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = formatNum(Math.round(target * eased)) + suffix;
      if (p < 1) requestAnimationFrame(step);
    })(start);
  }
  function formatNum(n) { return n.toLocaleString('en-US'); }

  if (counters.length) {
    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(counters, runCounter);
    } else {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { runCounter(e.target); cio.unobserve(e.target); }
        });
      }, { threshold: 0.4 });
      Array.prototype.forEach.call(counters, function (el) { cio.observe(el); });
    }
  }

  /* ---------- skills sidebar bars ---------- */
  function fillBars(scope) {
    Array.prototype.forEach.call(
      (scope || document).querySelectorAll('.skills-sidebar-bar-fill'), function (b) {
        b.style.width = (b.dataset.pct || 0) + '%';
      });
  }

  var sidebar = document.getElementById('skills-tabs');
  if (sidebar) {
    if (!('IntersectionObserver' in window)) fillBars();
    else {
      var bio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { fillBars(); bio.unobserve(e.target); }
        });
      }, { threshold: 0.2 });
      bio.observe(sidebar);
    }
  }

  /* ---------- skills tabs (sidebar + mobile) ---------- */
  function selectPanel(key) {
    Array.prototype.forEach.call(
      document.querySelectorAll('.skills-sidebar-tab, .skills-tab-mobile'), function (t) {
        var on = t.dataset.panel === key;
        t.classList.toggle('active', on);
        if (t.hasAttribute('aria-selected')) {
          t.setAttribute('aria-selected', on ? 'true' : 'false');
        }
      });
    Array.prototype.forEach.call(document.querySelectorAll('.skills-panel'), function (p) {
      p.classList.toggle('active', p.id === 'panel-' + key);
    });
  }

  ['skills-tabs', 'skills-tabs-mobile'].forEach(function (id) {
    var wrap = document.getElementById(id);
    if (!wrap) return;
    wrap.addEventListener('click', function (ev) {
      var b = ev.target.closest('.skills-sidebar-tab, .skills-tab-mobile');
      if (!b) return;
      selectPanel(b.dataset.panel);
    });
  });

  /* ---------- back to top ---------- */
  var top = document.getElementById('to-top');
  if (top) {
    window.addEventListener('scroll', function () {
      top.classList.toggle('show', window.scrollY > 500);
    }, { passive: true });
    top.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }

  /* ---------- footer year ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();

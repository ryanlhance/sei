/* =========================================================
   SEI Fit Map — renderer
   Pure renderer over data.json. No JD/resume content is
   hardcoded here; edit copy in data.json (or build_data.py).
   ========================================================= */
(function () {
  "use strict";

  var DATA = null;
  var PHRASES = {};            // id -> phrase segment {id,text,evidence}
  var activePhraseEl = null;   // currently-selected phrase button
  var lastFocused = null;      // element to restore focus to on close

  var el = {
    postingLink:  document.getElementById("posting-link"),
    jobTitle:     document.getElementById("job-title"),
    jobLocation:  document.getElementById("job-location-text"),
    kicker:       document.getElementById("candidate-kicker"),
    lede:         document.getElementById("candidate-lede"),
    stat:         document.getElementById("candidate-stat"),
    jdRoot:       document.getElementById("jd-root"),
    peek:         document.getElementById("peek"),
    peekPanel:    document.querySelector(".peek-panel"),
    peekScrim:    document.getElementById("peek-scrim"),
    peekClose:    document.getElementById("peek-close"),
    peekEmpty:    document.getElementById("peek-empty"),
    peekContent:  document.getElementById("peek-content"),
    peekHeading:  document.getElementById("peek-heading"),
    peekCards:    document.getElementById("peek-cards"),
    loadError:    document.getElementById("load-error")
  };

  // ---------- boot ----------
  fetch("./data.json")
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (data) {
      DATA = data;
      render();
      wireGlobalEvents();
      openFromHash();
    })
    .catch(showLoadError);

  // ---------- render ----------
  function render() {
    var job = DATA.job || {};

    if (job.tab_title) document.title = job.tab_title;

    if (job.url) {
      el.postingLink.href = job.url;
    } else {
      el.postingLink.style.display = "none";
    }

    el.jobTitle.textContent =
      (job.role || "") + (job.employment ? " (" + job.employment + ")" : "");
    el.jobLocation.textContent =
      (job.location || "") + (job.employment ? " · " + job.employment : "");
    el.kicker.textContent = job.candidate_kicker || (DATA.meta && DATA.meta.candidate) || "";
    el.lede.textContent = job.candidate_lede || "";

    renderProse();

    el.stat.textContent = job.candidate_stat || "";
  }

  function renderProse() {
    var blocks = DATA.jd_prose || [];
    var frag = document.createDocumentFragment();
    var ulBuffer = null; // collect consecutive <li> blocks into one <ul>

    function flushList() {
      if (ulBuffer) { frag.appendChild(ulBuffer); ulBuffer = null; }
    }

    blocks.forEach(function (block) {
      if (block.type === "li") {
        if (!ulBuffer) { ulBuffer = document.createElement("ul"); ulBuffer.className = "jd-ul"; }
        var li = document.createElement("li");
        li.className = "jd-li";
        appendSegments(li, block.segments || []);
        ulBuffer.appendChild(li);
        return;
      }

      flushList();

      if (block.type === "h2") {
        var h2 = document.createElement("h2");
        h2.className = "jd-h2";
        h2.textContent = block.text || "";
        frag.appendChild(h2);
      } else if (block.type === "h3") {
        var h3 = document.createElement("h3");
        h3.className = "jd-h3";
        h3.textContent = block.text || "";
        frag.appendChild(h3);
      } else { // paragraph
        var p = document.createElement("p");
        p.className = "jd-p";
        appendSegments(p, block.segments || []);
        frag.appendChild(p);
      }
    });
    flushList();

    el.jdRoot.innerHTML = "";
    el.jdRoot.appendChild(frag);
  }

  // Renders an array of segments (strings, {b}, or phrase objects) into a parent node.
  function appendSegments(parent, segments) {
    segments.forEach(function (seg) {
      if (typeof seg === "string") {
        parent.appendChild(document.createTextNode(seg));
      } else if (seg && seg.b) {
        var strong = document.createElement("span");
        strong.className = "jd-strong";
        strong.textContent = seg.b;
        parent.appendChild(strong);
      } else if (seg && seg.id) {
        PHRASES[seg.id] = seg;
        parent.appendChild(buildPhraseButton(seg));
      }
    });
  }

  function buildPhraseButton(phrase) {
    // A <span role="button"> (not a real <button>) so the phrase wraps
    // across lines like normal prose — buttons are atomic boxes and
    // break the text flow on narrow screens.
    var btn = document.createElement("span");
    btn.className = "phrase";
    btn.id = "phrase-" + phrase.id;
    btn.setAttribute("role", "button");
    btn.tabIndex = 0;
    btn.setAttribute("data-phrase-id", phrase.id);
    btn.setAttribute("aria-haspopup", "true");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", phrase.text + " — show the experience behind this.");
    btn.textContent = phrase.text;

    btn.addEventListener("click", function () { openPeek(phrase, btn, true); });
    btn.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
        e.preventDefault();
        openPeek(phrase, btn, true);
      }
    });
    return btn;
  }

  // ---------- peek ----------
  function openPeek(phrase, phraseEl, updateHash) {
    if (activePhraseEl && activePhraseEl !== phraseEl) {
      activePhraseEl.classList.remove("is-active");
      activePhraseEl.setAttribute("aria-expanded", "false");
    }
    activePhraseEl = phraseEl;
    if (phraseEl) {
      phraseEl.classList.add("is-active");
      phraseEl.setAttribute("aria-expanded", "true");
    }
    lastFocused = phraseEl;

    el.peekHeading.textContent = phrase.text;

    el.peekCards.innerHTML = "";
    (phrase.evidence || []).forEach(function (id) {
      var card = buildEvidenceCard(id);
      if (card) el.peekCards.appendChild(card);
    });

    el.peekEmpty.hidden = true;
    el.peekContent.hidden = false;
    el.peekClose.hidden = false;
    el.peek.classList.add("is-open");
    el.peekPanel.scrollTop = 0;

    if (updateHash) {
      if (history.replaceState) history.replaceState(null, "", "#" + phrase.id);
      else location.hash = phrase.id;
    }

    var focusTarget = el.peekClose && !el.peekClose.hidden ? el.peekClose : el.peekPanel;
    window.requestAnimationFrame(function () { focusTarget.focus(); });
  }

  function buildEvidenceCard(id) {
    var ev = DATA.evidence && DATA.evidence[id];
    if (!ev) return null;

    var card = document.createElement("article");
    card.className = "ev-card";

    var title = document.createElement("p");
    title.className = "ev-card-title";
    title.textContent = ev.title || "";
    card.appendChild(title);

    var text = document.createElement("p");
    text.className = "ev-card-text";
    text.textContent = ev.text || "";
    card.appendChild(text);

    if (ev.link) {
      var a = document.createElement("a");
      a.className = "ev-card-link";
      a.href = ev.link;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.innerHTML = "View case study <span aria-hidden=\"true\">↗</span>";
      card.appendChild(a);
    }
    return card;
  }

  function closePeek(restoreFocus) {
    el.peek.classList.remove("is-open");
    el.peekContent.hidden = true;
    el.peekClose.hidden = true;
    el.peekEmpty.hidden = false;

    if (activePhraseEl) {
      activePhraseEl.classList.remove("is-active");
      activePhraseEl.setAttribute("aria-expanded", "false");
    }
    activePhraseEl = null;

    if (history.replaceState) {
      history.replaceState(null, "", location.pathname + location.search);
    }
    if (restoreFocus && lastFocused && document.contains(lastFocused)) {
      lastFocused.focus();
    }
    lastFocused = null;
  }

  // ---------- events ----------
  function wireGlobalEvents() {
    el.peekClose.addEventListener("click", function () { closePeek(true); });
    el.peekScrim.addEventListener("click", function () { closePeek(true); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && el.peek.classList.contains("is-open")) closePeek(true);
    });
    window.addEventListener("hashchange", openFromHash);
  }

  function openFromHash() {
    var id = (location.hash || "").replace(/^#/, "");
    if (!id) return;
    var phrase = PHRASES[id];
    var btn = document.getElementById("phrase-" + id);
    if (phrase && btn) {
      btn.scrollIntoView({ behavior: "smooth", block: "center" });
      openPeek(phrase, btn, false);
    }
  }

  // ---------- error ----------
  function showLoadError(err) {
    el.loadError.hidden = false;
    el.loadError.innerHTML =
      "<strong>Couldn't load data.json.</strong><br>" +
      "This page reads its content from <code>data.json</code> via <code>fetch()</code>, " +
      "which the browser blocks over <code>file://</code>. " +
      "Serve the folder over http instead — e.g. run <code>python3 serve.py 8000</code> " +
      "in this folder and open <code>http://localhost:8000/</code>, or view it on GitHub Pages.<br><br>" +
      "<small>Details: " + (err && err.message ? err.message : err) + "</small>";
  }
})();

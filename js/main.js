/* Fluxoniks — main.js */
(function () {
  "use strict";

  // Mobile nav toggle
  var toggle = document.getElementById("navtoggle");
  var links = document.getElementById("navlinks");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Header shadow on scroll
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.classList.add("scrolled");
      else header.classList.remove("scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Reveal on scroll
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());

  // Contact form: simple client-side validation + faux submit
  var form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var status = document.getElementById("formStatus");
      var btn = form.querySelector("button[type=submit]");
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      // If Formspree action configured, this is replaced by real submit above;
      // otherwise show a graceful message with a mailto fallback.
      if (form.getAttribute("action") && form.getAttribute("action").indexOf("formspree.io") > -1) {
        form.submit();
        return;
      }
      setTimeout(function () {
        if (status) {
          status.textContent = "Thanks! To ensure your message reaches us, please also email hello@fluxoniks.com — or connect Formspree in the repo (see README).";
          status.style.display = "block";
        }
        if (btn) { btn.disabled = false; btn.textContent = "Request a quote"; }
        form.reset();
      }, 700);
    });
  }
})();
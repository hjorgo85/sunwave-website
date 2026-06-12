/* SunWave Switzerland — Main JS */

/* ── Hero carousel ── */
(function () {
  const slides = document.querySelectorAll('.hero__slide');
  const dots   = document.querySelectorAll('.hero__dot');
  if (!slides.length) return;

  let current = 0;
  let timer;

  function goTo(n) {
    slides[current].classList.remove('hero__slide--active');
    dots[current].classList.remove('hero__dot--active');
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('hero__slide--active');
    dots[current].classList.add('hero__dot--active');
  }

  function startTimer() {
    timer = setInterval(() => goTo(current + 1), 6000);
  }

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      clearInterval(timer);
      goTo(parseInt(dot.dataset.slide, 10));
      startTimer();
    });
  });

  startTimer();
})();

/* ── Sticky nav shadow ── */
window.addEventListener('scroll', () => {
  document.querySelector('.nav')?.classList.toggle('scrolled', window.scrollY > 20);
});

/* ── Mobile nav toggle ── */
(function () {
  const hamburger = document.querySelector('.nav__hamburger');
  const mobileMenu = document.querySelector('.nav__mobile');
  const mobileLang = document.querySelector('.mobile-lang');

  function closeMobileMenu() {
    mobileMenu?.classList.remove('open');
    mobileLang?.classList.remove('open');
    hamburger?.classList.remove('open');
  }

  hamburger?.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = mobileMenu?.classList.toggle('open');
    hamburger?.classList.toggle('open', isOpen);
  });

  // Close when any mobile link is tapped
  mobileMenu?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });

  // Close on outside tap
  document.addEventListener('click', (e) => {
    if (mobileMenu?.classList.contains('open') && !e.target.closest('.nav')) {
      closeMobileMenu();
    }
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMobileMenu();
  });
})();

/* ── Dropdown hover intent + keyboard/ARIA support ── */
document.querySelectorAll('.nav__drop').forEach(drop => {
  const btn = drop.querySelector('.nav__drop-btn');
  const menu = drop.querySelector('.nav__drop-menu');
  let closeTimer;

  function openMenu() {
    clearTimeout(closeTimer);
    menu.classList.add('open');
    btn?.setAttribute('aria-expanded', 'true');
  }
  function closeMenu() {
    menu.classList.remove('open');
    btn?.setAttribute('aria-expanded', 'false');
  }
  function scheduleClose() {
    closeTimer = setTimeout(closeMenu, 220);
  }

  drop.addEventListener('mouseenter', openMenu);
  drop.addEventListener('mouseleave', scheduleClose);
  menu.addEventListener('mouseenter', () => clearTimeout(closeTimer));
  menu.addEventListener('mouseleave', scheduleClose);

  btn?.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    menu.classList.contains('open') ? closeMenu() : openMenu();
  });

  btn?.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMenu();
      btn.focus();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      openMenu();
      menu.querySelector('a')?.focus();
    }
  });

  menu.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMenu();
      btn?.focus();
    }
  });
});

// Close nav dropdowns on outside click
document.addEventListener('click', (e) => {
  document.querySelectorAll('.nav__drop').forEach(drop => {
    if (!drop.contains(e.target)) {
      drop.querySelector('.nav__drop-menu')?.classList.remove('open');
      drop.querySelector('.nav__drop-btn')?.setAttribute('aria-expanded', 'false');
    }
  });
});

/* ── FAQ accordion ── */
document.querySelectorAll('.faq-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    // Close all
    document.querySelectorAll('.faq-trigger').forEach(b => b.setAttribute('aria-expanded', 'false'));
    // Open this one if it was closed
    if (!expanded) btn.setAttribute('aria-expanded', 'true');
  });
});

/* ── Product variant selector ── */
function initVariantSelector() {
  const btns = document.querySelectorAll('.variant-btn');
  const panel = document.getElementById('product-panel');
  const nameEl = document.getElementById('variant-name');

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (panel) {
        panel.className = 'hero__panel product-panel';
        panel.classList.add('variant--' + btn.dataset.variant);
      }
      if (nameEl) nameEl.textContent = btn.dataset.name;
    });
  });
}
initVariantSelector();

/* ── Smooth anchor scroll with nav offset ── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = 80;
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset, behavior: 'smooth' });
  });
});

/* ── Animate elements on scroll ── */
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.audience-card, .evidence-card, .feature-item, .stat-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

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

/* ── Savings calculator ── */
function swCalc() {
  const area     = parseFloat(document.getElementById('sw-area')?.value) || 80;
  const system   = document.getElementById('sw-system')?.value || 'gas';
  const elecRate = parseFloat(document.getElementById('sw-elec')?.value) || 0.29;
  const fuelRate = parseFloat(document.getElementById('sw-fuel')?.value) || 0.13;
  const insul    = document.getElementById('sw-insul')?.value || 'good';

  const energyIR = { excellent: 55, good: 71.21, average: 95, poor: 130 };
  const energyCurrent = { gas: 208.73, gas_condensing: 187.8, oil: 210, electric: 200 };
  const insulMult = { excellent: 0.77, good: 1.0, average: 1.33, poor: 1.83 };
  const fuelIsElec = system === 'electric';
  const boilerService = (system === 'gas' || system === 'gas_condensing' || system === 'oil') ? 400 : 0;

  const irEnergy   = energyIR[insul] * area;
  const curEnergy  = (energyCurrent[system] || 208.73) * insulMult[insul] * area;
  const irCost     = irEnergy * elecRate;
  const curCost    = curEnergy * (fuelIsElec ? elecRate : fuelRate) + boilerService;
  const saving     = curCost - irCost;
  const panels     = Math.ceil(area / 13);
  const capital    = panels * 490;
  const payback    = saving > 0 ? (capital / saving).toFixed(1) : '—';
  const co2Saving  = Math.round(curEnergy * (fuelIsElec ? 0.035 : 0.202) - irEnergy * 0.035);

  const fmtChf = n => 'CHF ' + Math.round(n).toLocaleString('de-CH');

  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  setEl('res-saving', saving > 0 ? fmtChf(saving) + '/yr' : '—');
  setEl('res-payback', saving > 0 ? payback + ' yrs' : '—');
  setEl('res-co2', co2Saving > 0 ? co2Saving + ' kg' : '—');

  const results = document.getElementById('calc-results');
  if (results) results.classList.add('show');
}

/* Bind system change to update fuel hint */
document.getElementById('sw-system')?.addEventListener('change', function() {
  const fuelInput = document.getElementById('sw-fuel');
  const fuelLabel = document.getElementById('sw-fuel-label');
  if (!fuelInput) return;
  const map = { gas: '0.13', gas_condensing: '0.13', oil: '0.10', electric: '—' };
  const labelMap = { gas: 'Gas price (CHF/kWh)', gas_condensing: 'Gas price (CHF/kWh)', oil: 'Oil price (CHF/kWh)', electric: 'Same as electricity' };
  fuelInput.value = map[this.value] || '0.12';
  if (fuelLabel) fuelLabel.textContent = labelMap[this.value] || 'Fuel price (CHF/kWh)';
  swCalc();
});

/* Auto-run calculator on page load */
if (document.getElementById('sw-area')) swCalc();

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

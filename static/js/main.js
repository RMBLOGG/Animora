// Mobile menu
const menuBtn = document.getElementById('menuBtn');
const mobileNav = document.getElementById('mobileNav');
if (menuBtn && mobileNav) {
  menuBtn.addEventListener('click', () => mobileNav.classList.toggle('open'));
}

// Alphabet filter
document.querySelectorAll('.alpha-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.alpha-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const target = btn.dataset.letter;
    document.querySelectorAll('.letter-group').forEach(g => {
      g.style.display = (target === 'all' || g.dataset.letter === target) ? '' : 'none';
    });
  });
});

// Image error fallback
document.querySelectorAll('img').forEach(img => {
  img.addEventListener('error', function () {
    this.style.display = 'none';
    const ph = this.parentElement.querySelector('.thumb-ph,.detail-hero-ph,.rekom-card-ph');
    if (ph) ph.style.display = 'flex';
  });
});

// Scroll to top
const scrollBtn = document.getElementById('scrollTop');
if (scrollBtn) {
  window.addEventListener('scroll', () => scrollBtn.classList.toggle('show', window.scrollY > 300));
  scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

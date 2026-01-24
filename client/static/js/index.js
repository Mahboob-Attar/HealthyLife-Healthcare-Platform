// Popup Triggers
const aboutLink = document.querySelector('a[href="#about"]');
if (aboutLink) {
  aboutLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('aboutPopup')?.classList.add('active');
  });
}

const faqLink = document.querySelector('a[href="#faq"]');
if (faqLink) {
  faqLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('faqPopup')?.classList.add('active');
  });
}

const supportLink = document.querySelector('a[href="#contact"]');
if (supportLink) {
  supportLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('supportPopup')?.classList.add('active');
  });
}

// Close Popups
document.querySelectorAll('.close-info').forEach(btn => {
  btn.addEventListener('click', () => {
    const popupId = btn.getAttribute('data-close');
    document.getElementById(popupId)?.classList.remove('active');
  });
});

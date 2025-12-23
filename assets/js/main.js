document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const themeToggle = document.getElementById('theme-toggle');
    const langToggle = document.getElementById('lang-toggle');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const html = document.documentElement;
    const body = document.body;

    // State
    let currentTheme = localStorage.getItem('theme') || 'light';
    let currentLang = localStorage.getItem('lang') || 'ar';

    // Initialize
    applyTheme(currentTheme);
    applyLang(currentLang);

    // Event Listeners
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            currentTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(currentTheme);
        });
    }

    if (langToggle) {
        langToggle.addEventListener('click', () => {
            currentLang = currentLang === 'ar' ? 'en' : 'ar';
            applyLang(currentLang);
        });
    }

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Functions
    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateIcons();
    }

    function applyLang(lang) {
        html.setAttribute('lang', lang);
        html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
        body.classList.remove('lang-ar', 'lang-en');
        body.classList.add(lang === 'en' ? 'lang-en' : 'lang-ar');
        localStorage.setItem('lang', lang);
        
        // Update button text if needed
        if (langToggle) {
            langToggle.textContent = lang === 'ar' ? 'English' : 'عربي';
        }
    }

    function updateIcons() {
        if (themeToggle) {
            themeToggle.textContent = currentTheme === 'light' ? '🌙' : '☀️';
        }
    }
});

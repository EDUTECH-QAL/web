document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const themeToggle = document.getElementById('theme-toggle');
    const langToggle = document.getElementById('lang-toggle');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const html = document.documentElement;
    const body = document.body;
    const overlay = document.createElement('div');
    overlay.className = 'nav-overlay';
    document.body.appendChild(overlay);

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
            const isOpen = navMenu.classList.contains('active');
            overlay.classList.toggle('active', isOpen);
            body.style.overflow = isOpen ? 'hidden' : '';
        });
    }
    overlay.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
        overlay.classList.remove('active');
        body.style.overflow = '';
    });
    // Close menu when clicking a link (mobile)
    if (navMenu) {
        navMenu.addEventListener('click', (e) => {
            const target = e.target.closest('a');
            const dropdownToggle = e.target.closest('.dropdown-toggle');
            
            // If it's a dropdown toggle on mobile, don't close the menu
            if (dropdownToggle && window.innerWidth <= 768) {
                return;
            }

            if (target && navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                overlay.classList.remove('active');
                body.style.overflow = '';
            }
        });
    }

    // Dropdown Logic for Mobile
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        if (toggle) {
            toggle.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Close other dropdowns if any (optional, but good for focus)
                    dropdowns.forEach(other => {
                        if (other !== dropdown) other.classList.remove('active');
                    });
                    
                    dropdown.classList.toggle('active');
                }
            });
        }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            overlay.classList.remove('active');
            body.style.overflow = '';
        }
    });

    // Functions
    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateIcons();
    }

    function applyLang(lang) {
        html.setAttribute('lang', lang);
        html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
        localStorage.setItem('lang', lang);
        
        document.querySelectorAll('.lang-ar').forEach(el => {
            el.style.display = lang === 'ar' ? '' : 'none';
        });
        document.querySelectorAll('.lang-en').forEach(el => {
            el.style.display = lang === 'en' ? '' : 'none';
        });

        if (langToggle) {
            langToggle.textContent = lang === 'ar' ? 'English' : 'عربي';
        }
        document.querySelectorAll('.social-links a').forEach(a => {
            const ar = a.getAttribute('data-label-ar');
            const en = a.getAttribute('data-label-en');
            if (ar || en) {
                const label = lang === 'ar' ? (ar || en || '') : (en || ar || '');
                a.setAttribute('aria-label', label);
                a.setAttribute('title', label);
            }
        });
    }

    function updateIcons() {
        if (themeToggle) {
            themeToggle.textContent = currentTheme === 'light' ? '🌙' : '☀️';
        }
    }

    // Dynamic Year
    const yearElements = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    yearElements.forEach(el => {
        el.textContent = currentYear;
    });
});

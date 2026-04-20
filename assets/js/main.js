document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

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
            body.classList.toggle('menu-open', isOpen);

            // Staggered animation for links
            if (isOpen) {
                const links = navMenu.querySelectorAll('.nav-link, .dropdown');
                links.forEach((link, index) => {
                    link.style.opacity = '0';
                    link.style.transform = 'translateX(' + (currentLang === 'ar' ? '20px' : '-20px') + ')';
                    link.style.transition = 'all 0.4s ease ' + (0.1 + index * 0.05) + 's';
                    
                    setTimeout(() => {
                        link.style.opacity = '1';
                        link.style.transform = 'translateX(0)';
                    }, 50);
                });
            } else {
                // Reset styles when closing
                const links = navMenu.querySelectorAll('.nav-link, .dropdown');
                links.forEach(link => {
                    link.style.transition = '';
                    link.style.opacity = '';
                    link.style.transform = '';
                });
            }
        });
    }
    overlay.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
        overlay.classList.remove('active');
        body.classList.remove('menu-open');
    });
    // Close menu when clicking a link (mobile)
    if (navMenu) {
        navMenu.addEventListener('click', (e) => {
            const target = e.target.closest('a');
            const dropdownToggle = e.target.closest('.dropdown-toggle');
            
            // If it's a dropdown toggle on mobile, don't close the menu, toggle dropdown instead
            if (dropdownToggle && window.innerWidth <= 768) {
                e.preventDefault();
                const dropdown = dropdownToggle.closest('.dropdown');
                dropdown.classList.toggle('active');
                return;
            }

            if (target && navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                overlay.classList.remove('active');
                body.classList.remove('menu-open');
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
            body.classList.remove('menu-open');
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

    // Scroll to Top logic
    const scrollToTop = document.getElementById('scroll-to-top');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollToTop.classList.add('active');
        } else {
            scrollToTop.classList.remove('active');
        }
    });
    scrollToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Decision Search & Category Filter
    const decisionSearch = document.getElementById('decision-search');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.decision-card');

    if (decisionSearch || filterBtns.length > 0) {
        const filterDecisions = () => {
            const searchTerm = decisionSearch ? decisionSearch.value.toLowerCase().trim() : '';
            const activeFilter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';

            cards.forEach(card => {
                const title = card.querySelector('.decision-title').textContent.toLowerCase();
                const summary = card.querySelector('.decision-summary').textContent.toLowerCase();
                const subject = card.querySelector('.decision-subject')?.textContent.toLowerCase() || '';
                const category = card.dataset.category;

                const matchesSearch = title.includes(searchTerm) || summary.includes(searchTerm) || subject.includes(searchTerm);
                const matchesCategory = activeFilter === 'all' || category === activeFilter;

                if (matchesSearch && matchesCategory) {
                    card.style.display = '';
                    setTimeout(() => card.classList.remove('hidden'), 10);
                } else {
                    card.classList.add('hidden');
                    setTimeout(() => {
                        if (card.classList.contains('hidden')) card.style.display = 'none';
                    }, 400);
                }
            });
        };

        if (decisionSearch) {
            decisionSearch.addEventListener('input', filterDecisions);
        }

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                filterDecisions();
            });
        });
    }
});

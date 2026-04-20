// Initialize GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Initialize AOS (Animate On Scroll)
// We use AOS for most scroll-reveal animations as it's more stable for visibility
AOS.init({
    duration: 600,
    easing: 'ease-out',
    once: true,
    offset: 50,
});

document.addEventListener('DOMContentLoaded', () => {
    // Only run GSAP if elements are present and visible
    initHeroAnimations();
    initHoverAnimations();
    // ScrollTrigger for specific complex animations only
    initScrollTriggers();
});

// 1. Hero Section Animations (Faster and more reliable)
function initHeroAnimations() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    // Set initial state to visible in case animation fails
    gsap.set(['.hero-logo', '.hero-title', '.hero-subtitle', '.hero-actions .btn'], { opacity: 1 });

    const tl = gsap.timeline({ 
        defaults: { ease: "power2.out", duration: 0.6 } 
    });

    tl.from('.hero-logo', {
        scale: 0.9,
        opacity: 0,
        duration: 0.8
    })
    .from('.hero-title', {
        y: 20,
        opacity: 0
    }, "-=0.4")
    .from('.hero-subtitle', {
        y: 10,
        opacity: 0
    }, "-=0.4")
    .from('.hero-actions .btn', {
        y: 10,
        opacity: 0,
        stagger: 0.1
    }, "-=0.4");
}

// 2. Specific Scroll Triggers (For things AOS can't do)
function initScrollTriggers() {
    // Reveal header on scroll up / hide on scroll down (optional enhancement)
    // For now, just ensure content revealed by AOS is not interfered with
}

// 3. Interactive Hover Effects (Lightweight)
function initHoverAnimations() {
    // Buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-outline, .btn-news, .btn-icon, .scroll-to-top');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, { scale: 1.03, duration: 0.2, ease: "power1.out" });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { scale: 1, duration: 0.2, ease: "power1.in" });
        });
    });

    // Cards
    const cards = document.querySelectorAll('.modern-card, .news-card, .team-card-modern, .strategy-card, .decision-card, .structure-item');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -5,
                duration: 0.3,
                ease: "power1.out"
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                duration: 0.3,
                ease: "power1.in"
            });
        });
    });
}

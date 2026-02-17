// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 800,
    easing: 'ease-out-cubic',
    once: true,
    offset: 50,
    delay: 50,
});

document.addEventListener('DOMContentLoaded', () => {
    initHeroAnimations();
    initHoverAnimations();
});

// 1. Hero Section Animations (Using GSAP for complex entry)
function initHeroAnimations() {
    const heroContent = document.querySelector('.hero-modern .container, .hero .container');
    if (!heroContent) return;

    const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 1 } });

    tl.from(heroContent.querySelectorAll('h1, .hero-title'), {
        y: 40,
        opacity: 0,
        delay: 0.1
    })
    .from(heroContent.querySelectorAll('p, .hero-subtitle'), {
        y: 20,
        opacity: 0
    }, "-=0.8")
    .from(heroContent.querySelectorAll('.hero-actions, .btn'), {
        y: 15,
        opacity: 0,
        stagger: 0.1
    }, "-=0.8")
    .from(heroContent.querySelectorAll('.hero-image, .hero-logo'), {
        scale: 0.9,
        opacity: 0,
        duration: 1,
        ease: "back.out(1.2)"
    }, "-=1");
}

// 2. Interactive Animations (Using GSAP)
function initHoverAnimations() {
    // Subtle button interaction
    const buttons = document.querySelectorAll('.btn-primary, .btn-outline');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, { scale: 1.03, duration: 0.2 });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { scale: 1, duration: 0.2 });
        });
    });

    // Card interactive tilt
    const modernCards = document.querySelectorAll('.modern-card, .team-card-modern, .news-card');
    modernCards.forEach(card => {
        const icon = card.querySelector('.icon-box, .team-img-wrapper-modern, .news-image-wrapper');
        if (icon) {
            card.addEventListener('mouseenter', () => {
                gsap.to(icon, { y: -5, duration: 0.3, ease: "power2.out" });
            });
            card.addEventListener('mouseleave', () => {
                gsap.to(icon, { y: 0, duration: 0.3, ease: "power2.in" });
            });
        }
    });
}

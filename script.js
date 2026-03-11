// Mobile menu toggle
const toggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (toggle) {
    toggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        toggle.classList.toggle('active');
    });
}

// Close mobile menu on link click
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        toggle.classList.remove('active');
    });
});

// Header scroll effect
const header = document.querySelector('.header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.style.background = 'rgba(17, 17, 17, 0.98)';
    } else {
        header.style.background = '';
    }
});

// Contact form handler (demo)
function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const name = form.querySelector('#name').value;
    
    // In production, this would submit to a backend
    alert(`Thanks ${name}! This is a demo site. In the live version, your request would be sent directly to Arch Electric. For now, please call (831) 359-8747.`);
    form.reset();
}

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply to service cards and testimonials
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.service-card, .testimonial-card, .why-item, .value-card, .contact-info-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

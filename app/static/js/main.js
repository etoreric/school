// main.js - Frontend client-side script

document.addEventListener('DOMContentLoaded', () => {
    // 1. Scroll effect on transparent Navbar
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 2. Countdown Timer for Events page (if selector exists)
    const countdownElements = document.querySelectorAll('[data-countdown]');
    countdownElements.forEach(elem => {
        const datetimeStr = elem.getAttribute('data-countdown');
        if (!datetimeStr) return;
        
        const targetDate = new Date(datetimeStr).getTime();
        
        const timer = setInterval(() => {
            const now = new Date().getTime();
            const distance = targetDate - now;
            
            if (distance < 0) {
                clearInterval(timer);
                elem.innerHTML = "Event has started";
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            elem.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);
    });

    // 2.5 Scroll reveal animation for main website sections and cards
    const revealTargets = document.querySelectorAll('section, .hero-image-card, .hover-card, .news-card, .testimonial-card, .premium-card, .post-card-img, .gallery-thumb');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });
    revealTargets.forEach(el => {
        el.classList.add('reveal-item');
        revealObserver.observe(el);
    });

    // 3. Simple Image/Video/Audio Previewer / Gallery lightbox Modal helper
    const galleryItems = document.querySelectorAll('.gallery-thumb');

    // Touch support: tap gallery overlay to reveal it first, second tap opens lightbox
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
    if (isTouchDevice) {
        galleryItems.forEach(item => {
            item.addEventListener('touchstart', (e) => {
                const alreadyActive = item.classList.contains('touch-active');
                // Dismiss any other active overlays
                document.querySelectorAll('.gallery-thumb.touch-active').forEach(el => {
                    el.classList.remove('touch-active');
                    el.style.opacity = '';
                });
                if (!alreadyActive) {
                    e.preventDefault();
                    item.classList.add('touch-active');
                    item.style.opacity = '1';
                }
                // If it was already active, let the click event proceed naturally (open lightbox)
            }, { passive: false });
        });
    }

    galleryItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // On touch: only proceed if overlay is already revealed
            if (isTouchDevice && !item.classList.contains('touch-active')) {
                e.preventDefault();
                return;
            }
            e.preventDefault();
            const src = item.getAttribute('href');
            const caption = item.getAttribute('data-caption') || '';

            // Build temporary Modal container
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(11, 15, 25, 0.9)';
            modal.style.display = 'flex';
            modal.style.flexDirection = 'column';
            modal.style.alignItems = 'center';
            modal.style.justify = 'center';
            modal.style.zIndex = '9999';
            modal.style.cursor = 'zoom-out';

            const lower = src.toLowerCase();
            let mediaEl;

            if (lower.endsWith('.mp4') || lower.endsWith('.mov') || lower.endsWith('.avi') || lower.endsWith('.webm')) {
                // Create a responsive 16:9 wrapper similar to YouTube player size
                const wrapper = document.createElement('div');
                wrapper.style.width = 'min(960px, 90vw)';
                wrapper.style.aspectRatio = '16/9';
                wrapper.style.maxHeight = '85vh';
                wrapper.style.borderRadius = '12px';
                wrapper.style.overflow = 'hidden';
                wrapper.style.background = '#000';

                mediaEl = document.createElement('video');
                mediaEl.src = src;
                mediaEl.controls = true;
                mediaEl.autoplay = true;
                mediaEl.playsInline = true;
                mediaEl.style.width = '100%';
                mediaEl.style.height = '100%';
                mediaEl.style.objectFit = 'contain';

                wrapper.appendChild(mediaEl);
                mediaEl.wrapper = wrapper; // attach for fullscreen handling
                mediaEl = wrapper;

            } else if (lower.endsWith('.mp3') || lower.endsWith('.wav') || lower.endsWith('.ogg') || lower.endsWith('.m4a') || lower.endsWith('.aac')) {
                mediaEl = document.createElement('audio');
                mediaEl.src = src;
                mediaEl.controls = true;
                mediaEl.autoplay = false;
                mediaEl.style.width = '90%';
            } else {
                mediaEl = document.createElement('img');
                mediaEl.src = src;
                mediaEl.style.maxWidth = '90%';
                mediaEl.style.maxHeight = '80%';
                mediaEl.style.borderRadius = '16px';
                mediaEl.style.boxShadow = '0 10px 40px rgba(0,0,0,0.5)';
                mediaEl.style.cursor = 'default';
            }

            const capText = document.createElement('p');
            capText.innerText = caption;
            capText.style.color = '#ffffff';
            capText.style.marginTop = '16px';
            capText.style.fontFamily = "'Outfit', sans-serif";
            capText.style.fontSize = '1.0rem';

            modal.appendChild(mediaEl);
            if (caption) modal.appendChild(capText);

            // Close modal on background click
            modal.addEventListener('click', (ev) => {
                // allow clicks inside media element without closing
                if (ev.target === modal) {
                    modal.remove();
                    // Reset touch-active overlay state
                    if (isTouchDevice) {
                        item.classList.remove('touch-active');
                        item.style.opacity = '';
                    }
                }
            });

            document.body.appendChild(modal);

            // Make video enter fullscreen on double-click if supported
            const videoElement = modal.querySelector('video') || (mediaEl.tagName === 'VIDEO' ? mediaEl : null);
            if (videoElement) {
                const fsTarget = videoElement.wrapper || videoElement; // wrapper when used
                fsTarget.addEventListener('dblclick', () => {
                    if (fsTarget.requestFullscreen) fsTarget.requestFullscreen();
                    else if (fsTarget.webkitRequestFullscreen) fsTarget.webkitRequestFullscreen();
                });
            }
        });
    });
});

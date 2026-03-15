/**
 * gallery.js - Masonry gallery and lightbox with lazy loading
 */

document.addEventListener('DOMContentLoaded', () => {
    // Lightbox Functionality
    const lightbox = document.getElementById('gallery-lightbox');
    if (!lightbox) return;

    const lightboxImg = lightbox.querySelector('.lightbox-image');
    const lightboxClose = lightbox.querySelector('.lightbox-close');
    const lightboxPrev = lightbox.querySelector('.lightbox-prev');
    const lightboxNext = lightbox.querySelector('.lightbox-next');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const lightboxDownload = lightbox.querySelector('.lightbox-download');

    // Get all gallery images that can be viewed
    const galleryItems = Array.from(document.querySelectorAll('.gallery-item img'));
    let currentIndex = 0;

    function openLightbox(index) {
        if (index < 0 || index >= galleryItems.length) return;
        currentIndex = index;
        const img = galleryItems[currentIndex];

        lightboxImg.src = img.src;
        lightboxCaption.textContent = img.alt || 'Evidence Image';
        lightboxDownload.href = img.src;

        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    function showNext() {
        openLightbox((currentIndex + 1) % galleryItems.length);
    }

    function showPrev() {
        openLightbox((currentIndex - 1 + galleryItems.length) % galleryItems.length);
    }

    // Attach click listeners to gallery images
    galleryItems.forEach((img, index) => {
        // Prevent default drag
        img.addEventListener('dragstart', e => e.preventDefault());

        img.parentElement.addEventListener('click', (e) => {
            e.preventDefault();
            openLightbox(index);
        });
    });

    // Lightbox Controls
    lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxNext) lightboxNext.addEventListener('click', showNext);
    if (lightboxPrev) lightboxPrev.addEventListener('click', showPrev);

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') showNext();
        if (e.key === 'ArrowLeft') showPrev();
    });

    // Lazy Loading via IntersectionObserver (if not natively supported or for custom effects)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    // Trigger fade in or basic load
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        galleryItems.forEach(img => imageObserver.observe(img));
    }
});

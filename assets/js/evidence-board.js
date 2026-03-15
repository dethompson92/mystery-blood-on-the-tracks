/**
 * evidence-board.js - Handle evidence tab switching and modal interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Modal evidence viewer
    const modal = document.getElementById('evidence-modal');
    if (modal) {
        const modalIframe = modal.querySelector('iframe');
        const modalClose = modal.querySelector('.modal-close');
        const evidenceCards = document.querySelectorAll('.evidence-card a');

        evidenceCards.forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                // Check if locked
                if (card.closest('.locked')) {
                    alert('This evidence is sealed. Unlock the tier first.');
                    return;
                }
                const url = card.getAttribute('href');
                modalIframe.src = url;
                modal.classList.add('active');
                document.body.style.overflow = 'hidden'; // prevent background scrolling
            });
        });

        modalClose.addEventListener('click', () => {
            modal.classList.remove('active');
            modalIframe.src = 'about:blank';
            document.body.style.overflow = '';
        });

        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modalClose.click();
            }
        });
    }
});

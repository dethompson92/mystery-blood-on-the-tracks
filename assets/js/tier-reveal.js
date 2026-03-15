/**
 * tier-reveal.js - Handles unlocking evidence tiers via localStorage
 */

const TierReveal = {
    config: {
        mystery: '',
        tier2Code: '',
        tier3Code: '',
        solutionsCode: '' // Only for GM if applicable here
    },

    init: function (config) {
        this.config = Object.assign(this.config, config);
        this.checkTiers();
        this.setupListeners();
    },

    getStorageKey: function (tier) {
        return `mmc_unlocked_${this.config.mystery}_${tier}`;
    },

    unlockTier: function (tier, codeEntered) {
        let correctCode = '';
        if (tier === 2) correctCode = this.config.tier2Code;
        if (tier === 3) correctCode = this.config.tier3Code;

        if (codeEntered.toUpperCase().trim() === correctCode.toUpperCase().trim()) {
            localStorage.setItem(this.getStorageKey(tier), 'true');
            this.checkTiers();

            // Dispatch custom event for other scripts
            const event = new CustomEvent('tierUnlocked', { detail: { tier } });
            document.dispatchEvent(event);
            return true;
        }
        return false;
    },

    isTierUnlocked: function (tier) {
        if (tier === 1) return true; // Tier 1 always unlocked
        return localStorage.getItem(this.getStorageKey(tier)) === 'true';
    },

    checkTiers: function () {
        // Reveal UI elements based on tier status
        for (let i = 2; i <= 3; i++) {
            const tierElements = document.querySelectorAll(`.needs-tier-${i}`);
            const lockForms = document.querySelectorAll(`.tier-${i}-lock-form`);

            if (this.isTierUnlocked(i)) {
                tierElements.forEach(el => {
                    el.classList.remove('locked', 'hidden');
                    el.classList.add('unlocked');
                });
                lockForms.forEach(form => {
                    form.style.display = 'none';
                });
            } else {
                tierElements.forEach(el => {
                    el.classList.add('locked');
                    // Don't hide completely, let CSS handle the locked state visualization (e.g. padlock blur)
                });
            }
        }
    },

    setupListeners: function () {
        // Forms to submit unlock code
        const unlockForms = document.querySelectorAll('.tier-unlock-form');

        unlockForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const tier = parseInt(form.dataset.tier);
                const input = form.querySelector('.tier-code-input');
                const errorMsg = form.querySelector('.error-message');

                if (input && this.unlockTier(tier, input.value)) {
                    input.value = '';
                    if (errorMsg) errorMsg.textContent = '';
                    // Optional success alert or visual feedback
                } else {
                    if (errorMsg) errorMsg.textContent = 'Invalid passcode.';
                    input.classList.add('error');
                    setTimeout(() => input.classList.remove('error'), 500);
                }
            });
        });
    }
};

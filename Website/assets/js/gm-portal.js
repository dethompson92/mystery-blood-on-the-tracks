/**
 * gm-portal.js - Basic password gating using sessionStorage and Web Crypto API
 */

const GMPortal = {
    // Hardcoded hash for 'MURDER-COLLECTIVE-GM' (for extra obfuscation compared to plaintext)
    // Actually, to keep it simple and vanlla per prompt, we will use a basic string check or basic SHA-256
    // Since it's a static site, anything is theoretically viewable in source. We will do SHA-256.

    // Hash for MURDER-COLLECTIVE-GM
    targetHash: '43c68383eaba4ec334f593db94eb84eec020facceb3be48cd0e104618e87493a',

    init: function () {
        this.checkAuth();
        this.setupLoginForm();
        // Disable console logs in portal if strictly requested
        if (window.location.pathname.includes('gm-portal')) {
            // console.log = function() {};
            // console.warn = function() {};
        }
    },

    async hashPassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
    },

    async authenticate(password) {
        const hash = await this.hashPassword(password.trim());
        if (hash === this.targetHash) {
            sessionStorage.setItem('gm_auth', 'true');
            return true;
        }
        return false;
    },

    checkAuth: function () {
        const isAuth = sessionStorage.getItem('gm_auth') === 'true';
        const loginContainer = document.getElementById('gm-login-container');
        const contentContainer = document.getElementById('gm-content-container');

        if (!loginContainer || !contentContainer) return; // Not on the portal page

        if (isAuth) {
            loginContainer.style.display = 'none';
            contentContainer.style.display = 'block';
        } else {
            loginContainer.style.display = 'block';
            contentContainer.style.display = 'none';
        }
    },

    setupLoginForm: function () {
        const form = document.getElementById('gm-login-form');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = document.getElementById('gm-password');
            const errorMsg = document.getElementById('gm-error');
            const btn = form.querySelector('button');

            btn.disabled = true;
            btn.textContent = 'Verifying...';

            const isValid = await this.authenticate(input.value);

            if (isValid) {
                this.checkAuth();
            } else {
                errorMsg.textContent = 'Invalid Access Code. Access Denied.';
                input.value = '';
                input.focus();

                // Shake effect or simple color change
                input.style.borderColor = 'red';
                setTimeout(() => input.style.borderColor = '', 1500);
            }

            btn.disabled = false;
            btn.textContent = 'Access Portal';
        });
    },

    // Used in individual mystery solution pages
    checkSolutionAuth: function (mysteryCode, correctCode) {
        // e.g. VICTOR-SOTO-0847
        // Let's use sessionStorage for solution pages
        const sessionKey = `solution_auth_${mysteryCode}`;

        // If coming from GM portal, we might bypass, or just check standard session
        if (sessionStorage.getItem(sessionKey) === 'true') {
            document.getElementById('solution-content').style.display = 'block';
            const lockSection = document.getElementById('solution-lock');
            if (lockSection) lockSection.style.display = 'none';
        }
    },

    authSolution: function (mysteryCode, correctCode, attemptedCode) {
        if (attemptedCode.toUpperCase().trim() === correctCode.toUpperCase().trim()) {
            sessionStorage.setItem(`solution_auth_${mysteryCode}`, 'true');
            this.checkSolutionAuth();
            return true;
        }
        return false;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    GMPortal.init();
});

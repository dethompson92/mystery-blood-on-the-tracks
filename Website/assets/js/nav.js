/**
 * nav.js - Navigation responsive behavior
 */

document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('active');
    });
  }

  // Highlight active link
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') && currentPath.includes(link.getAttribute('href').replace('../', ''))) {
      // Very basic active state matching
      if(link.getAttribute('href') !== '/' && link.getAttribute('href') !== 'index.html') {
          link.classList.add('active');
      }
    }
  });
  
  // Custom exact match for home
  if(currentPath === '/' || currentPath === '/index.html') {
      document.querySelectorAll('.nav-link[href="index.html"], .nav-link[href="/"]').forEach(link => {
          link.classList.add('active');
      });
  }
});

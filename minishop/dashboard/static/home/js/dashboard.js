// Immediately execute script when loaded
(function() {
    'use strict';
    
    // Initialize variables
    let isDarkMode = false;
    let isSidebarCollapsed = false;
    
    // DOM elements
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    const mobileSidebarToggleBtn = document.getElementById('mobile-sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const preloader = document.getElementById('preloader');
    
    // Hide preloader when page is loaded
    window.addEventListener('load', function() {
        preloader.classList.add('hidden');
        setTimeout(() => {
            preloader.style.display = 'none';
        }, 500);
    });
    
    // Apply saved theme
    function applySavedTheme() {
        if (isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggleBtn.querySelector('i').classList.remove('fa-moon');
            themeToggleBtn.querySelector('i').classList.add('fa-sun');
        } else {
            document.documentElement.removeAttribute('data-theme');
            themeToggleBtn.querySelector('i').classList.remove('fa-sun');
            themeToggleBtn.querySelector('i').classList.add('fa-moon');
        }
    }
    
    // Apply saved sidebar state
    function applySavedSidebarState() {
        if (isSidebarCollapsed) {
            sidebar.classList.add('sidebar-collapsed');
            content.classList.add('content-wrapper-expanded');
        } else {
            sidebar.classList.remove('sidebar-collapsed');
            content.classList.remove('content-wrapper-expanded');
        }
    }
    
    // Initial state - ensure sidebar is open by default on desktop
    function setInitialState() {
        // Apply saved theme
        applySavedTheme();
        
        // Apply saved sidebar state
        applySavedSidebarState();
        
        // Make sure sidebar is shown by default on larger screens
        if (window.innerWidth > 992) {
            sidebar.style.transform = 'translateX(0)';
        } else {
            // On mobile, ensure sidebar is hidden initially
            sidebar.classList.remove('show');
        }
    }
    
    // Function to toggle theme
    function toggleTheme() {
        isDarkMode = !isDarkMode;
        
        applySavedTheme();
    }
    
    // Function to toggle sidebar
    function toggleSidebar() {
        isSidebarCollapsed = !isSidebarCollapsed;
        
        applySavedSidebarState();
    }
    
    // Mobile sidebar toggle
    function toggleMobileSidebar(e) {
        e.stopPropagation();
        sidebar.classList.toggle('show');
    }
    
    // Close mobile sidebar when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 992 && 
            sidebar.classList.contains('show') && 
            !sidebar.contains(e.target) && 
            e.target !== mobileSidebarToggleBtn) {
            sidebar.classList.remove('show');
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            // Show sidebar on desktop
            sidebar.style.transform = 'translateX(0)';
            
            // If mobile sidebar was open, close it
            if (sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        } else {
            // Hide sidebar on mobile unless it's explicitly shown
            if (!sidebar.classList.contains('show')) {
                sidebar.style.transform = '';
            }
        }
    });
    
    // Highlight active link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('show');
            }
            
            // Remove active class from all links
            document.querySelectorAll('.nav-link').forEach(navLink => {
                navLink.classList.remove('active');
            });
            
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
    
    // Add event listeners
    themeToggleBtn.addEventListener('click', toggleTheme);
    sidebarToggleBtn.addEventListener('click', toggleSidebar);
    mobileSidebarToggleBtn.addEventListener('click', toggleMobileSidebar);
    
    // Set initial state when the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', setInitialState);
    
    // Call immediately as well to ensure proper state
    setInitialState();

    // Check and apply saved theme from localStorage
    document.addEventListener('DOMContentLoaded', function () {
        const themeToggle = document.getElementById('theme-toggle');
        const htmlElement = document.documentElement;
        const icon = themeToggle.querySelector('i');

        // Load saved theme from localStorage
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            htmlElement.setAttribute('data-theme', savedTheme);
            icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }

        // Toggle theme on click
        themeToggle.addEventListener('click', function () {
            const isDark = htmlElement.getAttribute('data-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        });
    });
})();

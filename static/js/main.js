document.addEventListener('DOMContentLoaded', function() {
    // Navbar Toggle
    const hamburger = document.querySelector('.navbar-toggler');
    const navLinks = document.querySelector('.navbar-collapse');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('show');
        });

        const navbarLinks = document.querySelectorAll('.nav-links a');
        const footerLinks = document.querySelectorAll('footer .footer-links a');
        const allLinks = [...navbarLinks, ...footerLinks];

        allLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    console.log('Rolando para elemento:', targetElement);

                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - navbarHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    if (navLinks.classList.contains('show')) {
                        navLinks.classList.remove('show');
                    }
                } else {
                    console.error('Elemento alvo não encontrado:', targetId);
                }
            });
        });
    }

    // Back to Top Button
    const backToTopButton = document.getElementById('back-to-top');

    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.style.display = 'none';
            }
        });

        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Team Tabs
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;

            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Image Carousel
    const carouselContainer = document.querySelector('.carousel-container');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    const slides = document.querySelectorAll('.carousel-slide');
    let currentIndex = 0;

    function updateCarousel() {
        if (carouselContainer) {
            carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
        }
    }

    if (prevButton && nextButton && slides.length > 0 && carouselContainer) {
        prevButton.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateCarousel();
        });

        nextButton.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % slides.length;
            updateCarousel();
        });
    }
});
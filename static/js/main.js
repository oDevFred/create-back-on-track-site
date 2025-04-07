document.addEventListener('DOMContentLoaded', function() {
    // Navbar Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const targetId = this.getAttribute('href');
                const targetElement = document.getElementById(targetId.substring(1));

                if (targetElement) {
                    console.log('Rolando para elemento:', targetElement);
                    targetElement.scrollIntoView({ behavior: 'smooth' });

                    // Fechar o menu hambúrguer após clicar em um link (se estiver aberto)
                    if (hamburger.classList.contains('active')) {
                        hamburger.classList.remove('active');
                        navLinks.classList.remove('active');
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

    // Image Carousel (Basic Implementation)
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
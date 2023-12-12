// Function to reset the gallery scroll
function resetGalleryScroll() {
    const galleryContainer = document.querySelector('.horizontal-scroll-gallery');
    galleryContainer.style.animation = 'none'; // Pause the animation
    galleryContainer.style.transform = 'translateX(0)'; // Reset the scroll position
    setTimeout(() => {
        galleryContainer.style.animation = 'scrollGallery 10s linear infinite'; // Resume the animation
    }, 100); // Delay the resumption to prevent flickering
}

// Check scroll position and reset if necessary
setInterval(function() {
    const galleryContainer = document.querySelector('.horizontal-scroll-gallery');

    // Check if galleryContainer is not null before proceeding
    if (galleryContainer) {
        const galleryWidth = galleryContainer.offsetWidth - galleryContainer.clientWidth;
        const scrollPosition = galleryContainer.scrollLeft;

        if (scrollPosition >= galleryWidth) {
            resetGalleryScroll();
        }
    }
}, 100);
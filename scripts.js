// Smooth Scroll to Sections
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: "smooth" });
    }
}

// Form Submission Handler
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // Simulate form submission
        alert(`Thank you, ${name}! Your message has been received.`);
        contactForm.reset(); // Reset the form
    });
}

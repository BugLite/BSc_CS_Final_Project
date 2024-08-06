// Bulma Script for Navbar Burger
document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target;
                const $target = document.getElementById(target);
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }
});

// javascript time
function updateTime() {
    const now = new Date();
    const day = now.getDate().toString().padStart(2, '0');
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-indexed
    const year = now.getFullYear();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    
    // Format date and time
    const dateString = `${day}-${month}-${year}`;
    const timeString = `| PKT ${hours}:${minutes}:${seconds}`;
    
    // Combine date and time
    document.getElementById('current-time').textContent = `${dateString} ${timeString}`;
}

// Update time every second
setInterval(updateTime, 1000);

// Initialize time on page load
document.addEventListener('DOMContentLoaded', updateTime);
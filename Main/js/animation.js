const table = document.getElementById('resultsTable');

table.addEventListener('mousemove', function(event) {
    const rect = table.getBoundingClientRect();
    const tableX = rect.left + rect.width / 2;
    const tableY = rect.top + rect.height / 2;
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    const deltaX = -(mouseX - tableX) / rect.width;
    const deltaY = -(mouseY - tableY) / rect.height;

    const tiltStrength = 8; 

    table.style.transform = `perspective(1000px) rotateX(${deltaY * tiltStrength}deg) rotateY(${deltaX * -tiltStrength}deg)`;
});

table.addEventListener('mouseleave', function() {
    table.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;
});
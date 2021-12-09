window.addEventListener("DOMContentLoaded", function() {
    const obj = document.getElementById("curr-icon");
    obj.addEventListener('change', updatePage);
});

function changeColor() {
    let color = document.getElementById('colorInputColor').value;
    const img = document.getElementById("profile-icon").getSVGDocument().getElementById("changeMe");
    img.style.fill = color;
}

async function updatePage(){
    const userId = document.getElementById("userID").value;
    const userRole = document.getElementById("userRole").value;
    const svg_icon = document.getElementById("profile-icon")
    const curr_icon = document.getElementById("curr-icon").value;
    svg_icon.data = `/static/images/${curr_icon}`
}

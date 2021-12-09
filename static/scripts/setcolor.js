window.addEventListener("DOMContentLoaded", function() {
    let color = document.getElementById('userColor').value;
    for(const svg of document.querySelectorAll(".svg-icon")){
        svg.addEventListener("load",function() {
            img = svg.getSVGDocument().getElementById("changeMe");
            img.style.fill = color;
        }, false);
	}
});
window.addEventListener("DOMContentLoaded", function() {
    for(const player of document.querySelectorAll(".players")){
        let color = document.getElementById(player.value).value;
        const svg = document.getElementById(`profile-icon-${player.value}`);
        svg.addEventListener("load",function() {
            img = svg.getSVGDocument().getElementById("changeMe");
            img.style.fill = color;
        }, false);
	}
});
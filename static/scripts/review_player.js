window.addEventListener("DOMContentLoaded", function() {
	for(btn of document.querySelectorAll(".remove-btn")){
		btn.addEventListener("click", removeItem);
	}
});

function removeItem(event){
	const btn = event.target;
	let parent = btn.parentElement;
	parent = parent.parentElement;
	const playerID = document.getElementById("playerID").value;
	return fetch(`/reviewplayer/${playerID}`, {
		method: "DELETE"
	})
	.then(function(){
		parent.remove();
	});
}
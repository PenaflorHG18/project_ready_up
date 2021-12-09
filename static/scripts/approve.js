window.addEventListener("DOMContentLoaded", function() {
	for(btn of document.querySelectorAll(".remove-btn")){
		btn.addEventListener("click", removeItem);
	}

	for(btn of document.querySelectorAll(".approve-btn")){
		btn.addEventListener("click", approveItem);
	}
});

function removeItem(event){
	const btn = event.target;
	let parent = btn.parentElement;
	parent = parent.parentElement;
	const gameID = document.getElementById("gameID").value;
	return fetch(`/reviewgames/${gameID}`, {
		method: "DELETE"
	})
	.then(function(){
		parent.remove();
	});
}

function approveItem(event){
	const btn = event.target;
	let parent = btn.parentElement;
	parent = parent.parentElement;
	const gameID = document.getElementById("gameID").value;
	return fetch(`/reviewgames/${gameID}`, {
		method: "POST"
	})
	.then(function(){
		parent.remove();
	});
}
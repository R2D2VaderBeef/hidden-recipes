const data = document.currentScript.dataset;

window.addEventListener("load", function (event) {
    document.getElementById("like-button").addEventListener("click", likePost);
    document.getElementById("id_text").placeholder = "Remember to be respectful!"
});

function likePost() {
    let button = this;
    let likeCount = document.getElementById("likes-count");

    fetch(`/like/${data.recipe}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": data.csrf,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        likeCount.innerText = data.likes_count;
        button.innerText = data.liked ? "Unlike" : "Like";
        document.getElementById("likeSvg").className = data.liked ? "liked" : "";
    });
}
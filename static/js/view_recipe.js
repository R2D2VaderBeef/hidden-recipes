const data = document.currentScript.dataset;

window.addEventListener("load", function (event) {
    document.getElementById("like-button").addEventListener("click", likePost);
    let commentField =  document.getElementById("id_text")
    commentField.placeholder = "Remember to be respectful!"
    commentField.addEventListener("keypress", ctrlEnterPostComment)
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

function ctrlEnterPostComment(event) {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        document.getElementById("commentForm").submit();
    }
}
function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    //const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`api/v1/like-post/${postId}/`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = "Likes: " + data["likes"];
            //if (data["liked"] === true) {
            //likeButton.className = "fas fa-thumbs-up";
            //} else {
            //likeButton.className = "far fa-thumbs-up";
            //}
        })
        .catch((e) => alert("Could not like post" + e));
}

var inputCount = 0;

function add_tag() {
    if (inputCount <= 4) {
        const container = document.getElementById(`tags`);
        var input = document.createElement("input");
        input.name = "tag" + inputCount;
        strcount = String(parseInt(inputCount) + 1)
        input.placeholder = "Enter tag " + strcount;
        container.appendChild(input);
        inputCount++;
    }
}
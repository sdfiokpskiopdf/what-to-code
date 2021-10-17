function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`api/v1/like-post/${postId}/`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className = "fas fa-thumbs-up";
            } else {
                likeButton.className = "far fa-thumbs-up";
            }
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
        input.style.cssText = "display: inline-flex;box-shadow: inset 0 .0625em .125em rgba(10,10,10,.05);width:  100%;height: 2.5rem;padding: calc(.5em - 1px) calc(.75em - 1px);align-items: center;justify-content: flex-start;border: 1px solid #dfdfdf;color: #363636;border-radius: 4px;font-family: var(--font-family);"
        container.appendChild(input);
        inputCount++;
    }
}
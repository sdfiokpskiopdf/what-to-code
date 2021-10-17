var inputs = [];

function remove_tag(inputName) {
    console.log("called")
    var input = document.getElementsByName(inputName)[0];
    var button = document.getElementsByClassName(`button_${inputName}`)[0]
    input.parentNode.removeChild(input);
    button.parentNode.removeChild(button)
    for (let i of inputs) {
        if (i.name == input.name) {
            inputs.splice(inputs.indexOf(i), 1);
            break;
        }
    }

    console.log(inputs)

    for (let i of inputs) {
        var old_name = i.name
        i.setAttribute("name", "tag" + inputs.indexOf(i))
        strcount = String(parseInt(inputs.indexOf(i)) + 1)
        i.setAttribute("placeholder", "Enter tag " + strcount)
        document.getElementsByClassName(`button_${old_name}`)[0].setAttribute("onclick", `remove_tag('${i.name}')`)
        document.getElementsByClassName(`button_${old_name}`)[0].setAttribute("class", `button_${i.name}`)
    }
}

function add_tag() {
    if (inputs.length <= 4) {
        const container = document.getElementById(`tags`);
        var input = document.createElement("input");
        var remove_button = document.createElement("button");
        input.name = "tag" + inputs.length;
        strcount = String(parseInt(inputs.length) + 1)
        input.placeholder = "Enter tag " + strcount;
        input.style.cssText = "display: inline-flex;box-shadow: inset 0 .0625em .125em rgba(10,10,10,.05);width:  100%;height: 2.5rem;padding: calc(.5em - 1px) calc(.75em - 1px);align-items: center;justify-content: flex-start;border: 1px solid #dfdfdf;color: #363636;border-radius: 4px;font-family: var(--font-family);";
        remove_button.style.cssText = "background-color: var(--accent-color);border-color: transparent;color: rgba(0,0,0,.7);border-radius: 4px;padding: .5em 1em;width:15%;";
        remove_button.className = `button_${input.name}`
        remove_button.setAttribute("onclick", `remove_tag('${input.name}')`)
        remove_button.innerText = "Remove"
        container.appendChild(input);
        container.appendChild(remove_button);
        inputs.push(input)
    }
}
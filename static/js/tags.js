const data = document.currentScript.dataset;

window.addEventListener("load", function (event) {
    addTags();
    document.getElementById("tagForm").addEventListener("submit", submitForm);
});

function addTags() {
    let tags = JSON.parse(data.tags);
    let select = document.getElementById("tags");
    let query = new URLSearchParams(window.location.search);
    let selected = []
    if (query.has("tags")) {
        let tagString = query.get("tags")
        selected = tagString.split("|")
    }
    for (let i = 0; i < tags.length; i++) {
        let option = document.createElement("option");
        let name = tags[i].fields.name
        option.value = name;
        option.textContent = name;
        if (selected.includes(name)) {
            option.selected = true;
        }
        select.appendChild(option);
    }
}

function submitForm() {
    let selectedTags = document.getElementById("tags").selectedOptions;
    let tags = [];
    for (let i = 0; i < selectedTags.length; i++) {
        tags.push(selectedTags[i].value);
    }
    document.getElementById("realtags").value = tags.join("|")
}
function showDropdown(id) {
    let dropdown =  document.getElementById(id)
    if (!dropdown.classList.contains("visible")) {
        dropdown.classList.add("visible");
    }
}

window.addEventListener("click", function (e) {
    let dropdowns = ["recipesDropdown", "accountDropdown"]
    for (let i = 0; i < dropdowns.length; i++) {
        checkHide(e, dropdowns[i])
    }
});

function checkHide(e, id) {
    if (!(e.target.matches("#" + id) || e.target.matches("#" + id + "Button"))) {
        let dropdown = document.getElementById(id);
        if (dropdown.classList.contains("visible")) {
            dropdown.classList.remove("visible");
        }
    }
}
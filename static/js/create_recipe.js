const data = document.currentScript.dataset;
let cropper;
let recipeCount = 0;
let stepsCount = 0;


window.addEventListener("load", function (event) {
    document.getElementById("recipeForm").addEventListener("submit", submitRecipe);
    document.getElementById("recipePicture").addEventListener("change", cropPhoto);
    document.getElementById("add-ingredient").addEventListener("keypress", enterKeyAddIngredient);
    document.getElementById("add-step").addEventListener("keypress", ctrlEnterAddStep)
    new Sortable(document.getElementById("instructions-container"), {
        draggable: ".single-step",
        handle: ".handle",
        animation: 150
    })
    addTags();
});

function addTags() {
    let tags = JSON.parse(data.tags);
    let select = document.getElementById("tags");
    for (let i = 0; i < tags.length; i++) {
        let option = document.createElement("option");
        option.value = tags[i].pk;
        option.textContent = tags[i].fields.name;
        select.appendChild(option);
    }
}

async function submitRecipe(e) {
    e.preventDefault();
}

function cropPhoto() {
    let photo = document.getElementById("recipePicture").files[0]
    let image = new Image();
    image.src = URL.createObjectURL(photo)

    document.getElementById('cropper-container').innerHTML = "";
    document.getElementById("cropper-output").innerHTML = "";

    cropper = new Cropper.default(image, {
        container: '#cropper-container',
    });


    let selection = cropper.getCropperSelection();
    selection.aspectRatio = 1.6;
    selection.id = "cropperSelection"

    let cropperImage = cropper.getCropperImage();
    cropperImage.initialCenterSize = "cover";

    let preview = document.createElement("cropper-viewer");
    preview.selection = "#cropperSelection";

    let previewContainer = document.createElement("div");
    previewContainer.id = "previewContainer";
    previewContainer.innerHTML = `
    <label>Preview</label>
    `
    previewContainer.appendChild(preview);

    let button = document.createElement("button")
    previewContainer.appendChild(button);
    button.outerHTML = `<button onclick="finaliseCrop(event)">Crop</button>`

    document.getElementById('cropper-container').appendChild(previewContainer);

    document.getElementById("cropper-help").style.display = "block";

}

async function finaliseCrop(e) {
    e.preventDefault();
    document.getElementById("cropper-output").innerHTML = "";
    let canvas = await cropper.getCropperSelection().$toCanvas({ height: 200 });
    document.getElementById("cropper-output").appendChild(canvas);

    document.getElementById('cropper-container').innerHTML = "";
    document.getElementById("cropper-help").style.display = "none";
}

function enterKeyAddIngredient (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("add-ingredient-button").click();
    }
} 

function ctrlEnterAddStep (event) {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      document.getElementById("add-step-button").click();
    }
} 

function addIngredient(e) {
    e.preventDefault();
    let inputField = document.getElementById("add-ingredient")
    let text = inputField.value;
    let component = `
    <input type="text" placeholder="Click the button on the right to delete" value="%text%" required>
    <button id="deleteingredient%counter%" onclick="deleteIngredient(event)">✕</button>
    `
    addListItem(text, "ingredient", "single-ingredient", component, recipeCount, "ingredients-container")
    .then(() => {
        inputField.value = "";
        recipeCount++;
    })
    .catch(() => {});
}

function addStep(e) {
    e.preventDefault();
    let textarea = document.getElementById("add-step")
    let text = textarea.value.replaceAll("\n", " ");
    let component = `
    <span class="handle">⋮⋮</span>
    <textarea placeholder="Click the button on the right to delete" required>%text%</textarea>
    <button id="deletestep%counter%" onclick="deleteStep(event)">✕</button>
    `
    addListItem(text, "step", "single-step", component, stepsCount, "instructions-container")
    .then(() => {
        textarea.value = "";
        stepsCount++;
    })
    .catch(() => {});
}

function addListItem(text, id, classname, component, counter, container) {
    return new Promise((resolve, reject) => {
        if (text == "") return reject();
        let item = document.createElement("div");
        item.id = id + counter.toString();
        item.className = classname;
        item.innerHTML = component.replaceAll("%counter%", counter.toString()).replaceAll("%text%", text);
        document.getElementById(container).appendChild(item);
        resolve();
    })
}

function deleteIngredient(e) {
    e.preventDefault();
    let id = e.target.id.split("deleteingredient")[1];
    let ingredient = document.getElementById("ingredient" + id);
    ingredient.remove();
}

function deleteStep(e) {
    e.preventDefault();
    let id = e.target.id.split("deletestep")[1];
    let step = document.getElementById("step" + id);
    step.remove();
}
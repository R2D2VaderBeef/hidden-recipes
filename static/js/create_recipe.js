const data = document.currentScript.dataset;
console.log(JSON.parse(data.tags));
let cropper;


window.addEventListener("load", function (event) {
    document.getElementById("recipeForm").addEventListener("submit", submitRecipe);
    document.getElementById("recipePicture").addEventListener("change", cropPhoto);
});

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
    let canvas = await cropper.getCropperSelection().$toCanvas({height: 200});
    document.getElementById("cropper-output").appendChild(canvas);

    document.getElementById('cropper-container').innerHTML = "";
    document.getElementById("cropper-help").style.display = "none";
}
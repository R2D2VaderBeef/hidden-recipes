const data = document.currentScript.dataset;

window.addEventListener("load", function (event) {
    document.getElementById("profileForm").addEventListener("submit", submitProfile);
    document.getElementById("profilePicture").addEventListener("change", cropPhoto);
});

async function submitProfile(e) {
    e.preventDefault();

    let newBio = document.getElementById("bio").value;

    let file = null;
    if (document.getElementById("cropper-output").children.length > 0) {
        let blob = await new Promise(resolve => document.getElementById("cropper-output").children[0].toBlob(resolve));
        file = new File([blob], `${data.username.replace(/[^a-zA-Z0-9]/g, '')}.png`, { type: 'image/png' });
    }
    else {
        // Show the crop dialog if they are midway through adding a photo.
        let cropperPreview = document.getElementById("previewContainer");
        if (cropperPreview) {
            cropperPreview.scrollIntoView({behavior: 'smooth'});
            cropperPreview.children[2].focus({focusVisible: true});
            cropperPreview.children[3].style.display = "block";
            return;
        }
    }

    let formData = new FormData();
    formData.append("action", "save_profile");
    formData.append("bio", newBio);
    formData.append("csrfmiddlewaretoken", document.getElementById("profileForm").children[0].value);

    if (file == null) {
        formData.append("new_picture", "false");
    }
    else {
        formData.append("new_picture", "true");
        formData.append("picture", file);
    }

    const response = await fetch(".", {
        method: "POST",
        body: formData
    })

    let res = await response.text();
    console.log(res);
    window.location.href = res;
}

function cropPhoto() {
    let photo = document.getElementById("profilePicture").files[0]
    let image = new Image();
    image.src = URL.createObjectURL(photo)

    document.getElementById('cropper-container').innerHTML = "";
    document.getElementById("cropper-output").innerHTML = "";

    cropper = new Cropper.default(image, {
        container: '#cropper-container',
    });


    let selection = cropper.getCropperSelection();
    selection.aspectRatio = 1;
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

    let button = document.createElement("button");
    previewContainer.appendChild(button);
    button.outerHTML = `<button onclick="finaliseCrop(event)">Save Crop</button>`

    let error = document.createElement("p");
    error.classList.add("error");
    error.classList.add("hidden");
    error.textContent = "Please save your profile image crop."
    previewContainer.appendChild(error);

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
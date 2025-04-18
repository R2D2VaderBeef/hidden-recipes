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
    let title = document.getElementById("recipe-title").value;
    let description = document.getElementById("recipe-description").value;

    let selectedTags = document.getElementById("tags").selectedOptions;
    let tags = [];
    for (let i = 0; i < selectedTags.length; i++) {
        tags.push(selectedTags[i].value);
    }

    let file = null;
    if (document.getElementById("cropper-output").children.length > 0) {
        let blob = await new Promise(resolve => document.getElementById("cropper-output").children[0].toBlob(resolve));
        file = new File([blob], `${title.replace(/[^a-zA-Z0-9]/g, '')}.png`, { type: 'image/png' });
    }
    else {
        // We are missing a picture. Let's show the crop dialog if they haven't cropped yet
        let cropperPreview = document.getElementById("previewContainer");
        if (cropperPreview) {
            cropperPreview.scrollIntoView({behavior: 'smooth'});
            cropperPreview.children[2].focus({focusVisible: true});
            cropperPreview.children[3].style.display = "block";
            return;
        }
        else {
            // Or clear the picture field and try again
            let pictureIn = document.getElementById("recipePicture")
            pictureIn.value = "";
            pictureIn.focus({focusVisible: true})
            return document.getElementById("recipeForm").reportValidity()
        }   
    }

    let addedIngredients = document.getElementById("ingredients-container").children;
    let ingredients = []
    for (let i = 0; i < addedIngredients.length; i++) {
        ingredients.push(addedIngredients[i].children[0].value)
    }
    if (ingredients.length < 1) {
        // Show the user they need to add at least one ingredient
        addMissingIngredient();
        document.getElementById("ingredients-container").scrollIntoView({behavior: 'smooth'});
        return document.getElementById("recipeForm").reportValidity()
    }

    let addedInstructions = document.getElementById("instructions-container").children;
    let instructions = []
    for (let i = 0; i < addedInstructions.length; i++) {
        instructions.push(addedInstructions[i].children[1].value.replaceAll("\n", "").replaceAll("\r", ""))
    }
    if (instructions.length < 1) {
        // Show the user they need to add at least one step
        addMissingStep();
        document.getElementById("instructions-container").scrollIntoView({behavior: 'smooth'});
        return document.getElementById("recipeForm").reportValidity()
    }

    // Construct and send a form request Django can hopefully understand
    let formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("ingredients", ingredients.join("\n"));
    formData.append("instructions", instructions.join("\n"));
    formData.append("tags", tags.join(","));
    formData.append("picture", file);
    formData.append("csrfmiddlewaretoken", document.getElementById("recipeForm").children[0].value)

    const response = await fetch(".", {
        method: "POST",
        body: formData
    })

    let redirect = await response.text();
    window.location.href = redirect;
}
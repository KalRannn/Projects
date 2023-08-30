const model = await tf.loadLayersModel('toxic.h5');
const commentInput = document.getElementById("commentInput");
const checkButton = document.getElementById("checkButton");
const resultDiv = document.getElementById("result");


checkButton.addEventListener("click", () => {

    const comment = commentInput.value;
    

    // Perform inference using the loaded model
    const predictions = model.predict(comment);
    print(comment)
    if (comment.includes("bad word")) {
        resultDiv.textContent = "Toxic comment detected!";
    } else {
        resultDiv.textContent = "Comment seems fine.";
    }


});
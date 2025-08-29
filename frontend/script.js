// script.js
async function uploadImage() {
  const input = document.getElementById("imageInput");
  const file = input.files[0];

  if (!file) {
    alert("Please select an image first!");
    return;
  }

  // Preview the image
  const reader = new FileReader();
  reader.onload = async () => {
    document.getElementById("preview").innerHTML = `<img src="${reader.result}" alt="Preview" style="max-width:300px; max-height:300px;">`;
    
    // Prepare payload with base64 image
    const payload = { image: reader.result };

    // Show sending status
    document.getElementById("caption").innerText = "⏳ Generating caption...";

    try {
      // Send to Flask backend
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();

      // Display caption
      document.getElementById("caption").innerText = "📝 Caption: " + (data.caption || "No caption returned");
    } catch (error) {
      document.getElementById("caption").innerText = "❌ Error contacting backend!";
      console.error(error);
    }
  };

  reader.readAsDataURL(file); // convert to base64
}

// Attach to button
document.getElementById("uploadBtn").addEventListener("click", uploadImage);

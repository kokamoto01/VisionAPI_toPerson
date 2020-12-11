function toBase64(imagePath) {
  // Read the file into memory.
  const fs = require("fs");
  const imageFile = fs.readFileSync(imagePath);

  // Convert the image data to a Buffer and base64 encode it.
  return Buffer.from(imageFile).toString("base64");
}

(async function () {
  const axios = require("axios");

  require('dotenv').config(); // .envからAPIキーを持ってくる
  const apiKey = process.env.API_KEY;

  if (!apiKey) {
    console.log("Env 'VISION_API_KEY' must be set.");
    process.exit(1);
  }

  const visionApiUrl = `https://vision.googleapis.com/v1/images:annotate?key=${apiKey}`;
  const imagePath = "./test05.jpg";
  const options = {
    requests: [
      {
        image: {
          content: toBase64(imagePath),
        },
        features: [
          {
            type: "OBJECT_LOCALIZATION",
            maxResults: 50,
          },
        ],
      },
    ],
  };
  
  try {
    const result = await axios.post(visionApiUrl, options);
    console.log("Request success!");

    if (result.data && result.data.responses) {
      const responses = result.data.responses;
      let detectedPerson = 0;

      responses.forEach((response) => {
        response.localizedObjectAnnotations.forEach((object) => {
          console.log(object.name);
          if(object.name == "Person"){
            detectedPerson++;
          }
        });
      });

      if(detectedPerson != 0){
        console.log("人物を" + detectedPerson + "人検出できました。");
      } else {
        console.log("人物を検出できませんでした。");
      }
    }

  } catch (error) {
    console.error(error.response || error);
  }
})();
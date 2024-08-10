const apiURL = "https://stockauto.onrender.com"

const uploadFile = () => {
    console.log("Button click works!!!");
    const file = document.querySelector(".form-file").files[0];
    const rowStart = document.querySelector(".form-row-start").value;
    const rowEnd = document.querySelector(".form-row-end").value;
    
    console.log("File details ===> ", file.name, file.type)
    let formData = new FormData();
    formData.append('file', file);
    formData.append('row_start', rowStart);
    formData.append('row_end', rowEnd);
    url = `${apiURL}/api/file/upload`
    console.log("Request will be sent to: ", url);

    // make POST call
    fetch(
        url,
        {
            body: formData,
            method: "post",
            // headers: {
            //     "Content-Type": "multipart/form-data",
            // }
        }
    )
    .then((res) => {
        console.log("Response from server ===> ", res)
        return res.json();
    })
    .then((data) => {
        file_id = data?.file_id;
        const url = new URL(window.location.href);
        const hostname = url?.pathname?.split("/")?.slice(0, -1)?.join("/");
        const redirectUrl = `${hostname}/download.html?file_id=${file_id}`
        console.log("Redirecting to file download page...");
        window.location.href = redirectUrl;
    })
};

function downloadBase64File(base64String, fileName) {
    console.log("reached download helper function!")
    // Decode Base64 string to binary string
    var binaryString = atob(base64String);
    
    // Convert binary string to array of 8-bit unsigned integers
    var byteNumbers = new Array(binaryString.length);
    for (var i = 0; i < binaryString.length; i++) {
        byteNumbers[i] = binaryString.charCodeAt(i);
    }
    var byteArray = new Uint8Array(byteNumbers);

    // Create a Blob from the byte array
    var blob = new Blob([byteArray], {type: 'application/octet-stream'});

    // Create a download link and trigger the download
    var link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    console.log("link ", link.href)
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


const downloadFile = () => {
    console.log("File Download [CLIENT CALL]");

    const urlSearchParams = new URLSearchParams(window.location.search);
    const file_id = urlSearchParams.get("file_id")
    console.log("File ID ===> ", file_id)

    // file_id = '3e679add-649d-474f-9f8d-ba0cd1ae4b21'
    // file_id = '32b92d2a-e957-45f8-9bb0-523bf7fdc7ee'
    url = `${apiURL}/api/file/download/${file_id}`
    console.log("Request will be sent to: ", url);

    // make GET call
    fetch(url)
    .then((res) => {
        console.log("Response from GET ===>", res);
        return res.json()
    })
    .then((data) => {
        msg = data?.message;
        fileData = data?.data?.file;
        fileStatus = data?.status;

        // Add msg to UI
        responseElement = document.querySelector(".download-response-msg")
        responseElement.textContent = msg;
        responseElement.style.visibility = "visible"; // Override initial invisibility
        
        // Download File if ready 
        if (fileStatus == "completed") {
            console.log("len ", fileData.length)
            downloadBase64File(fileData, "nav_updated.xlsx");
        };

    })
}
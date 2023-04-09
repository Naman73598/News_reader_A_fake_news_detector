
function getOuterText(contentElem){
    // console.log("Content elem : " + contentElem)
    return document.body.outerText;
    // contentElem.innerText = document.body.outerText;
};


chrome.tabs.query({ active: true, currentWindow : true }, async function (tabs) {
    var tab = tabs[0];
    var tabUrl = tab.url;
    var tabHtml = "";

    // console.log(tab);
    console.log(tab.id);
    console.log(tab.url);

    // const [tabInfo] = await chrome.tabs.executeScript(tab.id, { code: '({title: document.title, url: document.URL})' });
    // console.log(tabInfo);
    const contentElem = document.querySelector("#page-content");
    const predictionElem = document.querySelector("#prediction");

    console.log(contentElem);
    
    const results = await chrome.scripting.executeScript({
        target : { tabId : tab.id },
        func: getOuterText,
        args : [contentElem]
    });
    
    contentElem.innerText = results[0].result;
    
    try{
        const response = await fetch("http://localhost:5000/fake-news/predict", {
            method: "post",
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify({ "content" : [results[0].result]})
        });

        if(!response.ok){
            alert("Error in running the model");
            return;
        }

        const data = await response.json();
        
        if(data["predictions"][0] == 1){
            predictionElem.innerHTML = 
                `The given news is <span class="h5 fw-bold text-danger">Fake</span>`;
        }else{
            predictionElem.innerHTML = 
                `The given news is <span class="h5 fw-bold text-success">Genuine</span>`;
        }

    }catch(err){
        console.log(err);
        alert("Error occured in detecting news validity");
    }

});
function getOuterText(){
    console.log(document.documentElement.outerText);

    $("#page-content")[0].innerText = document.documentElement.outerText;
};


chrome.tabs.query({ active: true }, async function (tabs) {
    var tab = tabs[0];
    var tabUrl = tab.url;
    var tabHtml = "";

    console.log(tab.id);
    console.log(tab.url);
    
    chrome.scripting.executeScript({
        target : { tabId : tab.id },
        func: getOuterText
    }).then(() => {
        console.log("called getOuterText");
    })

});
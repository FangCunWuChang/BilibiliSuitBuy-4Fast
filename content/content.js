
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.key == "getCookies") {
        getCookies(message.value).then(sendResponse);
    };

    if (message.key == "getMySuitListRes") {
        getMySuitListRes(message.value).then(sendResponse);
    };
    if (message.key == "getMyFannumListRes") {
        getMyFannumListRes(message.value).then(sendResponse);
    };

    if (message.key == "postMySuitListSortRes") {
        postMySuitListSortRes(message.value).then(sendResponse);
    };
    if (message.key == "postGiveFannumToUser") {
        postGiveFannumToUser(message.value).then(sendResponse);
    }
    
    return true;
});

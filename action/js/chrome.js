// function backgroundPage(reqkey, value) {
//     // 和background.js 交互
//     return new Promise(function (resolve, _) {
//         chrome.runtime.sendMessage({key: reqkey, value: value}, function(res) {
//             resolve(res);
//         });
//     });
// };

function contentPage(reqkey, value) {
    // 和content.js 交互
    return new Promise(function (resolve, _) {
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {key: reqkey, value: value}, function(res) {
                resolve(res);
            });
        });
    });
};

function setLocalContent(content) {
    // 保存数据到本地
    return new Promise(function (resolve, _) {
        chrome.storage.local.set(content, function() {
            resolve(content);
        });
    });
};

function getLocalContent(key) {
    // 获取本地数据
    return new Promise(function (resolve, _) {
        chrome.storage.local.get([key], function(value) {
            resolve(value[key]);
        });
    });
};

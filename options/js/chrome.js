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

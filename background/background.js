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

// -----------------------------------------------------

chrome.contextMenus.create({
    // 注册右键组件
    id: "test",
    title: "test",
    type: 'normal'
});

// -----------------------------------------------------

async function initializeConfig() {
    // 初始化设置
    const defaultObj = {"style": {}, "switch": {}}
    var config = await getLocalContent("config") || defaultObj;
    if (!config["style"]["popup-background-color"]) {
        config["style"]["popup-background-color"] = "#202020";
    };
    await setLocalContent({"config": config});
    // console.log(config);
};

chrome.runtime.onInstalled.addListener(async function() {
    await initializeConfig();

    chrome.contextMenus.onClicked.addListener(async function(info, tab) {
        if (info.menuItemId === "test") {
            var res = await contentPage("getCookies", null);
            console.log(res);
            // chrome.tabs.create({url: `https://space.bilibili.com/1701735549`});
        };
    });
});

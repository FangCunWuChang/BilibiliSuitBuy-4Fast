function padNumber(num, len) {
    // 数字补齐
    return (Array(len).join("0") + `${num}`).slice(-len);
};


function getFanCardItemJson(eve) {
    // 获取粉丝卡片的item
    const item = eve.childNodes[0].dataset["item"];
    return JSON.parse(item);
};

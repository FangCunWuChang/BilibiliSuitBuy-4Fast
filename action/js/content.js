async function fanNumberOption(item) {
    // 库存
    var res = await contentPage("getMyFannumListRes", {item_id: item["item_id"]});
    console.log(res);
    if (res["code"] == 0) {
        setFanNumberList(res["data"]["list"] || new Array());
    } else {
        alert(res["message"]);
    };
};

function updateContentBackground(cover) {
    // 更新背景图片
    const image = document.getElementById(ChooseItemBoxBg_Id);
    image.opacity = chooseBackgroundOpacity;
    image.src = cover;
};

async function onClickFanCardHandle(eve) {
    const cover = eve.childNodes[0].dataset["cover"];
    var item = getFanCardItemJson(eve);
    updateContentBackground(cover);

    const root = document.getElementById("choose-item-box");
    delete item["fan_share_image"];
    root.dataset["item"] = JSON.stringify(item);

    var option = document.getElementById("main-box-option");

    if (option.options[0].value == "fanNumberOption"){
        await fanNumberOption(item);
    };
};

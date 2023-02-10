(async function() {
    // 初始化透明度选择条
    const root = document.getElementById("opacity-range");
    root.value = chooseBackgroundOpacity * 100;
})();

document.getElementById("opacity-range").onchange = async function() {
    // 背景透明度
    const root = document.getElementById("choose-item-box-bg");
    root.style.opacity = parseInt(this.value) / 100;
};

function setFanNumberList(number_list) {
    var root = document.getElementById("fan-number-item");
    root.innerHTML = "";

    for (let i = 0; i < number_list.length; i++) {
        const item = number_list[i];
        var tag = document.createElement("a");

        if (item["mid"] == item["buy_mid"]) {
            tag.className = "fan-number-item-yes";
        
            tag.onclick = function() {
                if (this.className == "fan-number-item-choose") {
                    this.className = "fan-number-item-yes";
                    return
                };
                var items = document.getElementsByClassName("fan-number-item-choose");
                for (let i = 0; i < items.length; i++) {
                    items[i].className = "fan-number-item-yes";
                };

                this.className = "fan-number-item-choose";
            };;
            tag.dataset["item"] = JSON.stringify(item);

        } else {
            tag.className = "fan-number-item-no";
        };

        tag.innerText = padNumber(item["number"], 6);
        root.append(tag);
    };
};

document.getElementById("main-box-option").onchange = async function() {
    // 选择显示内容
    const index = this.options.selectedIndex;
	const value = this.options[index].value;

    const root = document.getElementById("choose-item-box");
    const item = JSON.parse(root.dataset["item"]);

    if (value == "fanNumberOption"){
        await fanNumberOption(item);
    };
};

document.getElementById("give-fan-number-user").onclick = async function() {
    var choose_items = document.getElementsByClassName("fan-number-item-choose");
    if (choose_items.length == 0 || choose_items.length > 1) {
        alert("未选择编号 or 选择数量超过1个");
        return
    };

    const data_div = document.getElementById("choose-item-box");

    const item = JSON.parse(choose_items[0].dataset["item"]);
    const item_id = JSON.parse(data_div.dataset["item"])["item_id"];

    var to_mid = prompt("输入获赠人Uid", "0");
    var res = await contentPage("postGiveFannumToUser", {
        "fan_num": item["number"], "item_id": item_id, "to_mid": to_mid,
    });
    console.log(res);

    if (res["code"] == 0) {
        alert("赠送成功");
    } else {
        alert(res["message"]);
    };
};

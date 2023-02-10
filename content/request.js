function reqAsy(data) {
    // 请求
    return new Promise(function (resolve, reject) {
        const url = addParams(data.url, data["params"]);
        var xhr = new XMLHttpRequest();
        xhr.open(data.method, url, true);
        if (data.method == "POST") {
            xhr.setRequestHeader("Content-Type", data["type"] || "");
        };
        xhr.onload = function() {
            if (xhr.status == 200) {
                resolve(JSON.parse(xhr.responseText));
            } else {
                reject(Error(xhr.statusText));
            };
        };
        xhr.withCredentials = true;
        xhr.send(data["body"] || null);
    });
};

async function getMySuitListRes(data) {
    // 获取自己拥有的装扮 type->json
    const url = "https://api.bilibili.com/x/garb/user/suit/asset/list";
    return await reqAsy({method: "GET", url: url, params: {
        "part": "suit", "state": "active", "is_fans": "true", 
        "ps": data.ps, "pn": data.pn,
    }});;
};

async function getMyFannumListRes(data) {
    // 获取自己指定装扮的库存
    const url = "https://api.bilibili.com/x/garb/user/fannum/list";
    return await reqAsy({method: "GET", url: url, params: {
        "item_id": data.item_id,
    }});;
};

async function postMySuitListSortRes(data) {
    // 应用装扮排序
    var cookies = await getCookies(null);
    var body = `ids=${data.ids.join(",")}&csrf=${cookies["bili_jct"]}`
    return await reqAsy({
        url: "https://api.bilibili.com/x/garb/user/suit/asset/list/sort",
        method: "POST", type: "application/x-www-form-urlencoded", body: body,
    });
};

async function postGiveFannumToUser(data) {
    // 赠送装扮
    var cookies = await getCookies(null);
    var body = `item_id=${data["item_id"]}&fan_num=${data["fan_num"]}&`;
    body += `to_mid=${data["to_mid"]}&csrf=${cookies["bili_jct"]}`;
    return await reqAsy({
        url: "https://api.bilibili.com/x/garb/user/fannum/present/v2",
        method: "POST", type: "application/x-www-form-urlencoded", body: body,
    });
};

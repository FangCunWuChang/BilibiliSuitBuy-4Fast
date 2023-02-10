function addParams(_url, params) {
    // 往url添加Params
    if (!params) {
        return _url;
    }
    var url = _url + "?"
    for(let key in params) {
        url += `${key}=${params[key]}&`
    };
    return url.slice(0, url.length-1);
};

function cookieString2Object(cookies) {
    // 字符串cookie转object
    var cookie = {};
    if (!cookie) {
        return cookie;
    };
    var cookie_list = cookies.split("; ");
    for (let i = 0; i < cookie_list.length; i++) {
        var element = cookie_list[i].split("=");
        if (element.length < 2) {
            element = [element[0], ""];
        };
        cookie[element[0]] = element[1];
    };
    return cookie
};

async function getCookies(_) {
    // 获取cookies -> type[dict]
    return cookieString2Object(document.cookie);
};

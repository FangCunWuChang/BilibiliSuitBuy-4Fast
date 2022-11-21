function getQueryValue(key) {
    const url_href = new URL(window.location.href);
    const url = new URL(url_href);
    return url.searchParams.get(key);
}

window.onload = function() {
    var gee_gt = getQueryValue("gt");
    var gee_challenge = getQueryValue("challenge");
    $('#gt')[0].value = gee_gt;
    $('#challenge')[0].value = gee_challenge;

    var handler = function (captchaObj) {
        captchaObj.appendTo('#captcha');
        captchaObj.onReady(function () {
            $("#wait").hide();
        });

        var interval = setInterval(function(){
            var result = captchaObj.getValidate();
            if (result) {
                var data = btoa(JSON.stringify(result))
                location.href = "/finish?" + "data=" + data
                clearInterval(interval)
            }
        }, 2000)
    };

    $('#text').hide();
    $('#wait').show();
    initGeetest({
        gt: $('#gt')[0].value,
        challenge: $('#challenge')[0].value,
        offline: false,
        new_captcha: true,

        product: "popup", 
        width: "300px",
        https: true
    }, handler);
}

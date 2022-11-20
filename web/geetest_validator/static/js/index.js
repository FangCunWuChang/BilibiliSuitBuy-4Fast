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

    // alert($('#gt')[0].value);
    // alert($('#challenge')[0].value);

    var handler = function (captchaObj) {
        captchaObj.appendTo('#captcha');
        captchaObj.onReady(function () {
            $("#wait").hide();
        });
        $('#btn-result').click(function () {
            var result = captchaObj.getValidate();
            console.log(result);
            if (!result) {
                return alert('请完成验证');
            }
            var validate = $('#validate')[0];
            var seccode = $('#seccode')[0];
            validate.value = result.geetest_validate;
            seccode.value = result.geetest_seccode;
        });
        // 更多前端接口说明请参见：http://docs.geetest.com/install/client/web-front/
    };

    $('#text').hide();
    $('#wait').show();
    var gt = $('#gt')[0].value;
    var challenge = $('#challenge')[0].value;
    // 调用 initGeetest 进行初始化
    // 参数1：配置参数
    // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它调用相应的接口
    initGeetest({
        // 以下 4 个配置参数为必须，不能缺少
        gt: gt,
        challenge: challenge,
        offline: false, // 表示用户后台检测极验服务器是否宕机
        new_captcha: true, // 用于宕机时表示是新验证码的宕机

        product: "popup", // 产品形式，包括：float，popup
        width: "300px",
        https: true

        // 更多前端配置参数说明请参见：http://docs.geetest.com/install/client/web-front/
    }, handler);

}

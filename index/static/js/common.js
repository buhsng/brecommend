/** cookie operate **/
//读取设置浏览器cookies
var cookieOperate = /** @class */ (function () {
    function cookieOperate() {
    }
//       cookie名称
    cookieOperate.prototype.getCookie = function (cname) {
        var name = cname + "=";
//        获取所有cookie
        var ca = document.cookie.split(';');
//       遍历所有cookie并去除每个cookie的前导空格 cookie包含name返回cookie值，否则返回空白字符串
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ')
                c = c.substring(1);
            if (c.indexOf(name) != -1)
                return c.substring(name.length, c.length);
        }
        return "";
    };
 //     exday cookie的过期时间/天 cvalue cookie的值
    cookieOperate.prototype.setCookie = function (cname, cvalue, exdays) {
        var d = new Date();
 //     当前时间+过期时间的毫秒数计算cookie过期时间 并转化为utc字符串 设置到doucumentcookie中        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    };
    return cookieOperate;
}());



$(document).ready(function () {
    // 使用jQuery进行ajax请求获取书单数目
    $.ajax({
        type: 'GET',
        url: '/index/getcartnum1/',
         // 定义success回调函数处理服务器响应
         success: function (res) {
            if (res.recode) {
                $('#show_count').text(res.data.allcart);
            } else {
                if (res.data) {
                    alert(res.data.error);
                };
            }
        }
    })

});
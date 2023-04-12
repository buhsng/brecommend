$(function () {
    var name = false;
    var phone = false;
    var password = false;
    var cpassword = false;
    var email = false;
    /*var error_check = false;*/

    $('#txt_username').blur(function () {  /*失去焦点执行*/
        check_user_name();
    });

    $('#txt_phone').blur(function () {  /*失去焦点执行*/
        check_phone();
    });

    $('#txt_password').blur(function () {
        check_password();
    });

    $('#txt_check_password').blur(function () {
        check_cpassword();
    });

    $('#txt_email').blur(function () {
        check_email();
    });

    function check_user_name() {
        var len = $('#txt_username').val().length    /*val 返回被选中的值*/
        if (len < 5 || len > 20) {
            $('#txt_username').next().html('请输入5-20个字符的用户名');
            $('#txt_username').next().show();
            name = true;
        } else {
            name = false;
        }
    }

    function check_phone() {
        var len = $('#txt_phone').val().length    /*val 返回被选中的值*/
        if (len != 11 ) {
            $('#txt_phone').next().html('请输入11位手机号');
            $('#txt_phone').next().show();
            phone = true;
        } else {   /*get() 方法通过远程 HTTP GET 请求载入信息。*/
            $.get('/user/register_exist/?phone=' + $('#txt_phone').val(), function (data) {
                if (data.count == 1) {
                    $('#txt_phone').next().html('手机号已存在').show();
                    phone = true;
                } else {
                    $('#txt_phone').next().hide();
                    phone = false;
                }
            });
            phone = false;
        }
    }

    function check_password() {
        var len = $('#txt_password').val().length;
        if (len < 6 || len > 20) {
            $('#txt_password').next().html('密码最少6位，最长20位');
            $('#txt_password').next().show();
            password = true;
        } else {
            $('#txt_password').next().hide();
            password = false;
        }
    }

    function check_cpassword() {
        var pass = $('#txt_password').val();
        var cpass = $('#txt_check_password').val();

        if (pass != cpass) {
            $('#txt_check_password').next().html('两次输入的密码不一致');
            $('#txt_check_password').next().show();
            cpassword = true;
        } else {
            $('#txt_check_password').next().hide();
            cpassword = false;
        }
    }

    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#txt_email').val()))      //test() 方法用于检测一个字符串是否匹配某个模式.
        {
            $('#txt_email').next().hide();
            email = false;
        } else {
            $('#txt_email').next().html('你输入的邮箱格式不正确');
            $('#txt_email').next().show();
            email = true;
        }
    }

    $('#J_submitRegister').click(function () {
        check_user_name();
        check_password();
        check_cpassword();
        check_email();

        if (name == false && password == false && cpassword == false && email == false)
        {
            $('#reFrom').submit();
            console.log('提交成功');
            return true;
        } else {
            console.log('输入有误');
            return false;
        }
    })


});
$(function () {
    var captcha=false;
    var newpassword=false;
    var newpassword2=false;
    var email=false;


    $('#captcha').blur(function() {  /*失去焦点执行*/
        check_captcha();
    });
    $('#newpassword').blur(function() {  /*失去焦点执行*/
       check_newpassword();
    });
    $('#newpassword2').blur(function() {  /*失去焦点执行*/
       check_newpassword2();
    });
    $('#captcha').focus(function() {  /*失去焦点执行*/
        $('#captcha_tips').hide();
    });
    $('#newpassword').focus(function() {  /*失去焦点执行*/
        $('#newpassword_tips').hide();
    });
    $('#newpassword2').focus(function() {  /*失去焦点执行*/
        $('#newpassword2_tips').hide();
    });



    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#email').val()))      //test() 方法用于检测一个字符串是否匹配某个模式.
        {
            $('#email').next().hide();
            email = false;
        } else {
            $('#email').next().html('你输入的邮箱格式不正确');
            $('#email').next().show();
            email = true;
        }
    }

    function check_captcha() {
        var len = $('#captcha').val().length;
        if(len==0){
            $('#captcha_tips').html('旧密码不能为空!').show();
            captcha = true;
        }
        else
        {
            $('#captcha_tips').hide();
            captcha= false;
        }
    }
    function check_newpassword() {
        var len = $('#newpassword').val().length;
        if(len<8||len>20){
            $('#newpassword_tips').html('密码最少8位，最长20位!').show();
            newpassword = true;
        }
        else
        {
            $('#newpassword_tips').hide();
            newpassword= false;
        }
    }

    function check_newpassword2() {

        var pass = $('#newpassword').val();
        var cpass = $('#newpassword2').val();

        if (pass != cpass) {
            $('#newpassword2_tips').html('密码两次不一样!').show();
            newpassword2= true;
        }
        else {
            $('#newpassword2_tips').hide();
            newpassword2= false;

        }
    }

    $("#sent").click(function(){
        check_email();
        if(email==false){
             $('#reFrom').submit();
              console.log('提交成功');
              return true;
          }else{
             console.log('输入有误');
             return false;
          }
    });

     $('#address_btn').click(function () {
           check_email();
           check_captcha();
           check_newpassword()
           check_newpassword2()


          if(captcha == false && newpassword == false && newpassword2 == false && email==false)
          {
             $('#reFrom').submit();
              console.log('提交成功');
              return true;
          }
          else
          {
             console.log('输入有误');
             return false;
          }
      })

     $('#a_eidpwd')[0].style.color="red";




});

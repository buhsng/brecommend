  //获取指定图片的url，设置为一个元素的src属性
   $(function () {
    // 获取id为mediumimg的元素的src属性，使用split方法将其按照##分割为多个子字符串，取第一个子字符串作为图片的url
       var imgll = $("#mediumImg")[0].src.split("##")[0];//使用数组索引获取dom元素
       //将获取到的图片url设置为id为mediumimg的元素的src属性以显示该图片
       $("#mediumImg").attr('src', imgll);


       //使用jquery的ajax请求代码，向服务器发送post请求并将数据添加到购物车
    var cookieop = new cookieOperate();
    var csrf = cookieop.getCookie('csrftoken');
    // 给id名为addcart的元素添加单击事件
    $('#add_cart').click(function () {
        $.ajax({
            type: 'POST',//请求类型
            url: '/index/addtocart/',//指定请求url
            data: {
                book_bid: $('input[name="pid[]"]').val(),
                pnum: $('input[id="shuliang"]').val(),
                sumprice :$("#zongjia").text(),
            },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf);//在请求头中添加名为x-csrftoken的csrf token
            },
            success: function (res) {//请求成功后执行
                if (res.recode) { //请求返回的res对象中的recode属性是否为真
                    $('#show_count').text(res.data.allcart);//返回的res对象中的data属性中的allcart值设置为showcount的元素的文本值
                    alert('添加成功');//弹窗
                } else {
                    alert(res.data.error);
                }
            }
        })

    });
});

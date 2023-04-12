   $(function () {
       var imgll = $("#mediumImg")[0].src.split("##")[0];
       $("#mediumImg").attr('src', imgll);


       //加入书单
    var cookieop = new cookieOperate();
    var csrf = cookieop.getCookie('csrftoken');
    $('#add_cart').click(function () {
        $.ajax({
            type: 'POST',
            url: '/index/addtocart/',
            data: {
                book_bid: $('input[name="pid[]"]').val(),
                pnum: $('input[id="shuliang"]').val(),
                sumprice :$("#zongjia").text(),
            },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf);
            },
            success: function (res) {
                if (res.recode) {
                    $('#show_count').text(res.data.allcart);
                    alert('添加成功');
                } else {
                    alert(res.data.error);
                }
            }
        })

    });
});

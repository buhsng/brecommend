$(function () {
    //获取html页面中类名为“wrap”的元素，存储在wrap中
    var wrap = document.querySelector(".wrap");
    //给返回首页修改密码按钮添加单击事件
    //给左右箭头按钮添加单击事件，分别执行prev-pic和next-pic函数
    $("#tab-prev").on("click", function () {
        prev_pic();
    });
    $("#tab-next").on("click", function () {
        next_pic();
    });
    //存储当前图片的索引，默认为0
    var index = 0;

    //显示下一张图片并实现图片的滚动效果
    function next_pic() {

        index++;
        if (index > 4) {
            index = 0;
        }
        //调用showcurrentdot函数。更新当前图片指示点
        showCurrentDot();
        // 声明变量newleft，存储图片容器的新左边距
        var newLeft;
        //如果当前显示的是最后一张图片，则将newleft谁职位第一行图片的左边距-1604px，实现滚动效果
        if (wrap.style.left === "-4812px") {
            newLeft = -1604;
        } else { //否则，将newleft设置为当前左边距减去一个图片的宽度802px
            newLeft = parseInt(wrap.style.left) - 802;
        }
        // 图片容器的左边距设置为newleft，实现图片滚动的效果
        wrap.style.left = newLeft + "px";
    }

    //显示上一张图片并实现图片滚动
    function prev_pic() {
        index--;
        if (index < 0) {
            index = 4;
        }
        showCurrentDot();
        var newLeft;
        //如果当前显示的是第一张图片，则设置为最后一张图片的左边距-3208px
        if (wrap.style.left === "0px") {
            newLeft = -3208;
        } else { //否则，将newleft设置为当前左边距加上一个图片的宽度802px
            newLeft = parseInt(wrap.style.left) + 802;
        }
        wrap.style.left = newLeft + "px";
    }

    //存储定时器的id
    var timer = null;

    function autoPlay() {   //自动轮播
        timer = setInterval(function () {   //定时器
            next_pic();
        }, 3000);
    }

    // 给轮播图增加鼠标悬停事件
    autoPlay();
    //获取html页面中类名为container元素存储在container中
    var container = document.querySelector(".container")
    //鼠标移动到container元素上执行函数
    container.onmouseenter = function () {
        clearInterval(timer);//停止自动轮播效果，清除定时器
    }
    //鼠标移开时，执行函数
    container.onmouseleave = function () {
        autoPlay();//重新启动轮播
    }

    //更新指示点，添加单击事件，实现点击指示点切换到对应图片
    //获取html页面中所有标签名为s的元素存储在allL中
    var allL = document.getElementsByTagName("s");
    //更新当前图片指示点
    function showCurrentDot() {
    //遍历所有指示点元素
        for (var i = 0, len = allL.length; i < len; i++) {
            allL[i].style.backgroundColor = '#7f7f7f'; //所有指示点背景设置为灰色
        }
        allL[index].style.backgroundColor = '#fff'; // 当前图片对应指示点背景设置为白色
    }
    //再次遍历
    for (var i = 0, len = allL.length; i < len; i++) {
        //使用闭包和立即执行函数保持i的作用域
        (function (i) {
            allL[i].onclick = function () { //给每个指示点添加单击事件
                var dis = index - i; //计算当前图片索引和单机的指示点索引之间的距离
                if (index == 4 && parseInt(wrap.style.left) !== -4812) {
                    dis = dis - 5; //当前图片是最后一张图片并且左边距不等于-4812px，则将距离减去5，轮播
                }
                //和使用prev和next相同，在最开始的照片5和最终的照片1在使用时会出现问题，导致符号和位数的出错，做相应地处理即可
                if (index == 0 && parseInt(wrap.style.left) !== -802) {
                    dis = 5 + dis;
                }
                //计算图片容器的新左边距，实现切换到对应图片
                wrap.style.left = (parseInt(wrap.style.left) + dis * 802) + "px";
                index = i; //更新当前图片索引
                showCurrentDot();
            }
        })(i);
    }
});

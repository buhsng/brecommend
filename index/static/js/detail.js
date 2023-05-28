 // 用用jquery库实现动态页面交互


 $(function () {
        // 增加数量输入框中的数字，并根据数量和单价计算总价显示在页面上
      $('#jiahao').mousedown(function () {
          var num = $('#shuliang').val(); //获取数量输入框中的当前值并存储在变量num中
            if($('#shuliang').val() < 1000)
            {
            // 数量输入框值设置为一个回调函数的返回值
              	$('#shuliang').val(function () {
                return num * 1 + 1;
            	});
			}
			//数量输入框中的值转换为整数并存储在变量num1中
			var num1 = parseInt($('#shuliang').val());
			//获取单价元素的文本内容，并转换为浮点数，存储在变量num2中
		    var num2 = parseFloat($('#danjia').html());
		    //总价的文本内容设置为一个回调函数的返回值，将num1和num2相乘结果除以10000，使用tofixed（）方法将结果保留两位小数返回
			$('#zongjia').html(function () {
			    return ((num1*100)*(num2*100)/10000).toFixed(2);
			});
        });
        //减少数量输入框数字，根据数量和单价计算总价，显示在页面上
      $('#jianhao').mousedown(function () {
            var num = $('#shuliang').val();
            if($('#shuliang').val() > 1)
            {
              	$('#shuliang').val(function () {
                return num * 1 - 1;
            	});
			}
			var num1 = parseInt($('#shuliang').val());
		    var num2 = parseFloat($('#danjia').html());
			$('#zongjia').html(function () {
			    return ((num1*100)*(num2*100)/10000).toFixed(2);
			});

        });

        //确保输入的数量值在指定的范围内，根据输入数量单价计算总价
      $('#shuliang').change(function(){
        //输入值设置为回调函数的返回值，确保输入值为整数
		    $('#shuliang').val(function () {
				return parseInt($('#shuliang').val());
            });
		     //计算更新总价元素的文本内容
		     jieguo();
		    if($('#shuliang').val()<1){
			    $('#shuliang').val(1);
				jieguo();
			}
			else if($('#shuliang').val() > 365){
			    $('#shuliang').val(365);
			    jieguo();
			}

		});
        //计算更新总价
       function jieguo() {
		    var num1 = parseInt($('#shuliang').val());
		    var num2 = parseFloat($('#danjia').html());
			$('#zongjia').html(function () {
			    return ((num1*100)*(num2*100)/10000).toFixed(2);
			});
        }







   });





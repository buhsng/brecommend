$(function () {
    $('#submit_favor').click(function () {
        let count1=0;
        for(let i=0;i<6;i++) {
            let checked = $('#check'+i).is(':checked');
            if(checked) {
                count1+=1;
            }
        }
        if(count1==0) {
            alert('至少添加一项');
        } else {
            $('#favorFrom').submit();
        }
    })
});
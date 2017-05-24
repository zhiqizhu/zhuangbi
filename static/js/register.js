// if (userName !== '' || Email !== '' || Password1 !== '' || Password2 !== '') {
//     $('.btn').css('opacity', '.9');
//     $('.btn').css('backgroundColor', 'red');
// }
$('.btn').click(function () {
    var userName = $('#exampleInputUsername').val();
    var Email = $('#exampleInputEmail1').val();
    var Password1 = $('#exampleInputPassword1').val();
    var Password2 = $('#exampleInputPassword2').val();
    $(".attention").hide();
    if (userName == '' || userName == null) {
        $('#exampleInputUsername').siblings('.attention').text("用户名不能为空").css('display', 'block');
        $('#exampleInputUsername').focus();
        return;
    }
    if (Email == null) {
        $('#exampleInputEmail1').siblings('.attention').css('display', 'block');
        $('#exampleInputEmail1').focus();
        return;
    }
    if (Password1 == null) {
        $('#exampleInputPassword1').siblings('.attention').css('display', 'block');
        $('#exampleInputEmail1').focus();
        return;
    }
    if (Password2 == null) {
        $('#exampleInputPassword1').siblings('.attention').css('display', 'block');
        $('#exampleInputEmail1').focus();
        return;
    }
    if (Password1 !== Password2) {
        $('#exampleInputPassword2').siblings(".attention").css('display', 'block');
        return;
    }
    // if (Password1.length < 6) {
    //         $('#exampleInputPassword1').siblings('.attention').text("密码必须大于6位").css('display', 'block');
    //         return;
    //     }
    $.ajax({
        url: 'http://127.0.0.1:5000/api/register',// this is server address
        type: 'post',
        timeout: 1000,
        dataType: 'json',
        data: {
            'username': userName,
            'password': Password1,
            'email': Email
        },
        success: function (data) {
            console.log(data);
            if (data.code == 'SUCCESS') {
                alert("注册成功");
                window.location = 'index.html'
            } else {
                alert(data.message);
            }
        }
    })

})


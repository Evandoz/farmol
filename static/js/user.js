//邮箱验证码发送
function sendCodeChangeEmail($btn){
    var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: "get",
        dataType:'json',
        url: "/user/code/",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
        },
        success: function(data){
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            }else if(data.status == 'failure'){
                 Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱验证码发送失败");
            }else if(data.status == 'success'){
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });
}

//修改邮箱
function changeEmailSubmit($btn){
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if(!verify){
        return;
    }
    $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/user/email/",
            data:$('#jsChangeEmailForm').serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                $btn.val("发送中...");
                $btn.attr('disabled',true);
                $("#jsChangeEmailTips").html("验证中...").show(500);
            },
            success: function(data) {
                if(data.email){
                    Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '邮箱信息修改成功！',
                    });
                    //Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱信息更新成功");
                    Dml.fun.winReload();
                    //setTimeout(function() { location.reload(); }, 1500);
                    //setTimeout(function() { window.location.href = window.location.href; }, 1500);
                }else{
                    Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱信息修改失败");
                }
            },
            complete: function(XMLHttpRequest){
                $btn.val("完成");
                $btn.removeAttr("disabled");
            }
    });
}

$(function() {
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function() {
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function() {
        console.log($('#jsResetPwdForm').serialize());
        $.ajax({
            cache: false,
            type: "POST",
            dataType: 'json',
            url: "/user/pwd/",
            data: $('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {
                if (data.password) {
                    Dml.fun.showValidateError($("#pwd"), data.password);
                } else if (data.password2) {
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                } else if (data.status == "success") {
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h5: '密码修改成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                } else if (data.msg) {
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });

    //个人资料头像
    $('.jsAvatarUp').uploadPreview({
        Img: ".jsAvatarShow",
        Width: 120,
        Height: 120,
        Callback: function() {
            $('#jsAvatarForm').submit();
            Dml.fun.showTipsDialog({
                title: '保存成功',
                h5: '图像修改成功！',
            });
            Dml.fun.winReload();
        }
    });


    $('#jsChangeEmailEntry').click(function() {
        Dml.fun.showDialog('#jsChangeEmailDialog', '#jsChangePhoneTips', '#jsChangeEmailTips');
    });
    $('#jsChangeEmailCodeBtn').on('click', function() {
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function() {
        changeEmailSubmit($(this));
    });


    //input获得焦点样式
    $('.perinform input[type=text]').focus(function() {
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function() {
        $(this).parent('li').removeClass('focus');
    });

    verify(
        [
            { id: '#nick_name', tips: Dml.Msg.epNickName, require: true },
            { id: '#mobile', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function() {
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
        verify = verifySubmit(
            [
                { id: '#nick_name', tips: Dml.Msg.epNickName, require: true },
                { id: '#mobile', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true}
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType: 'json',
            url: "/user/info/",
            data: $jsEditUserForm.serialize(),
            async: true,
            beforeSend: function(XMLHttpRequest) {
                _self.val("保存中...");
                _self.attr('disabled', true);
            },
            success: function(data) {
                if (data.nick_name) {
                    _showValidateError($('#nick_name'), data.nick_name);
                } else if (data.address) {
                    _showValidateError($('#address'), data.address);
                } else if (data.status == "failure") {
                    Dml.fun.showTipsDialog({
                        title: data.msg
                    });
                } else if (data.status == "success") {
                    Dml.fun.showTipsDialog({
                        title: '保存成功'
                    });
                    Dml.fun.winReload();
                }
            },
            complete: function(XMLHttpRequest) {
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });
});
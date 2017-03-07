var log = function () {
    console.log.apply(console, arguments)
};

var setup = function () {
    $('.login-div-header > div').on('click', function () {
        var self = $(this);
        $('.orange-bottom-border').removeClass('orange-bottom-border');
        self.addClass('orange-bottom-border')
    });

    var tabAction = function (showLogin) {
        $('#id-div-register').toggle(showLogin);
        $('#id-div-login').toggle(!showLogin);
    };

    $('#id-login').on('click', function () {
        var showLogin = false;
        tabAction(showLogin);
    });

    $('#id-register').on('click', function () {
        var showLogin = true;
        tabAction(showLogin);
    });
};


var bindEventLogin = function () {
    $('#id-login-button').on('click', function () {
        log('login click')
        var username = $('#id-login-username').val();
        var password = $('#id-login-password').val();
        var form = {
            'username': username,
            'password': password
        };
        log(username, password, form)
        var response = function (r) {
            if (r.success) {
                log('login success', r)
                //loginSuccessView()
                location.href = '/weibo/' + String(r.data.id) + '/timeline';
                log(location.href)
            } else {
                log('login fail', r)
                //loginFailView()
            }
        }
        api.login(form, response)
    });
};

var bindEventRegister = function () {
    $('#id-register-button').on('click', function (e) {
        log('register click')
        var username = $('#id-register-username').val();
        var password = $('#id-register-password').val();
        var form = {
            'username': username,
            'password': password
        };
        log(username, password, form)
        var response = function (r) {
            if (r.success) {
                //RegisterSuccessView()
                log('注册成功', r)
                $('#id-login').click();
            } else {
                log('注册失败', r)
                //RegisterFailView()
            }
        }
        api.register(form, response);
    });
};


var bindEvent = function () {
    bindEventLogin();
    bindEventRegister();
};

var __main = function () {
    setup();
    bindEvent();
    $('#id-login').click();
};

$(document).ready(function () {
    __main();
});

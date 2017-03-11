var api = {}

api.ajax = function (url, method, form, callback) {
    var request ={
        url: url,
        type: method,
        data: form,
        success: function (response) {
            log('ajax', response);
            var r = JSON.parse(response);
            callback(r)
        },
        error: function (response) {
            var r = {
                'success': false,
                message: '网络错误'
            };
            callback(r)
        }
    };
    $.ajax(request)
};

api.get = function (url, response) {
    api.ajax(url, 'get', {}, response)
};

api.post = function (url, form, response) {
    api.ajax(url, 'post', form, response)
};

api.login = function (form, response){
    var url = '/login';
    api.post(url, form, response)
};

api.register = function (form, response){
    var url = '/register';
    api.post(url, form, response)
};

api.weiboAdd = function (form, response) {
    var url = '/api/weibo/add';
    api.post(url, form, response)
};

api.weiboDelete = function (form, response) {
    var url = '/api/weibo/delete';
    api.post(url, form, response)
};


api.citeShow = function (form, response) {
  var url = '/api/weibo/citeShow';
  api.post(url, form, response)
}

api.citeAdd = function (form, response) {
  var url = '/api/weibo/cite/add';
  api.post(url, form, response)
}

api.commentShow = function (form, response) {
    var url = '/api/weibo/commentShow';
    api.post(url, form, response)
};

api.commentAdd = function (form, response) {
    var url = '/api/weibo/comment/add';
    api.post(url, form, response)
};

api.weiboCollect = function(form, response) {
    var url = '/api/weibo/collect';
    api.post(url, form, response)
};

api.weiboFavorite = function(form, response) {
    var url = '/api/weibo/favorite';
    api.post(url, form, response)
};

api.commentFavorite = function(form, response) {
    var url = '/api/weibo/comment/favorite';
    api.post(url, form, response)
};

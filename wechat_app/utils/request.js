var HOST_NAME = 'http://127.0.0.1:8000'
var URL = {
    wx_login: '/wx_login',

    topic_post: '/topic/post',
    topic_fetch: '/topic/fetch',
    topic_vote: '/topic/vote',
    topic_post_comment: '/topic/post_comment',

    comment_post_comment: 'comment/post_comment',
    comment_vote: '/comment/vote'
}

module.exports.URL = URL

var CurrentUser = {
    uuid : '',
    wx_openid : ''
}

function login(wx_code, callback) {
    GET(
        URL.wx_login + '?code=' + wx_code,
        function(suc, res) {
            if (suc) {
                CurrentUser = res.data;
                saveUserInfoToLocal();
                console.log('logged in!');
                callback(true);
            }
        }
    );
}
module.exports.login = login

function GET(url, callback) {
    wx.request({
        url: HOST_NAME + url,
        header: {
            'uuid': CurrentUser.uuid
        },
        success: function(res) {
            var suc = res.statusCode === 200;
            console.log(res.data);
            callback(suc, res);
        },
        fail: function() {
            callback(false, null);
        }
    })
}
module.exports.GET = GET

function POST(url, params, callback) {
    wx.request({
        url: HOST_NAME +  url,
        method: 'POST',
        data: params,
        header: {
            'content-type': 'application/json',
            'uuid': CurrentUser.uuid
        },
        success: function(res) {
            var suc = res.statusCode === 200;
            console.log(res.data);
            callback(suc, res);
        },
            fail: function() {
            callback(false, null);
        }
    })
}
module.exports.POST = POST

function loadUserInfoFromLocal() {
     var info = wx.getStorageSync('user_info') || {}
     if (info.uuid !== undefined && info.uuid !== '') {
         CurrentUser = info;
         return true;
     }
     else {
         return false
     }
}
module.exports.loadUserInfoFromLocal = loadUserInfoFromLocal

function saveUserInfoToLocal() {
    wx.setStorageSync('user_info', CurrentUser)
}
module.exports.saveUserInfoToLocal = saveUserInfoToLocal


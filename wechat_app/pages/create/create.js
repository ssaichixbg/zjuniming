//index.js
var RequestManager = require('../../utils/request.js')

//获取应用实例
var app = getApp();

Page({
  data: {
    length: 0,
    content: '',
  },
  //事件处理函数
  handleInput: function(event){
    this.setData({
      length: event.detail.value.length,
      content: event.detail.value
    });
    console.log(event.detail.value);
  },
  //按钮动作
  handleCancle: function(event){
    wx.navigateBack({
      delta: 1
    })
  },
  handlePost: function(event) {
    RequestManager.POST(
      RequestManager.URL.topic_post,
      {content: this.data.content},
      function (suc, res) {
        console.log('post topic succuessful!');
        wx.navigateBack({
          delta: 1
        })
      }
    )
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
  }
})

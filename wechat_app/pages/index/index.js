//index.js
var RequestManager = require('../../utils/request.js')


//获取应用实例
var app = getApp()

Page({
  data: {
    usr: {
      position:"浙江大学"
    },
    order:0,
    orderClass:["order-front-0", "order-front-1"],
    animationStyleIndex:0,
    animationStyleArray:[null, "animation: bounceInUp 0.5s;", null, "animation: bounceOutDown 0.5s;"],
    card:{
      id:0,
      text:"室友没去吃早饭就去上自习，我们托他占第一排座位，他满口答应。等我们吃完去教室，他居然站在门口，郁闷的说：“没戏了，你们看，有一女生用围巾把第一排全占了。”当天自习下课，我们就凑钱买了卷手纸，让他明天带去……",
      vote:{
        number:86,
        state: 0
      },
    },
    comment:{
      number:9,
      list:[
        {
          id:"1",
          from: "蒸煮白膜",
          to: "黄梅黄文",
          like: 30,
          islike: true,
          content: "好巧",
          time: "6小时前" 
        },
        {
          id:"2",
          from: "黄梅黄文",
          to: "蒸煮白膜",
          like: 28,
          islike: false,
          content: "刚刚我们亲亲了",
          time: "6小时前" 
        },
        {
          id:"3",
          from: "黄梅黄文",
          to: "蒸煮白膜",
          like: 8,
          islike: false,
          content: "啊啊啊",
          time: "6小时前" 
        }
      ]
    },
    shareHintDisplay:false,
    commentDisplay: false,
    backgroundDisplay: false,
    isCommenting: false,
    contentRight:0,
    contentLeft:0,
    screenHeight:0,
    screenWidth:0,
    touchStartPos: 0
  },
  //事件处理函数
  handleTouchStart: function(event){
    this.setData({
      touchStartPos: event.touches[0].clientX
    })
  },
  handleTouchMove: function(event) {
    var move = this.data.touchStartPos - event.touches[0].clientX;
    this.setData({
      contentRight: (move<0)?move:0,
      contentLeft:(move<0)?0:0-move
    })
  },
  handleTouchEnd: function(event){
    var move = this.data.touchStartPos - event.changedTouches[0].clientX;
    if(move>-200 && move<200){
      this.setData({
      contentRight: 0,
      contentLeft: 0
    })
    }
  },
  backgroundHind: function(event){
    this.background.hind(this);
  },
  handleCommentDisplay: function(event){
    if(!this.data.commentDisplay){
      this.setData({
        commentDisplay: !this.data.commentDisplay,
        animationStyleIndex: (this.data.animationStyleIndex+1)%4
      });
      var that = this;
      setTimeout(
        function(){
          that.setData({
            animationStyleIndex: (that.data.animationStyleIndex+1)%4
          })
        },500);
    }
    else{
      this.setData({
        animationStyleIndex: (this.data.animationStyleIndex+1)%4
      });
      var that = this;
      setTimeout(
        function(){
          that.setData({
            animationStyleIndex: (that.data.animationStyleIndex+1)%4,
            commentDisplay: !that.data.commentDisplay
          })
        },500);
    }
  },
  handleScrollToLower: function(){
    if(this.data.commentDisplay){
      console.log("to the end");
    }
  },
  //按钮动作
  routeToCreate: function(event){
    wx.navigateTo({
      url:"../create/create"
    })
  },
  desireComment:function(event){
    this.setData({
      backgroundDisplay: true,
      isCommenting: true
    })
  },
  shareHindShow: function(event){
    //this.background.show(this);
    this.setData({
      backgroundDisplay: true,
      shareHintDisplay: true
    });
  },
  backgroundHide: function(event){
    //this.background.hide(this);
    if(this.data.shareHintDisplay){
        this.setData({
          backgroundDisplay: false,
          shareHintDisplay:false
        });
    }
  },
  commentCancel: function(event){
    this.setData({
      backgroundDisplay: false,
      isCommenting:false
    });
  },
  commentSubmit: function(event){
    /*submit*/
    this.setData({
      backgroundDisplay: false,
      isCommenting:false
    })
  },
  orderChange: function(event){
    /*request*/
    /*if succuss*/
    this.setData({
      order: 1-this.data.order
    });
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
    //获取屏幕宽高
    wx.getSystemInfo({
     success: function (res) {
        that.setData({
          screenHeight: res.windowHeight,
          screenWidth: res.windowWidth,
        });
      }
    });

    RequestManager.GET(
      RequestManager.URL.topic_fetch,
      function (suc, res) {
        console.log(res.data.data);
      }
    )

  },
  onShareAppMessage: function () {
    this.backgroundHide();
    return {
      title: '这里有个东东',
      path: '/pages/index/index'
    }
  },
  /*background*/
  background:{
    show: function(that){
      that.setData({
        backgroundDisplay: true
      })  
    },
    hide: function(that){
      that.setData({
        backgroundDisplay: false
      })  
    }
  },
  /*dialog*/
  openConfirm: function () {
        wx.showModal({
            title: '举报',
            content: '举报该页的内容或评论？',
            confirmText: "确认",
            cancelText: "取消",
            confirmColor: "#d0011b",
            success: function (res) {
                console.log(res);
                if (res.confirm) {
                    console.log('用户点击主操作')
                }else{
                    console.log('用户点击辅助操作')
                }
            }
        });
    }
})

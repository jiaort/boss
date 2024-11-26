let ERROR_CODE = {
  SUCCESS: 0,
  UNKNOWN: 1,
  FAILED: 2,
  IN_BLACKLIST: 6,
  PARAM_ERROR: 12,
  NOT_FOUND: 13,
  NOT_LOGIN: 14
};

function msg_info(msg, type, timeout) {
  if (!type) type = 'info';
  if (!timeout) timeout = 3000;
  let id = (new Date).getTime() + '' + parseInt(Math.random() * 100);
  let msg_html = '<div class="pad margin no-print" id="' + id + '">' +
    '<div class="alert alert-' + type + '" style="padding-bottom: 0!important;">' +
    '<h4 style="margin-bottom: 15px;"><i class="fa fa-info"></i>&nbsp;&nbsp;' + msg + '</h4>' +
    '</div>' +
    '</div>';

  $('.show-message').after(msg_html);

  setTimeout(function () {
    $("#" + id).fadeOut();
  }, timeout);

  window.location.href = '#message-top';
}

function toastr_info(msg, type, title, postion) {
  if (!title) title = "";
  if (!msg) msg = "修改成功";
  if (!type) type = "success";  // info warning error
  if (!postion) postion = "toast-top-center";  // toast-bottom-center toast-bottom-full-width toast-top-full-width toast-top-left toast-bottom-left toast-bottom-right toast-top-right
  toastr[type](msg, title, {
    positionClass:     postion,
    closeButton:       true,  // 关闭按钮
    progressBar:       false, // 进度条
    preventDuplicates: true,  // 相同信息只能存在一个
    newestOnTop:       true,  // 最新的提示在最上部
  });
}

function msg_info_small(msg, timeout) {
  if (!timeout) timeout = 3000;
  let id = (new Date).getTime() + '' + parseInt(Math.random() * 100);
  let msg_html = '<div class="default" id="' + id + '">' +
    '<div class="growl growl-error growl-medium">' +
    '<div class="growl-close">×</div><div class="growl-title">Notice!</div><div class="growl-message">' + msg + '</div>' +
    '</div>' +
    '</div>';

  $('.show-message').after(msg_html);
  setTimeout(function () {
    $("#" + id).fadeOut();
  }, timeout);

  window.location.href = '#message-top';
}

$(function(){
  // 短时间显示错误提示 3s
  setTimeout(function () {
    $(".msg-fadeout").fadeOut();
  }, 3000);

  // 长时间显示错误提示 10s
  setTimeout(function () {
    $(".msg-fadeout-long").fadeOut();
  }, 10000);
});

//获取url中的参数
function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg);  //匹配目标参数
  if (r != null) return unescape(r[2]); return null; //返回参数值
}

function setParam(param, value) {
  let query = location.search.substring(1);
  let p = new RegExp("(^|)" + param + "=([^&]*)(|$)");
  if (p.test(query)) {
    let firstParam = query.split(param)[0];
    let secondParam = query.split(param)[1];
    if (secondParam.indexOf("&") > -1) {
      let lastParam = secondParam.substring(secondParam.indexOf('&') + 1);
      return '?' + firstParam + param + '=' + value + '&' + lastParam;
    } else {
      if (firstParam) {
        return '?' + firstParam + param + '=' + value;
      } else {
        return '?' + param + '=' + value;
      }
    }
  } else {
    if (query == '') {
      return '?' + param + '=' + value;
    } else {
      return '?' + query + '&' + param + '=' + value;
    }
  }
}

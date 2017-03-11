var log = function () {
    console.log.apply(console, arguments)
};

var bindEventCommentToggle = function () {
    $('.weibo-container').on('click', '.comment-button', function () {
        var commentContainer = $(this).parent().parent().next('.weibo-comment-container');
        if (commentContainer.hasClass('hide')) {
            var weibo_id = commentContainer.parent().data('id');
            var form = {
                weibo_id: weibo_id
            };
            var response = function (r) {
                if (r.success) {
                    comments = '';
                    cs = r.data;
                    log('cs', cs)
                    for (var i = 0; i < cs.length; i++) {
                        if (cs[i].is_fav) {
                            comments += commentTempalte_fav(cs[i])
                        } else {
                            comments += commentTempalte(cs[i])
                        }
                    }
                    commentContainer.children().children('.weibo-comments').append(comments)
                    commentContainer.slideDown('slow').removeClass('hide');
                }
            };
            api.commentShow(form, response);
        } else {
            commentContainer.children().children('.weibo-comments').children().slideUp('slow').remove()
            commentContainer.slideUp('slow').addClass('hide');
        }
        log('comment click');
        return false
    })
};

var bindEventStatusPanelToggle = function () {
    $('.weibo-container').on('click', '.id-status-panel-control', function () {
        var statusPanel = $(this).next('.id-status-panel');
        statusPanel.toggleClass('hide');
        log('panel click');
        return false
    })
};

var commentTempalte = function (c) {
  t = `
  <div id="id-comment-cell-${ c.id }" data-id="${ c.id }" class="weibo-comment-cell flex">
      <div class="comment-avatar">
          <a href=" ${ "/weibo/" + c.user_id + "/homepage" }">
              <img class="comment-avatar-img" src="${ c.avatar }">
          </a>
      </div>
      <div class="comment-detail">
          <div class="comment-user">
              <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }">${ c.username }:</a>
              <span class="comment-content">
                  ${ c.content }
              </span>
          </div>
          <div class="clearfix">
              <div class="comment-time float-left">${ c.created_time }</div>
              <div class="comment-cell-fav float-right flex">
                  <div class="comment-cell-fav-item">
                      <a href="#">删除</a>
                  </div>
                  <div class="comment-cell-fav-item">
                      <a href="#">回复</a>
                  </div>
                  <div class="comment-cell-fav-item">
                      <a href="#"><span class="comment-fav-icon icon-heart"></span><span class="comment-fav-num">${ c.fav_num }</span></a>
                  </div>
              </div>
          </div>
      </div>
  </div>
  `
    return t
};


var commentTempalte_fav = function (c) {
    t = `
    <div id="id-comment-cell-${ c.id }" data-id="${ c.id }" class="weibo-comment-cell flex">
        <div class="comment-avatar">
            <a href=" ${ "/weibo/" + c.user_id + "/homepage" }">
                <img class="comment-avatar-img" src="${ c.avatar }">
            </a>
        </div>
        <div class="comment-detail">
            <div class="comment-user">
                <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }">${ c.username }:</a>
                <span class="comment-content">
                    ${ c.content }
                </span>
            </div>
            <div class="clearfix">
                <div class="comment-time float-left">${ c.created_time }</div>
                <div class="comment-cell-fav float-right flex">
                    <div class="comment-cell-fav-item">
                        <a href="#">删除</a>
                    </div>
                    <div class="comment-cell-fav-item">
                        <a href="#">回复</a>
                    </div>
                    <div class="comment-cell-fav-item">
                        <a class="comment-fav-button lightbutton" href="#">
                            <span class="comment-fav-icon icon-heart weibo-cell-icon-big"></span>
                            <span class="comment-fav-text"><span class="comment-fav-num">${ c.fav_num }</span></span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
`
    return t
};

var citeTempalte = function (c) {
  t = `
  <div class="weibo-cite-cell flex">
    <div class="comment-avatar">
        <a href=" ${ "/weibo/" + c.user_id + "/homepage" }">
            <img class="cite-avatar-img" src="${ c.avatar }">
        </a>
    </div>
    <div class="cite-detail">
        <div class="cite-user">
            <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }">${ c.username }:</a>
            <span class="cite-content">
               ${ c.content }
            </span>
        </div>
        <div class="clearfix">
            <div class="cite-time float-left">${ c.created_time }</div>
            <div class="cite-cell-fav float-right flex">
                <div class="cite-cell-item">
                    <a href="#">删除</a>
                </div>
                <div class="cite-cell-item">
                    <a href="#">转发</a>
                </div>
                <div class="cite-cell-item">
                    <a href="#"><span class="cite-fav-icon icon-heart"></span><span class="comment-fav-num">${ c.fav_num }</span></a>
                </div>
            </div>
        </div>
    </div>
  </div>
  `
  return t
}

var citeTempalte_fav = function (c) {
  t = `
  <div class="weibo-cite-cell flex">
    <div class="comment-avatar">
        <a href=" ${ "/weibo/" + c.user_id + "/homepage" }">
            <img class="cite-avatar-img" src="${ c.avatar }">
        </a>
    </div>
    <div class="cite-detail">
        <div class="cite-user">
            <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }">${ c.username }:</a>
            <span class="cite-content">
               ${ c.content }
            </span>
        </div>
        <div class="clearfix">
            <div class="cite-time float-left">${ c.created_time }</div>
            <div class="cite-cell-fav float-right flex">
                <div class="cite-cell-item">
                    <a href="#">删除</a>
                </div>
                <div class="cite-cell-item">
                    <a href="#">转发</a>
                </div>
                <div class="cite-cell-item">
                    <a href="#">
                      <span class="cite-fav-icon icon-heart weibo-cell-icon-big"></span>
                      <span class="comment-fav-num">${ c.fav_num }</span>
                    </a>
                </div>
            </div>
        </div>
    </div>
  </div>
  `
  return t
}

var weiboTemplate = function (w) {
    t = `
<div id="id-weibo-cell-${ w.id }" data-id="${ w.id}" class="weibo-cell">
    <div class="weibo-cell-top flex">
        <div class="weibo-avatar-cell">
            <a href="${ "/weibo/" + w.user_id + "/homepage"}">
                <img class="weibo-avatar-img" src="${ w.avatar }">
            </a>
        </div>
        <div class="weibo-detail">
            <div class="clearfix">
                <div class="float-left">
                    <div class="weibo-user"><a href="${ "/weibo/" + w.user_id + "/homepage" }">${ w.username }</a></div>
                    <div class="weibo-time">${ w.created_time }</div>
                    <div class="weibo-content">
                        ${ w.content }
                    </div>
                </div>
                <div class="float-right relative">
                    <a class="id-status-panel-control" href="#"><span class="icon-circle-down"></span></a>
                    <div class="id-status-panel weibo-status-div hide">
                        <div class="weibo-status-item"><a href="#" class="delete-button weibo-status-item-a">删除</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">置顶</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">转换为好友圈可见</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">转换为仅自己可见</a></div>
                    </div>
                </div>
            </div>
            {% if w.has_cite %}
              <div class="weibo-cell-cite" id="id-weibo-cite-${ w.cite_id }" data-id="${ w.cite_id }">
                <div class="weibo-cite-detail">
                  {% if not w.cite_w.is_hidden %}
                    <div>
                        <div class="weibo-cite-user"><a href="${ "/weibo/" + w.cite_w.user_id + "/homepage" }">${ w.cite_w.username }</a></div>
                        <div class="weibo-cite-content">
                            ${ w.cite_w.content }
                        </div>
                        <div class="weibo-cite-bottom clearfix">
                            <div class="weibo-cite-time float-left">${ w.cite_w.created_time }</div>
                            <div class="weibo-cite-cell-fav float-right flex">
                                <div class="weibo-cite-cell-item">
                                    <a href="${ "/weibo/" + w.cite_w.id + "/detail" }"><span class="weibo-cite-fav-icon icon-exit"></span>${ w.cite_w.cite_num }</a>
                                </div>
                                <div class="weibo-cite-cell-item">
                                    <a href="${ "/weibo/" + w.cite_w.id + "/detail" }"><span class="weibo-cite-fav-icon icon-bubble2"></span>${ w.cite_w.comments_num }</a>
                                </div>
                                <div class="weibo-cite-cell-item">
                                    <a href="${ "/weibo/" + w.cite_w.id + "/detail" }"><span class="weibo-cite-fav-icon icon-heart"></span>${ w.cite_w.fav_time }</a>
                                </div>
                            </div>
                        </div>
                    </div>
                  {% else %}
                    <div class="weibo-cite-empty">
                        <div class="weibo-empty-content"><span class="icon-cancel-circle"></span>抱歉，该微博已被原作者删除</div>
                    </div>
                  {% endif %}
                </div>
            </div>
          {% endif%}
        </div>
    </div>
    <div class="weibo-cell-bottom flex">
        <div class="weibo-cell-b-item">
            <a class="collect-button" href="#"><span class="weibo-cell-icon icon-star-empty"></span>${ w.col_num }</a>
        </div>
        <div class="weibo-cell-b-item">
            <a class="" href="cite-button"><span class="weibo-cell-icon icon-exit"></span>${ w.cite_num }</a>
        </div>
        <div class="weibo-cell-b-item">
            <a class="comment-button" href="#"><span class="weibo-cell-icon icon-bubble2"></span>${ w.comments_num }</a>
        </div>
        <div class="weibo-cell-b-item">
            <a class="fav-button" href="#"><span class="weibo-cell-icon icon-heart"></span>${ w.fav_num }</a>
        </div>
    </div>
    <div class="weibo-comment-container hide">
        <div class="comment-container">
            <div class="comment-input-div flex">
                <div class="comment-avatar">
                    <img class="comment-avatar-img" src="${ w.avatar }">
                </div>
                <div class="comment-right">
                    <div class="comment-send-div">
                        <textarea class="comment-send-textarea"></textarea>
                    </div>
                    <div class="clearfix">
                        <div class="comment-send-tool float-left flex">
                            <div class="comment-send-item">
                                <a href="#"><span class="weibo-send-icon icon-smile"></span></a>
                            </div>
                            <div class="comment-send-item">
                                <a href="#"><span class="weibo-send-icon icon-image"></span></a>
                            </div>
                            <div class="comment-send-choice">
                                <div><input type="checkbox" >同时转发到我的微博</div>
                                <div><input type="checkbox" >同时评论给 瓜</div>
                            </div>
                        </div>
                        <div class="comment-setting float-right">
                            <a class="comment-send-button button-white-a" href="#">
                                评论
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="weibo-comments">
            </div>
        </div>
    </div>
    <div class="weibo-cite-container hide">
        <div class="cite-container">
            <div class="cite-input-div">
                <div class="cite-top flex">
                    <div class="cite-top-item cite-top-item-active"><a href="#">转发到微博</a></div>
                    <div class="cite-top-item"><a href="#">转发到私信</a></div>
                </div>
                <div class="cite-bottom">
                    <div class="cite-send-div">
                        <textarea class="cite-send-textarea"></textarea>
                    </div>
                    <div class="clearfix">
                        <div class="cite-send-tool float-left flex">
                            <div class="cite-send-item">
                                <a href="#"><span class="weibo-send-icon icon-smile"></span></a>
                            </div>
                            <div class="cite-send-item">
                                <a href="#"><span class="weibo-send-icon icon-image"></span></a>
                            </div>
                            <div class="cite-send-choice">
                                <div><input type="checkbox" >同时评论给 好东西传送门</div>
                                <div><input type="checkbox" >同时评论给原文作者 瓜</div>
                            </div>
                        </div>
                        <div class="cite-setting float-right">
                            <a class="cite-status-radio" href="#"><span class="cite-status">公开</span><span class="icon-circle-down"></span></a>
                            <div class="cite-status-div hide">
                                <div class="cite-status-item"><a href="#" class="cite-status-item-a">公开</a></div>
                                <div class="cite-status-item"><a href="#" class="cite-status-item-a">好友圈</a></div>
                                <div class="cite-status-item"><a href="#" class="cite-status-item-a">仅自己可见</a></div>
                            </div>
                            <a class="cite-send-button button-white-a" href="#">
                                转发
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="cite-comments">
            </div>
        </div>
    </div>
</div>
`
    return t
};

var bindEventWeiboAdd = function () {
    $('#id-weibo-send-button').on('click', function () {
        var content = $('#id-weibo-content').val();
        var form = {
            content: content
        };
        log('weibo add click', form);
        var response = function (r) {
            log('weibo add r', r);
            if (r.success) {
                log('add weibo success');
                var weibo = weiboTemplate(r.data);
                var weiboContainer = $('.weibo-container');
                weiboContainer.prepend(weibo).slideDown('slow');
            } else {
                log('add weibo fail')
            }
        };
        api.weiboAdd(form, response);
        return false
    })
};

var bindEventCommentAdd = function () {
    $('.weibo-container').on('click', '.comment-send-button', function () {
        var content = $(this).parent().parent().prev().children().val();
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var weiboCommentsContainer = $(this).parents('.comment-container').children('.weibo-comments');
        log('comment add click', content, weibo_id);
        var form = {
            content: content,
            weibo_id: weibo_id
        };
        var response = function (r) {
            log('comment add response', r);
            if (r.success) {
                var comment = commentTempalte(r.data);
                log(weiboCommentsContainer, $(this))
                weiboCommentsContainer.prepend(comment).slideDown('slow');
            } else {
                log('add comment fail')
            }
        };
        api.commentAdd(form, response);
        return false
    })
};

var bindEventWeiboDelete = function () {
    $('.weibo-container').on('click', '.delete-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var weiboContainer = $(this).closest('.weibo-cell');
        var form = {
            weibo_id: weibo_id
        };
        log('delete click', form);
        var response = function (r) {
            log('weibo delete', r);
            if (r.success) {
                log('weibo delete success');
                weiboContainer.slideUp('slow').remove()
            } else {
                log('weibo delete fail');
            }
        };
        api.weiboDelete(form, response);
        return false
    })
};


var bindEventCiteToggle = function () {
  $('.weibo-container').on('click', '.cite-button', function () {
      var citeContainer = $(this).parent().parent().next().next();
      var weibo_cell = citeContainer.parent()
      var weibo_user = $.trim(weibo_cell.find('.weibo-user').text())
      var weibo_content = $.trim(weibo_cell.find('.weibo-content').text())
      var cited_weibo_id = $(this).parents('.weibo-cell').find('.weibo-cell-cite').data('id');
      if (citeContainer.hasClass('hide')) {
          var weibo_id = citeContainer.parent().data('id');
          var cite_send_textarea = citeContainer.find('.cite-send-textarea')
          var form = {
              weibo_id: weibo_id
          };
          var response = function (r) {
              if (r.success) {
                  cites = '';
                  cs = r.data;
                  log('cs', cs);
                  for (var i = 0; i < cs.length; i++) {
                      if (cs[i].is_fav) {
                          cites += citeTempalte_fav(cs[i])
                      } else {
                          cites += citeTempalte(cs[i])
                      }
                  }
                  citeContainer.children().children('.cite-comments').append(cites)
                  if (cited_weibo_id) {
                    var content = '//@' + weibo_user + ':' + weibo_content
                    log('cite textarea', content)
                    cite_send_textarea.text(content)
                  }
                  citeContainer.slideDown('slow').removeClass('hide');
              }
          };
          api.citeShow(form, response);
      } else {
          citeContainer.children().children('.cite-comments').children().slideUp('slow').remove();
          citeContainer.slideUp('slow').addClass('hide');
      }
      log('cite button click');
      return false
  })
};

var bindEventWeiboCiteAdd = function () {
  $('.weibo-container').on('click', '.cite-send-button', function () {
      var content = $(this).parent().parent().prev().children().val();
      var weibo_id = $(this).closest('.weibo-cell').data('id');
      var cited_weibo_id = $(this).parents('.weibo-cell').find('.weibo-cell-cite').data('id');
      var weiboCitesContainer = $(this).parents('.cite-container').children('.cite-comments');
      if (cited_weibo_id) {
        var cite_id = cited_weibo_id
      } else {
        var cite_id = weibo_id
      }
      var form = {
          content: content,
          cite_id: cite_id
      };
      var response = function (r) {
          log('cite add response', r);
          if (r.success) {
              var cite = citeTempalte(r.data);
              log(weiboCitesContainer, $(this))
              weiboCitesContainer.prepend(cite).slideDown('slow');
          } else {
              log('add cite fail')
          }
      };
      api.citeAdd(form, response);
      return false
  })
}


var weiboCollect = function (form, collect_btn) {
    var response = function (r) {
            if (r.success) {
                log('weibo collect', r.data);
                collect_btn.children('.weibo-cell-b-item-text').text('已收藏');
                collect_btn.children('.weibo-cell-icon').removeClass('icon-star-empty')
                                    .addClass('weibo-cell-icon-big icon-star-full');
                collect_btn.addClass('lightbutton')
            } else {
                log('微博收藏失败')
            }
        };
    api.weiboCollect(form, response);
};

var weiboDisCollect = function (form, collect_btn) {
    var response = function (r) {
            if (r.success) {
                log('weibo discollect', r.data);
                collect_btn.children('.weibo-cell-b-item-text').text('收藏');
                collect_btn.children('.weibo-cell-icon').removeClass('weibo-cell-icon-big icon-star-full')
                                                        .addClass('icon-star-empty');
                collect_btn.removeClass('lightbutton')
            } else {
                log('微博取消收藏失败')
            }
        };
    api.weiboCollect(form, response);
};

var bindEventWeiboCollect = function () {
    $('.weibo-container').on('click', '.collect-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var collect_btn = $(this);
        log('collect_btn', collect_btn);
        var form = {
            weibo_id: weibo_id
        };
        if (collect_btn.hasClass('lightbutton')) {
            //showdisCollectPanel()
            log('weibo discollect');
            weiboDisCollect(form, collect_btn)
        } else {
            log('weibo collect');
            weiboCollect(form, collect_btn)
        }
        return false
    });
};


var weiboFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            log('weibo favor', r.data);
            var f_text = fav_btn.children().children('.weibo-fav-num').text();
            var f_n_text = String(parseInt(f_text) + 1);
            log('weibo favor', f_text, f_n_text)
            fav_btn.children().children('.weibo-fav-num').text(f_n_text)
            fav_btn.children('.weibo-cell-icon').addClass('weibo-cell-icon-big');
            fav_btn.addClass('lightbutton')
        }
    };
    api.weiboFavorite(form, response);
};

var weiboUnFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            log('weibo unfavor', r.data);
            var f_text = fav_btn.children().children('.weibo-fav-num').text();
            var f_n_text = String(parseInt(f_text) - 1);
            log('weibo unfavor', f_text, f_n_text)
            fav_btn.children().children('.weibo-fav-num').text(f_n_text)
            fav_btn.children('.weibo-cell-icon').removeClass('weibo-cell-icon-big');
            fav_btn.removeClass('lightbutton')
        }
    };
    api.weiboFavorite(form, response);
};

var bindEventWeiboFav = function () {
    $('.weibo-container').on('click', '.fav-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var fav_btn = $(this);
        var form = {
            weibo_id: weibo_id
        };
        if (fav_btn.hasClass('lightbutton')) {
            weiboUnFavorite(form, fav_btn)
        } else {
            weiboFavorite(form, fav_btn)
        }
        return false;
    });
};


var commentFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            log('comment favor', r.data);
            var f_text = fav_btn.children().children('.comment-fav-num').text();
            var f_n_text = String(parseInt(f_text) + 1);
            log('comment favor', f_text, f_n_text)
            fav_btn.children().children('.comment-fav-num').text(f_n_text)
            fav_btn.children('.comment-fav-icon').addClass('weibo-cell-icon-big');
            fav_btn.addClass('lightbutton')
        }
    };
    api.commentFavorite(form, response);
};

var commentUnFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            log('comment unfavor', r.data);
            var f_text = fav_btn.children().children('.comment-fav-num').text();
            var f_n_text = String(parseInt(f_text) - 1);
            log('comment unfavor', f_text, f_n_text)
            fav_btn.children().children('.comment-fav-num').text(f_n_text);
            fav_btn.children('.comment-fav-icon').removeClass('weibo-cell-icon-big');
            fav_btn.removeClass('lightbutton')
        }
    };
    api.commentFavorite(form, response);
};

var bindEventCommentFav = function () {
    $('.weibo-container').on('click', '.comment-fav-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var fav_btn = $(this);
        var comment_id = fav_btn.closest('.weibo-comment-cell').data('id');
        var form = {
            weibo_id: weibo_id,
            comment_id: comment_id
        };
        if (fav_btn.hasClass('lightbutton')) {
            commentUnFavorite(form, fav_btn)
        } else {
            commentFavorite(form, fav_btn)
        }
        return false;
    })
};


var bindEventPersonInfoPanelToggle = function () {
    $('.weibo-container').on('click', '.weibo-avatar-img', function () {

    })
};


var bindEvent = function () {
    bindEventCommentToggle();
    bindEventStatusPanelToggle();
    bindEventWeiboAdd();
    bindEventCiteToggle();
    bindEventWeiboCiteAdd();
    bindEventCommentAdd();
    bindEventWeiboDelete();
    bindEventWeiboCollect();
    bindEventWeiboFav();
    bindEventCommentFav();
    bindEventPersonInfoPanelToggle();
};

var __main = function () {
    bindEvent();
};

$(document).ready(function () {
    __main();
});

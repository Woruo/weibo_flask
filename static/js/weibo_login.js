var log = function () {
    console.log.apply(console, arguments)
};

var bindEventCommentToggle = function () {
    $('.main-container').on('click', '.comment-button', function () {
        var commentContainer = $(this).parent().parent().next('.weibo-comment-container');
        var citeContainer = commentContainer.parent().children('.weibo-cite-container');
        if (commentContainer.hasClass('hide')) {
            var weibo_id = commentContainer.parent().data('id');
            var form = {
                weibo_id: weibo_id
            };
            var response = function (r) {
                if (r.success) {
                    comments = '';
                    cs = r.data;
                    for (var i = 0; i < cs.length; i++) {
                        if (cs[i].is_fav) {
                            comments += commentTempalte_fav(cs[i])
                        } else {
                            comments += commentTempalte(cs[i])
                        }
                    }
                    commentContainer.children().children('.weibo-comments').append(comments);
                    if ( !citeContainer.hasClass('hide') ) {
                        citeContainer.addClass('hide')
                        citeContainer.hide()
                    }
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
    $('.main-container').on('click', '.id-status-panel-control', function () {
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
              <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }>${ c.username }:</a>
              <span class="comment-content">
                  ${ c.content }
              </span>
          </div>
          <div class="clearfix">
              <div class="comment-time float-left">${ c.created_time }</div>
              <div class="comment-cell-fav float-right flex">
                  <div class="comment-cell-fav-item">
                      <a class="comment-fav-button" href="#">
                           <span class="comment-fav-icon icon-heart"></span>
                           <span class="comment-fav-num"><span class="comment-fav-num">${ c.fav_num }</span></span>
                      </a>
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
                <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }>${ c.username }:</a>
                <span class="comment-content">
                    ${ c.content }
                </span>
            </div>
            <div class="clearfix">
                <div class="comment-time float-left">${ c.created_time }</div>
                <div class="comment-cell-fav float-right flex">
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
            <a class="orange-a" href=${ "/weibo/" + c.user_id + "/homepage" }>${ c.username }:</a>
            <span class="cite-content">
               ${ c.content }
            </span>
        </div>
        <div class="clearfix">
            <div class="cite-time float-left">${ c.created_time }</div>
            <div class="cite-cell-fav float-right flex">               
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
                    </div>
                </div>
            </div>
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
                        </div>
                        <div class="cite-setting float-right">                           
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


var bindEventWeiboTag = function () {
    $('.weibo-send-item').on('click', function () {
        log('weibo-tag click')
        var self = $(this);
        var active_item = $('.weibo-send-tag-active');
        if (self.data('id') == active_item.data('id')) {
            self.removeClass('weibo-send-tag-active')
        } else {
            $('.weibo-send-tag-active').removeClass('weibo-send-tag-active');
            self.addClass('weibo-send-tag-active')
        }
    });
}

var bindEventWeiboAdd = function () {
    $('#id-weibo-send-button').on('click', function () {
        var content = $('#id-weibo-content').val();
        var tag_id = $('.weibo-send-tag-active').data('id');
        var form = {
            content: content,
        };
        if ($.inArray(tag_id, [1, 2, 3, 4, 5]) != -1) {
            form['tag_id'] = tag_id
        }
        var response = function (r) {
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

var bindEventWeiboDelete = function () {
    $('.main-container').on('click', '.delete-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var weiboContainer = $(this).closest('.weibo-cell');
        var form = {
            weibo_id: weibo_id
        };
        var response = function (r) {
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


// 微博转发
var bindEventCiteToggle = function () {
    $('.main-container').on('click', '.cite-button', function () {
        var citeContainer = $(this).parent().parent().next().next();
        var commentContainer = citeContainer.parent().children('.weibo-comment-container');
        var weibo_cell = citeContainer.parent();
        var weibo_user = $.trim(weibo_cell.find('.weibo-user').text());
        var weibo_content = $.trim(weibo_cell.find('.weibo-content').text());
        var origin_weibo_id = $(this).parents('.weibo-cell').find('.weibo-cell-cite').data('id');
        if (citeContainer.hasClass('hide')) {
            var weibo_id = citeContainer.parent().data('id');
            var cite_send_textarea = citeContainer.find('.cite-send-textarea');
            var form = {
                weibo_id: weibo_id
            };
            var response = function (r) {
                if (r.success) {
                    cites = '';
                    cs = r.data;
                    for (var i = 0; i < cs.length; i++) {
                        if (cs[i].is_fav) {
                            cites += citeTempalte_fav(cs[i])
                        } else {
                            cites += citeTempalte(cs[i])
                        }
                    }
                    citeContainer.children().children('.cite-comments').append(cites);
                    if (origin_weibo_id) {
                        var content = '//@' + weibo_user + ':' + weibo_content;
                        cite_send_textarea.text(content)
                    }
                    if ( !commentContainer.hasClass('hide') ) {
                        commentContainer.addClass('hide');
                        commentContainer.children().children('.weibo-comments').children().slideUp('slow').remove()
                        commentContainer.hide()
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
    $('.main-container').on('click', '.cite-send-button', function () {
        var content = $(this).parent().parent().prev().children().val();
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var origin_weibo_id = $(this).parents('.weibo-cell').find('.weibo-cell-cite').data('id');
        if (!origin_weibo_id) {
            origin_weibo_id = weibo_id
        }
        var weiboCitesContainer = $(this).parents('.cite-container').children('.cite-comments');
        var form = {
            content: content,
            cite_id: weibo_id,
            origin_w_id: origin_weibo_id
        };
        var response = function (r) {
            if (r.success) {
                var cite = citeTempalte(r.data);
                weiboCitesContainer.prepend(cite).slideDown('slow');
            } else {
                log('add cite fail')
            }
        };
        api.citeAdd(form, response);
        return false
    })
}


// 微博收藏
var weiboCollect = function (form, collect_btn) {
    var response = function (r) {
        if (r.success) {
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
    $('.main-container').on('click', '.collect-button', function () {
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var collect_btn = $(this);
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


// 微博点赞
var weiboFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            var f_text = fav_btn.children().children('.weibo-fav-num').text();
            var f_n_text = String(parseInt(f_text) + 1);
            log('weibo favor')
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
            var f_text = fav_btn.children().children('.weibo-fav-num').text();
            var f_n_text = String(parseInt(f_text) - 1);
            log('weibo unfavor');
            fav_btn.children().children('.weibo-fav-num').text(f_n_text)
            fav_btn.children('.weibo-cell-icon').removeClass('weibo-cell-icon-big');
            fav_btn.removeClass('lightbutton')
        }
    };
    api.weiboFavorite(form, response);
};

var bindEventWeiboFav = function () {
    $('.main-container').on('click', '.fav-button', function () {
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


var bindEventCommentAdd = function () {
    $('.main-container').on('click', '.comment-send-button', function () {
        var content = $(this).parent().parent().prev().children().val();
        var weibo_id = $(this).closest('.weibo-cell').data('id');
        var weiboCommentsContainer = $(this).parents('.comment-container').children('.weibo-comments');
        var form = {
            content: content,
            weibo_id: weibo_id
        };
        var response = function (r) {
            log('comment add success');
            if (r.success) {
                var comment = commentTempalte(r.data);
                weiboCommentsContainer.prepend(comment).slideDown('slow');
            } else {
                log('add comment fail')
            }
        };
        api.commentAdd(form, response);
        return false
    })
};


// 评论点赞
var commentFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            var f_text = fav_btn.children().children('.comment-fav-num').text();
            var f_n_text = String(parseInt(f_text) + 1);
            fav_btn.children().children('.comment-fav-num').text(f_n_text);
            fav_btn.children('.comment-fav-icon').addClass('weibo-cell-icon-big');
            fav_btn.addClass('lightbutton')
        }
    };
    api.commentFavorite(form, response);
};

var commentUnFavorite = function (form, fav_btn) {
    var response = function (r) {
        if (r.success) {
            var f_text = fav_btn.children().children('.comment-fav-num').text();
            var f_n_text = String(parseInt(f_text) - 1);
            log('comment unfavor');
            fav_btn.children().children('.comment-fav-num').text(f_n_text);
            fav_btn.children('.comment-fav-icon').removeClass('weibo-cell-icon-big');
            fav_btn.removeClass('lightbutton')
        }
    };
    api.commentFavorite(form, response);
};

var bindEventCommentFav = function () {
    $('.main-container').on('click', '.comment-fav-button', function () {
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



//关注和取消关注
var Follow = function (form, follow_btn) {
    var response = function (r) {
        if (r.success) {
            var f_text = follow_btn.text();
            var f_n_text = '已关注';
            log('follow success');
            follow_btn.empty().append(f_n_text);
            follow_btn.addClass('followed');
        }
    };
    api.followPerson(form, response);
};

var unFollow = function (form, follow_btn) {
    var response = function (r) {
        if (r.success) {
            var f_text = follow_btn.text();
            var f_n_text = `<span class="icon-checkmark"></span> 关注`;
            log('unfollow success');
            follow_btn.empty().append(f_n_text);
            follow_btn.removeClass('followed');
        }
    };
    api.followPerson(form, response);
};

var bindEventFollow = function () {
    $('.main-container').on('click', '.follow-btn', function () {
        var u_id = $(this).closest('.follow-person-cell').data('id');
        var follow_btn = $(this);
        var form = {
            u_id: u_id,
        };
        if (follow_btn.hasClass('followed')) {
            unFollow(form, follow_btn)
        } else {
            Follow(form, follow_btn)
        }
        return false;
    })
};


var BigFollow = function (form, follow_btn) {
    var response = function (r) {
        if (r.success) {
            var f_n_text = '已关注';
            log('follow success');
            follow_btn.empty().append(f_n_text);
            follow_btn.removeClass('header-option-item-active');
        }
    };
    api.followPerson(form, response);
};

var unBigFollow = function (form, follow_btn) {
    var response = function (r) {
        if (r.success) {
            var f_n_text = `关注`;
            log('unfollow success');
            follow_btn.empty().append(f_n_text);
            follow_btn.addClass('header-option-item-active');
        }
    };
    api.followPerson(form, response);
};

var bindEventBigFollow = function () {
    $('.main-container').on('click', '.follow-button', function () {
        var u_id = $(this).closest('.homepage-person-detail').data('id');
        var follow_btn = $(this);
        var form = {
            u_id: u_id,
        };
        if ( !follow_btn.hasClass('header-option-item-active') ) {
            unBigFollow(form, follow_btn)
        } else {
            BigFollow(form, follow_btn)
        }
        return false;
    })
};


var bindEvent = function () {
    bindEventCommentToggle();
    bindEventStatusPanelToggle();
    bindEventWeiboTag();
    bindEventWeiboAdd();
    bindEventCiteToggle();
    bindEventWeiboCiteAdd();
    bindEventCommentAdd();
    bindEventWeiboDelete();
    bindEventWeiboCollect();
    bindEventWeiboFav();
    bindEventCommentFav();
    bindEventFollow();
    bindEventBigFollow();
};


var __main = function () {
    bindEvent();
};

$(document).ready(function () {
    __main();
});

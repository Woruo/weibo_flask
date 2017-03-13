
// 首页微博显示
// var bindEventWeiboHomeShow = function () {
//
// };
// // 我的收藏微博显示
// var bindEventWeiboCollectShow = function () {
//   $('.my-col-button').on('click', function () {
//       log('my collect weibo btn click');
//       var response = function (r) {
//         log('my collect r', r);
//         if (r.success) {
//             log('show collect success');
//             weibos = '';
//             ws = r.data;
//             log('ws', ws)
//             for (var i = 0; i < ws.length; i++) {
//                 weibos += weiboTemplate(ws[i])
//             }
//             var weiboContainer = $('.weibo-container');
//             $('.weibo-send-container').addClass('hide');
//             $('.weibo-nav ').addClass('hide');
//             $('.weibo-collect-bar').removeClass('.hide');
//             weiboContainer.empty();
//             weiboContainer.prepend(weibos).slideDown('slow');
//         } else {
//             log('show collect fail')
//         }
//       };
//       api.weiboColShow(response);
//       return false
//   })
// };
//
// // 我的赞微博显示
// var bindEventWeiboFavShow = function () {
//
// };
// // 不同Tag标签微博显示
// var bindEventWeiboTagShow = function () {
//
// };


`
<div id="id-weibo-cell-${ w.id }" data-id="${ w.id }" class="weibo-cell">
    <div class="weibo-cell-top flex">
        <div class="weibo-avatar-cell">
            <a href="${ "/weibo/" + w.user_id + "/homepage"}">
                <img class="weibo-avatar-img" src="${ w.avatar }">
            </a>
        </div>
        <div class="weibo-detail">
            <div class="clearfix">
                <div class="weibo-detail-left float-left">
                    <div class="weibo-user">
                      <a href="${ "/weibo/" + w.user_id + "/homepage" }">
                        ${ w.username }
                      </a>
                    </div>
                    <div class="weibo-time">${ w.created_time }</div>
                    <div class="weibo-content">
                        ${ w.content }
                    </div>
                </div>
                <div class="weibo-detail-right float-right relative">
                    <a class="id-status-panel-control" href="#"><span class="icon-circle-down"></span></a>
                    <div class="id-status-panel weibo-status-div hide">
                        <div class="weibo-status-item"><a href="#" class="delete-button weibo-status-item-a">删除</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">置顶</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">转换为好友圈可见</a></div>
                        <div class="weibo-status-item"><a href="#" class="weibo-status-item-a">转换为仅自己可见</a></div>
                    </div>
                </div>
            </div>
              <div class="weibo-cell-cite" id="id-weibo-cite-${ w.cite_id }" data-id="${ w.cite_id }">
                <div class="weibo-cite-detail">
                  {% if not w.cite_w.is_hidden %}
                    <div>
                        <div class="weibo-cite-user">
                            <a href={{ url_for('weibo.homepage', user_id=w.cite_w.user_id) }}>
                                {{ w.cite_w.user.username }}
                            </a>
                        </div>
                        <div class="weibo-cite-content">
                            {{ w.cite_w.content }}
                        </div>
                        <div class="weibo-cite-bottom clearfix">
                            <div class="weibo-cite-time float-left">{{ w.cite_w.created_time }}</div>
                            <div class="weibo-cite-cell-fav float-right flex">
                                <div class="weibo-cite-cell-item">
                                    <a href={{ url_for('weibo.detail', id=w.cite_w.id) }}>
                                      <span class="weibo-cite-fav-icon icon-exit"></span>
                                      {% if w.cite_w.cite_num %}
                                        {{ w.cite_w.cite_num }}
                                      {% else %}
                                        0
                                      {% endif %}
                                    </a>
                                </div>
                                <div class="weibo-cite-cell-item">
                                    <a href={{ url_for('weibo.detail', id=w.cite_w.id) }}>
                                      <span class="weibo-cite-fav-icon icon-bubble2"></span>
                                      {{ w.cite_w.comments_num }}
                                    </a>
                                </div>
                                <div class="weibo-cite-cell-item">
                                    <a href={{ url_for('weibo.detail', id=w.cite_w.id) }}>
                                      <span class="weibo-cite-fav-icon icon-heart"></span>
                                      {{ w.cite_w.fav_time }}
                                    </a>
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
          {% if w.is_collected %}
            <a class="collect-button lightbutton" href="#">
                <span class="weibo-cell-icon icon-star-full weibo-cell-icon-big"></span>
                <span class="weibo-cell-b-item-text">已收藏</span>
            </a>
          {% else %}
            <a class="collect-button" href="#">
                <span class="weibo-cell-icon icon-star-empty"></span>
                <span class="weibo-cell-b-item-text">收藏</span>
            </a>
          {% endif %}
        </div>
        <div class="weibo-cell-b-item">
            <a class="cite-button" href="#">
              <span class="weibo-cell-icon icon-exit"></span>
              {% if w.cite_num %}
                {{ w.cite_num }}
              {% else %}
                转发
              {% endif %}
            </a>
        </div>
        <div class="weibo-cell-b-item">
          <a class="comment-button" href="#">
            <span class="weibo-cell-icon icon-bubble2"></span>{{ w.comments_num }}
          </a>
        </div>
        <div class="weibo-cell-b-item">
            {% if w.is_favored %}
              <a class="fav-button lightbutton" href="#">
                  <span class="weibo-cell-icon icon-heart weibo-cell-icon-big"></span>
                  <span class="weibo-cell-b-item-text"><span class="weibo-fav-num">{{ w.fav_num }}</span></span>
              </a>
            {% else %}
              <a class="fav-button" href="#">
                  <span class="weibo-cell-icon icon-heart"></span>
                  <span class="weibo-cell-b-item-text"><span class="weibo-fav-num">{{ w.fav_num }}</span></span>
              </a>
            {% endif %}
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
                                {% if w.has_cite %}
                                    <div><input type="checkbox" >同时评论给 {{ w.cite_w.user.username }}</div>
                                {% endif %}
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
                                <div><input type="checkbox" >同时评论给 {{ w.username }}</div>
                                {% if w.has_cite %}
                                  <div><input type="checkbox" >同时评论给原文作者 {{ w.cite_w.user.username }}</div>
                                {% endif %}
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
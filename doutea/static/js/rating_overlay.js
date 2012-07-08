

(function($) {

    var G = {};

    var methods = {
        init: function(options) {
            var defaults = {

            };

            var root = G.root = this;
            var options = $.extend(defaults, options);

            // create rating overlay
            root.addClass("RO_root");
            var content = $("<div>").addClass("RO_content"),

            upper = $("<div>").addClass("RO_upper").appendTo(content),

            close = $("<div>").addClass("RO_close").addClass("close").appendTo(upper),
            dishname = G.dishname = $("<div>").addClass("RO_dishname").appendTo(upper),
            star = G.star = $("<div>").addClass("RO_star").addClass("sstar").appendTo(upper),

            my_rating = $("<div>").addClass("RO_myrating").html("给个评价吧").appendTo(upper),
            my_rating_star = $("<div>").addClass("star").appendTo(my_rating),

            comment = G.comment = $("<textarea>").addClass("RO_comment").appendTo(upper),
            reply = $("<button>").addClass("RO_reply_button").html("评论").appendTo(upper),
            
            lower = G.lower = $("<div>").addClass("RO_lower").appendTo(content);

            content.appendTo(root);

            G.current_star = 0;         // 当前显示的条目的星数


            // myratings: 鼠标移过显示相应的星数
            G.current_myrating = 0;     // 用于保存当前用户对条目打的星数

            var set_star = G.set_star = function(rating) {
                var current_rating = my_rating_star.attr('rel');
                my_rating_star.removeClass('star-' + current_rating).addClass('star-' + rating).attr({rel:rating});
            };

            var replace_entity = function(s) {
                return s.replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/\"/g, "&quot;")
                    .replace(/\n/g, "<br/>");
            };

            var show_comments = G.show_comments = function(ratings) {
                var comment_area = G.lower;
                comment_area.empty();
                var html = '';
                for (var i = 0; i < ratings.length; i++) {
                    var rating = ratings[i];
                    var comment_block = $("<div>").addClass('RO_commentblock');
                    $("<div>").html('<a href="' + rating.user.home_url + '" target="_blank">' + rating.user.nickname + '</a> ' + rating.update_time)
                        .css({float:'left'})
                        .appendTo(comment_block);
                    $("<div>").addClass("sstar").addClass("RO_lowersstar").addClass("sstar-" + rating.rating).appendTo(comment_block);
                    $("<div>").addClass("clear").appendTo(comment_block);
                    $("<div>").html(replace_entity(rating.comment)).appendTo(comment_block);
                    comment_block.appendTo(comment_area);
                }
            };

            var show_overlay_content = G.show_overlay_content = function(data) {
                dishname.html(data.dish.name);
                star.removeClass('sstar-' + G.current_star)
                    .addClass('sstar-' + data.dish.rating)
                    .html(data.dish.rating_count + "人评价");
                G.current_star = data.dish.rating;

                // 在ratings中找到当前用户的评分
                my_rating = { comment: '', rating: 0 };
                for (var i = 0; i < data.dish.ratings.length; i++) {
                    if (data.dish.ratings[i].user.id == G.user_id) {
                        my_rating = data.dish.ratings[i];
                        break;
                    }
                }

                // 设置我的评分的星数&评论
                G.current_myrating = my_rating.rating;
                set_star(my_rating.rating);
                comment.val(my_rating.comment);

                show_comments(data.dish.ratings);
            };

            my_rating_star.css({cursor:"pointer"}).mousemove(function(e) {
                // 根据鼠标位置显示不同的星
                var x = e.offsetX ? e.offsetX : (e.target ? e.clientX - $(this).offset().left : 0),
                current_rating = $(this).attr('rel'),
                rating = Math.floor(x / 15) * 2 + 2;

                if (rating > 10) rating = 10;

                if (rating != current_rating) {
                    set_star(rating);
                }
            }).mouseout(function(e) {
                set_star(G.current_myrating);
            }).click(function(e) {
                // 保存
                var x = e.offsetX ? e.offsetX : (e.target ? e.clientX - $(this).offset().left : 0),
                rating = Math.floor(x / 15) * 2 + 2;
                if (rating > 10) rating = 10;

                G.current_myrating = rating;
            });

            // 单击回应按钮提交评价
            reply.click(function() {
                var comment_text = comment.val().trim(),
                rating = G.current_myrating;

                if (comment_text == '') {
                    alert("请填写评论。");
                    return;
                }

                if (rating == 0) {
                    alert("请给个评分。");
                    return;
                }

                $.post('/d' + G.dish_id + '/rate', { rating: rating, comment: comment_text }, function(data) {
                    if (data.result == 'ok') {
                        // refresh
                        $.getJSON('/d' + G.dish_id + '/detail', function(data) {
                            G.show_overlay_content(data);
                        });
                    } else {
                        alert("评论出错了");
                    }
                }, 'json');
            });


            // add overlay effect
            root.overlay({
                mask: {
                    color: '#333',
                    loadSpeed: 100,
                    opacity: 0.2
                },
                closeOnClick: true,
                load: false,
            });

            return this;
        },

        load: function(dish_id, user_id) {
            var root = G.root;
            G.dish_id = dish_id;
            G.user_id = user_id;

            $.getJSON('/d' + dish_id + '/detail', function(data) {
                G.show_overlay_content(data);

                root.overlay().load();
            });
        },

        __NULL__: null
    };
    

    $.fn.rating_overlay = function(method) {
        // Method calling logic
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error( 'Method ' + method + ' does not exist on jQuery.selecttable' );
        }
    };


})(jQuery);

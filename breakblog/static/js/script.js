//网站运行时间
function show_runtime() {
    window.setTimeout("show_runtime()", 1000);
    let X = new Date("9/19/2019 00:00:00");
    let Y = new Date();
    let T = (Y.getTime() - X.getTime());
    let M = 24 * 60 * 60 * 1000;
    let a = T / M;
    let A = Math.floor(a);
    let b = (a - A) * 24;
    let B = Math.floor(b);
    let c = (b - B) * 60;
    let C = Math.floor((b - B) * 60);
    let D = Math.floor((c - C) * 60);
    $('#runtime').html("Runtime : " + A + "天" + B + "小时" + C + "分" + D + "秒");
}

//评论回复时间，悬浮提示具体时间
function render_time() {
    let time = moment($(this).data('timestamp')).format('LLL');
    $('[data-toggle="tooltip"]').tooltip({ title: time });
}

//回复表单提示语
function set_palceholder() {
    $('#author').attr('placeholder', '昵称');
    $('#email').attr('placeholder', '邮箱');
    $('#site').attr('placeholder', "主页 (可不填)");
    $('#body').attr('placeholder', "评论");
}

//图片自动添加类class="img-fluid"
function add_img_class() {
    $('img').addClass('img-fluid');
}

//入口
$(function () {
    show_runtime();
    render_time();
    set_palceholder();
    add_img_class();
});

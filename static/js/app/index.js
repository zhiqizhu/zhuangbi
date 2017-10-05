//mouseover 的效果
$('.user_info').mouseover(function () {
    $('.dropdown-menu').addClass('open');
})
$('.user_info').mouseout(function () {
    $('.dropdown-menu').removeClass('open');
})

//swiper 的效果
var mySwiper = new Swiper('.swiper-container', {
    direction: 'vertical',
    loop: true,
    autoplay: 5000,

    // 如果需要分页器
    pagination: '.swiper-pagination',

    // 如果需要前进后退按钮
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev'

    // 如果需要滚动条
//    scrollbar: '.swiper-scrollbar',
})

// 给列表绑定数据
$(document).ready(function () {
    var vm = new Vue({
        el: "#ul",
        data: {
            posts:[],
            banners:[]
        },
        mounted: function () {
            $.ajax({
                url: "http://127.0.0.1:5000/api/post",
                method: "get",
                type: "json",
                success: function (data) {
                    vm.posts=data;
                }
            })
            $.ajax({
                url:"http://127.0.0.1:5000/api/banners",
                method: "get",
                type: "json",
                success: function (data) {
                    console.log(data.data)
                    vm.banners=data.data;
                }

            })
        }

    })
});

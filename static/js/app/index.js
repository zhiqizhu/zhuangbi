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


})

// 给列表绑定数据
$(document).ready(function () {
    var vm = new Vue({
        el: "#ul",
        data: {
            posts:[],
            banners:[],
            page:"1",
            paging:"1"
        },
        mounted: function () {

            this.pageFunction();
            $.ajax({
                url:"http://127.0.0.1:5000/api/banners",
                method: "get",
                type: "json",
                success: function (data) {
                    vm.banners=data.data;
                }

            })
        },
        methods:{
            pageFunction:function () {
                var _this=this
                $.ajax({
                url: "http://127.0.0.1:5000/api/post",
                data:{page :_this.page, size: 5},
                method: "get",
                type: "json",
                success: function (data) {
                    if (data==null ||data.length ==0){
                        $('.learnmore').attr('disabled',true)
                    }
                     _this.posts=_this.posts.concat(data);

                    return _this.page++
                }
            })
            },
            // pagingFunction:function () {
            //     var _this=this
            //     var total
            //     $.ajax({
            //     url: "http://127.0.0.1:5000/api/post",
            //     data:{page :_this.paging, size: 5},
            //     method: "get",
            //     type: "json",
            //     success: function (data) {
            //         console.log(data)
            //         _this.posts=data
            //         total=Math.round(data.length/5);
            //         console.log(total)
            //         return _this.paging++
            //     }
            // })
            // }
        }

    })
});

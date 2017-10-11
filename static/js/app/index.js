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
            posts: [],
            banners: [],
            page: "1",
            paging: "1",
            pagingNum: '',
        },
        mounted: function () {
            this.pagingFunction();
            $.ajax({
                url: "http://127.0.0.1:5000/api/banners",
                method: "get",
                type: "json",
                success: function (data) {
                    vm.banners = data.data;
                }

            })
        },
        methods: {
            // pageFunction: function () {
            //     var _this = this
            //     $.ajax({
            //         url: "http://127.0.0.1:5000/api/post",
            //         data: {page: _this.page, size: 2},
            //         method: "get",
            //         type:"json",
            //         success:function (resp) {
            //             console.log(resp)
            //             if (resp.data==null|| resp.data.length==0){
            //                  $('.learnmore').attr('disabled',true)
            //             }
            //             _this.posts= _this.posts.concat(resp.data);
            //             return  _this.page++
            //
            //         }
            //     })
            // },
            //
            // pagingFunction: function (n) {
            //     var _this = this
            //     $.ajax({
            //         url: "http://127.0.0.1:5000/api/post",
            //         data: {page: n, size: 3},
            //         method: "get",
            //         type: "json",
            //         success: function (resp) {
            //             _this.posts = resp.data
            //             var total = resp.total
            //             _this.pagingNum = Math.ceil(total / 3);
            //         }
            //     })
            // }
            pagingFunction:function (n) {
                var _this=this
                console.log(n)
                $.ajax({
                     url: "http://127.0.0.1:5000/api/post",
                    data: {page:n, size: 3},
                    method: "get",
                    type: "json",
                    success:function (resp) {
                         console.log(resp)
                        _this.posts=resp.data
                        _this.pagingNum=Math.ceil(resp.total/3)
                    }
                })
            }
        }

    })
});

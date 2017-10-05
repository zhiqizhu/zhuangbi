var vm = new Vue({
    el: "#article",
    data: {
        title: "",
        content: "",
        comment: "",
        comments: [],
    },
    methods: {
        GetQueryString: function (name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null)return unescape(r[2]);
            return null;
        },
        comment_submit: function (e) {
            var _this = this;
            $.ajax({
                url: "http://127.0.0.1:5000/api/comment",
                method: "post",
                type: "json",
                data: $.param({
                    post_id: _this.GetQueryString("id"),
                    body: _this.comment

                }),
                success: function (data) {
                    console.log(data)
                    if(data.code==="SUCCESS") {
                        _this.load_data();
                        _this.comment='';
                    }
                }
            })
        },
        load_data: function () {
            var _this = this;
            $.ajax({
                url: "http://127.0.0.1:5000/api/post/" + _this.GetQueryString("id"),
                method: "get",
                type: "json",
                success: function (data) {
                    console.log(data)
                    _this.title = data.title;
                    _this.content = data.content;
                    _this.comments = data.comments;
                }
            })
        }
    },
    mounted: function () {
        this.load_data()

    }
})

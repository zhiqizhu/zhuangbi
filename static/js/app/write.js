$(document).ready(function () {
    var vm = new Vue({
        el: "#edit",
        data: {
            title: "",
            content: '',
            img: ''
        },
        methods: {
            onSubmit: function () {
                this.loadImage()
                $.ajax({
                    url: "http://127.0.0.1:5000/api/post",
                    method: "post",
                    type: "json",
                    cache: false,
                    data: new FormData($('#edit')[0]),
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        console.log(data);
                        if (data.code == "SUCCESS") {
                            window.location = "index.html"
                        }
                    },
                    error: function (res) {
                        console.log(res)
                        alert("提交失败")
                    }
                })
            },
            loadImage: function () {
                var _this = this
                _this.img = $('.upload').find('input')[0].files[0];

            }
        }

    })
})
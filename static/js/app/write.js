// var editor = new Simditor({
//     textarea: $('#editor'),
//     // placeholder: '随便写会让你灵感迸发哦~',
//     // params: {},
//     // upload: {
//     //     url: '',
//     //     params: null,
//     //     fileKey: 'upload_file',
//     //     connectionCount: 3,
//     //     leaveConfirm: 'Uploading is in progress, are you sure to leave this page?'
//     // },
//     // tabIndent: true,
//     // toolbar: [
//     //     'title',
//     //     'bold',
//     //     'italic',
//     //     'underline',
//     //     'strikethrough',
//     //     'fontScale',
//     //     'color',
//     //     'ol',
//     //     'ul',
//     //     'blockquote',
//     //     'code',
//     //     'table',
//     //     'link',
//     //     'image',
//     //     'hr',
//     //     'indent',
//     //     'outdent',
//     //     'alignment'
//     // ],
//     // allowedTags: ['br', 'span', 'a', 'img', 'b', 'strong', 'i', 'strike', 'u', 'font', 'p', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'hr'],
//     // toolbarFloat: true,
//     // toolbarFloatOffset: 0,
//     // toolbarHidden: false,
//     // pasteImage: false,
//     // cleanPaste: false
// });
$(document).ready(function () {
    var vm = new Vue({
        el: "#edit",
        data: {
            title: "",
            content:''
        },
        methods: {
            onSubmit: function () {
                $.ajax({
                    url: "http://127.0.0.1:5000/api/post",
                    method: "post",
                    type: "json",
                    data: $.param({
                        title: vm.title,
                        content: vm.content
                    }),
                    success: function (data) {
                        console.log(data);
                        if (data.code=="SUCCESS"){
                            window.location = "index.html"

                        }
                    },
                    error:function () {
                        alert("提交失败")
                    }
                })
            }
        }

    })
})
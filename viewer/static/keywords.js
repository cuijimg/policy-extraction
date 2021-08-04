ew_row = '<div class="keyword_cont">' +
    '<button class="remove_button">-</button>' +
    '<span class="keyword" contenteditable="true">...</span>' +
    '</div>'

$(document).on("click", ".remove_button", function(){
    $(this).closest("div").remove();
});

function add_keyword(id) {
    $(id).append(new_row)
}

function upload() {
    let keys = {};
    $('.topic_cont').each((pos, obj) => {
        let topic = obj.getAttribute('topic');
        let arr = [];
        $(obj).find('.keyword').each((pos_keyword, elem_keyword) => {
            arr.push($(elem_keyword).text());
        });
        keys[topic] = arr;
    });

    let fillers = [];
    $('#fillers').find('.keyword').each((pos_keyword, elem_keyword) => {
        fillers.push($(elem_keyword).text());
    });

    let join = [];
    $('#join_words').find('.keyword').each((pos_keyword, elem_keyword) => {
        join.push($(elem_keyword).text());
    });

    let data;
    data = {
        'keys': keys,
        'fillers': fillers,
        'join_words': join
    };

    $.ajax({
        method: 'POST',
        url: '/keywords',
        contentType: 'application/json',
        data: JSON.stringify(data)
    });
}
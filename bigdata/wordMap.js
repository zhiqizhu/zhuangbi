function wordMap() {

    //find words in the document text
    if (!this.keyword) return;
    var words = this.keyword.split(" ");

    if (words == null) {
        return;
    }

    for (var i = 0; i < words.length; i++) {
        //emit every word, with count of one
        emit(words[i], {count: 1});
    }

}
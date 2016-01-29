AppModule.filter('firstLetter', function () {
    return function (input, letter, prop) {

        input = input || [];
        var out = [];

        if (letter==="0-9") {
            input.forEach(function (item) {
                var itembis = (prop)? item[prop]: item;
                if (/^\d.*/.test(itembis)) {
                    out.push(item);
                }
            });
        }
        else{
            input.forEach(function (item) {
                var itembis = (prop)? item[prop]: item;
                if (itembis.charAt(0).toUpperCase() == letter) {
                    out.push(item);
                }
            });
        }

        return out;
    }
});


var fs = require('fs')
var extract = require('pdf-text-extract')

var input = process.argv.slice(2)[0]
var output = process.argv.slice(2)[1]

extract(input, function (err, pages) {
    if (err) {
        console.dir(err)
        return
    }
    // pages is an array, join it into a string
    var text = Array.isArray(pages) ? pages.join('\n') : pages
    fs.writeFile(output, text, (error) => {
        if (error) {
            console.log(error);
        } else {
            console.log(output + " DONE")
        }
    });
})
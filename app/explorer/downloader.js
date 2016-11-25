var page = require('webpage').create();
var fs = require('fs');// File System Module
var args = system.args;
var output = 'test1.html'; // path for saving the local file
page.open('http://www.duckduckgo.com?q=harry+potter', function() { // open the file
  fs.write(output,page.content,'w'); // Write the page to the local file using page.content
  phantom.exit(); // exit PhantomJs
});

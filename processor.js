// headings trigger a new slide
// headings with a caret (e.g., '##^ foo`) trigger a new vertical slide
// // and images will be surrounded with tags allowing them to not overflow
module.exports = (markdown, options) => {

  return markdown.split('\n').map((line, index) => {
    //test images
    if(/!\[[^]]+\]\([^)]+\)/g.test(line) || /^<img([\w\W]+?)\/>/g.test(line))
    {
      return '<div style="height:500px;width:100%;max-width:500px;max-height: 500px;display:inline-block; overflow:hidden;">\n'+line+"\n</div>"
    }
    //test headers and vertical headers
    if(!/^#/.test(line) || index === 0) return line;
    const is_vertical = /#\^/.test(line);
    line = line.replace('#^', '#');

    if(is_vertical)
    {
      return "\n----\n\n" + line
    }
    else
    {
      const is_h1 = /^#{1}([^#].*)$/gm.test(line);
      if(is_h1 && index > 1){//skip the first title so we don't insert another slide
        return "\n---\n\n" + line
      }

      else
        return line
    }

  }).join('\n');
};

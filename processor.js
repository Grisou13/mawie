// headings trigger a new slide
// headings with a caret (e.g., '##^ foo`) trigger a new vertical slide
module.exports = (markdown, options) => {
  // console.log(options);
  // options.separator= "^(\r\n?|\n)----(\r\n?|\n)$"
  // options.verticalSeparator='^(\r\n?|\n)----(\r\n?|\n)$'
  // console.log(options);
  return markdown.split('\n').map((line, index) => {
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

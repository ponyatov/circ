
function g(w)    { return w.join("") }
function s(c,g)  { return "<span class="+c+">"+g+"</span>" }
function u(rl)   { return "<a href="+rl+">"+rl+"</a>" }
function e(mail) { return "<a href=mailto:"+mail+">"+mail+"</a>" }

grammar = peg.generate(`
dump    = w:(class/gt/hash/cycle/slot/.)*

email   = n:name a:"@" d:domain   {return e(n+a+d)}
url     = h:"http://" d:domain    {return u(h+d)}
domain  = w:[a-z\.\-]+            {return g(w)}

slot    = n:name e:eq             {return s("slot",n)+e}
class   = l:lt n:name c:":"       {return l+s("clazz",n)+s("op",c)}
name    = w:[a-zA-Z0-9А-Яа-я_]+   {return g(w)}
lt      = "<"                     {return s("lg","&lt;")}
gt      = "> "                    {return s("lg","&gt; ")}
hash    = a:"@" w:[0-9a-f]+       {return s("hash",a+g(w))}
cycle   = w:" _/"                 {return s("op",w)}
eq      = w:" = "                 {return s("op",w)}
`)

$(
        $(".dump").each(
            function(idx,item) {
                $(this).html(
                    grammar.parse(
                        $(this).text()))})
)


require 'sinatra'
require "liquid"

class Motioner < Sinatra::Base
  get '/' do
    liquid :layout
  end

  get '/generate', provides: [:text] do
    template = Liquid::Template.parse(File.read(File.join(File.dirname(__FILE__), 'views', 'template.liquid')))
    locals = params
    locals["items"] = locals["items"].values
    locals["authors"] = locals["authors"].values

    if locals["document_type"] == "motion"
      locals["i_or_we"] = locals["authors"].length > 1 ? "vi" : "jag"
    else
      locals["i_or_we"] = "D-rektoratet"
    end

    template.render(locals)
  end
end

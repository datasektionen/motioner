require 'sinatra'
require 'liquid'

class Motioner < Sinatra::Base
  get '/' do
    liquid :'layout.html'
  end

  get '/generate', provides: [:text] do
    template = Liquid::Template.parse(File.read(File.join(File.dirname(__FILE__), 'views', 'template.tex.liquid')))
    locals = params

    if locals['document_type'] == 'motion'
      locals['i_or_we'] = locals['authors'].length > 1 ? 'vi' : 'jag'
    else
      locals['i_or_we'] = 'D-rektoratet'
    end

    attachment locals['document_type']+'.tex'
    template.render(locals)
  end
end

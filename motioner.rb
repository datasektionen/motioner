# encoding: utf-8
require 'sinatra'
require "liquid"

class Motioner < Sinatra::Base
  get '/' do
    liquid :layout
  end

  get '/generate', provides: [:text] do
    template = Liquid::Template.parse(File.read(File.join(File.dirname(__FILE__), 'views', 'template.liquid')))
  #  liquid :template, locals: params
    locals = params
    locals["items"] = locals["items"].values
    locals["authors"] = locals["authors"].values
    template.render(locals)
  end
end

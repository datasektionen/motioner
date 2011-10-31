require File.dirname(__FILE__) + '/motioner.rb'

use Rack::ShowExceptions

run Motioner.new

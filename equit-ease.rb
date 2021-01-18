class EquitEase < Formula
    desc "The easiest way to access data about stocks, options, cryptocurrencies, and more from the command line."
    homepage "https://github.com/danmurphy1217/equit-ease"

    url "https://github.com/danmurphy1217/equit-ease/zipball/main", :using => :curl

    def install
        bin.install "danmurphy1217/equit-ease"
    end
end
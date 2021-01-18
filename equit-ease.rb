class EquitEase < Formula
  include Language::Python::Virtualenv
  desc "The easiest way to access data about stocks, options, cryptocurrencies, and more from the command line."
  homepage "https://github.com/danmurphy1217/equit-ease"
  license "MIT"
  head "https://github.com/danmurphy1217/equit-ease.git"
  version "0.0.1"

  depends_on "python@3.8"

  # depends_on "cmake" => :build

  def install
    # ENV.deparallelize  # if your formula fails when building in parallel
    # Remove unrecognized options if warned by configure
    system "./configure", "--disable-debug",
                          "--disable-dependency-tracking",
                          "--disable-silent-rules",
                          "--prefix=#{prefix}"

  end

  test do
    # `test do` will create, run in and delete a temporary directory.
    #
    # This test will fail and we won't accept that! For Homebrew/homebrew-core
    # this will need to be a test that verifies the functionality of the
    # software. Run the test with `brew test equit-ease`. Options passed
    # to `brew install` such as `--HEAD` also need to be provided to `brew test`.
    #
    # The installed folder is not in the path, so use the entire path to any
    # executables being tested: `system "#{bin}/program", "do", "something"`.
    system "true"
  end
end

class Chatter < Formula
  desc "Chatter Formula"
  homepage ""
  url "file:///Users/chris/code/chatter/chatter-1.0.0.tar.gz"
  version "1.0.0"
  sha256 "7db7af880f8d938d6f77b7c5501c1becf492d627a4b308c7f675e5780255e8a8"

  def install
    (bin/"chatter").write <<~EOS
      #!/bin/bash
      source /Users/chris/code/dotfiles/.env
      source /Users/chris/code/chatter/.venv/bin/activate
      cd /Users/chris/code/chatter/chatter
      exec streamlit run app.py --server.port=8505
    EOS
  end

  service do
    run [opt_bin/"chatter"]
    keep_alive true
    working_dir var
    log_path var/"log/chatter.log"
    error_log_path var/"log/chatter.log"
  end
end

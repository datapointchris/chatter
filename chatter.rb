class Chatter < Formula
  desc "Chatter Formula"
  homepage ""
  url "file:///Users/chris/code/chatter/chatter-1.0.0.tar.gz"
  version "1.0.0"
  sha256 "4c4885338eeb8bad5ec5fe1070851bba1cbf0481df09089390c6b18cf4343595"

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

#!/usr/bin/env bash

FILENAME="chatter-1.0.0.tar.gz"

echo "Uninstalling chatter"
brew uninstall chatter

echo "Removing old cached tar files"
rm /Users/chris/Library/Caches/Homebrew/downloads/*"$FILENAME"

echo "Removing and Recreating tar file"
rm -f "./$FILENAME"
tar -czf "$FILENAME" .

echo "Creating checksum"
CHECKSUM=$(shasum -a 256 "$FILENAME" | awk '{ print $1 }')

echo "Updating formula with new checksum"

sed -i '' "s/sha256 \".*\"/sha256 \"$CHECKSUM\"/" chatter.rb

echo "Reinstalling chatter"
brew install --force --build-from-source "$(pwd)/chatter.rb"

echo "Restarting chatter service"
brew services restart chatter

#!/bin/sh
set -e

echo "Installing packages!"
npm install

echo "Server is starting!"
exec npm run dev
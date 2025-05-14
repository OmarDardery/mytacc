#!/bin/bash

echo "📦 Installing Node dependencies..."
cd templates/mainApp_react/liasu || exit
npm install
chmod +x ./node_modules/.bin/react-scripts
echo "🏗️ Building React..."
npm run build
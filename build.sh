#!/bin/bash

echo "📦 Installing Node dependencies..."
cd templates/mainApp_react/liasu || exit
npm install

echo "🏗️ Building React..."
npm run build
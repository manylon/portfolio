#!/bin/bash

# Build React app if BUILD_REACT_APP is set to 1
if [ "$BUILD_REACT_APP" -eq 1 ]; then
  echo "Building React app..."
  yarn build
else
  echo "Skipping React app build."
fi

# Build Storybook if BUILD_STORYBOOK is set to 1
if [ "$BUILD_STORYBOOK" -eq 1 ]; then
  echo "Building Storybook..."
  yarn build-storybook
else
  echo "Skipping Storybook build."
fi
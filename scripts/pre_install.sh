git clone https://github.com/mity/md4c.git --depth 1
cd md4c
cmake -B build
cmake --build build
cd build
cmake --install .
cd ../..
rm -rf md4c

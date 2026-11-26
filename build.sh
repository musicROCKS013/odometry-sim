c++ -O3 -Wall -shared -std=c++17 -undefined dynamic_lookup \
  $(python -m pybind11 --includes) \
  backend.cpp -o backend$(python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
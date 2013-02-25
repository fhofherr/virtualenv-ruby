1. Modifiy existing virtualenv:
   * installation of gems into virtualenv
   * requires the following environment variables to be set::

     export GEM_HOME="$VIRTUAL_ENV/gems"
     export GEM_PATH=""
     export PATH=$PATH:"$GEM_HOME/bin" 

   * Either add them to the postactivate hook, or append activation code to
     the activate script (like nodeenv does)

2. Download and install user-specified ruby version. This might require the
   activate script to be modified.

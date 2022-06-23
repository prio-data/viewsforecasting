## Package checker

if(!require(tictoc,quietly = T)){
  cat('Installing tictoc...', "\n")
  install.packages("tictoc",repos = "https://cloud.r-project.org")
  require(tictoc)
  cat('tictoc installed...', "\n")
}

if(!require(ranger,quietly = T)){
  cat('Installing ranger...', "\n")
  install.packages("ranger",repos = "https://cloud.r-project.org")
  require(ranger)
  cat('ranger installed...', "\n")
}


if(!require(tidyverse,quietly = T)){
  cat('tidyverse ranger...', "\n")
  install.packages("tidyverse",repos = "https://cloud.r-project.org")
  require(tidyverse)
  cat('tidyverse installed...', "\n")
}

if(!require(magrittr,quietly = T)){
  cat('magrittr ranger...', "\n")
  install.packages("magrittr",repos = "https://cloud.r-project.org")
  require(tidyverse)
  cat('magrittr installed...', "\n")
}

if(!require(arrow,quietly = T)){
  cat('arrow ranger...', "\n")
  install.packages("arrow",repos = "https://cloud.r-project.org")
  require(tidyverse)
  cat('arrow installed...', "\n")
}

cat("\n",'All required packages installed',"\n")



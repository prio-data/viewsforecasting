## Package checker


if(!require(ranger,quietly = T)){
  cat('Installing ranger...', "\n")
  install.packages("ranger",repos = "https://cloud.r-project.org")
  require(ranger)
  cat('ranger installed...', "\n")
}


if(!require(tidyverse,quietly = T)){
  cat('Installing tidyverse ...', "\n")
  install.packages("tidyverse",repos = "https://cloud.r-project.org")
  require(tidyverse)
  cat('tidyverse installed...', "\n")
}

if(!require(magrittr,quietly = T)){
  cat('Installing magrittr ...', "\n")
  install.packages("magrittr",repos = "https://cloud.r-project.org")
  require(magrittr)
  cat('magrittr installed...', "\n")
}

if(!require(arrow,quietly = T)){
  cat('Installing arrow ...', "\n")
  install.packages("arrow",repos = "https://cloud.r-project.org")
  require(arrow)
  cat('arrow installed...', "\n")
}

cat("\n",'All required packages installed',"\n")



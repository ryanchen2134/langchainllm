library(googlesheets4) # provides oauth browser implementation
library(tidyverse)
library(reticulate) # provides access to python

source_python("./src/main.py")
use_virtualenv("./venv")
#read google sheet with year, film format
dat <- read_sheet("1-y3-3wSL8p12kGCF0Qqgl6I1aGSex0nrkdLLytN5eoA") %>%
  mutate(film = as.character(film)) %>%
  select(year, film) %>%
  mutate(resp = NA)

for (r in 50:nrow(dat)) {
    cat("prompting", r, "\n")
    dat$resp[r] <- str_replace_all( 
        prior_films(dat$year[r], dat$film[r]), #chatgpt prompt
        fixed("\n"),
        " " 
    )
    #wrrite to csv here
    cat("writing", r, "\n")
    if (r == 1) {
        write_csv(dat[r, ], "prior_films.csv")
    } else {
        write_csv(dat[r, ], "prior_films.csv", append = TRUE)
    }

    Sys.sleep(runif(1, 2, 10))
}